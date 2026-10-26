using System.Globalization;
using System.Security.Cryptography;
using System.Text;
using LeitorDeJornal.Domain;
namespace LeitorDeJornal.Application;

/// <summary>Casos de uso. Não conhece MVC, caminhos de arquivos ou bibliotecas de extração.</summary>
public sealed class LibraryService(ICatalogStore store, IDocumentExtractor extractor, IDraftStore drafts)
{
    public Task<List<BookSummary>> ListAsync(string? query, string? format, string? sort, CancellationToken ct) =>
        store.ReadAsync(c =>
        {
            var books = c.Books.Where(b => (string.IsNullOrWhiteSpace(query) ||
                b.Title.Contains(query.Trim(), StringComparison.CurrentCultureIgnoreCase)) &&
                (string.IsNullOrWhiteSpace(format) || b.Format == format));
            books = sort switch { "title" => books.OrderBy(b => b.Title), "oldest" => books.OrderBy(b => b.ImportedAt),
                _ => books.OrderByDescending(b => b.LastOpenedAt ?? b.ImportedAt) };
            return books.Select(b => new BookSummary(b.Id, b.Title, b.Format, b.Text.Length, b.Position,
                b.ImportedAt, b.LastOpenedAt, b.Annotations.Count)).ToList();
        }, ct);

    public async Task<ImportDraft> PreviewAsync(string owner, string filename, Stream input, CancellationToken ct)
    {
        var extension = Path.GetExtension(filename).ToLowerInvariant();
        if (extension is not (".txt" or ".pdf" or ".epub"))
            throw new ReaderException("Formato não suportado. Selecione TXT, PDF textual ou EPUB refluível sem DRM.");
        var result = await extractor.ExtractAsync(input, extension, ct);
        if (string.IsNullOrWhiteSpace(result.Text)) throw new ReaderException("Nenhum texto legível foi encontrado. PDFs digitalizados precisam de OCR, indisponível nesta versão.");
        if (result.Text.Length > Limits.MaxCharacters) throw new ReaderException("O texto excede o limite de 5 milhões de caracteres.");
        var draft = new ImportDraft(Guid.NewGuid(), Path.GetFileNameWithoutExtension(filename), extension[1..].ToUpperInvariant(),
            result.Text, result.Contents, result.Warnings, DateTimeOffset.UtcNow.AddMinutes(15));
        drafts.Put(owner, draft);
        return draft;
    }
    public ImportDraft Draft(string owner, Guid token) => drafts.Get(owner, token) ??
        throw new ReaderException("A prévia expirou. Selecione o arquivo novamente.");
    public void Cancel(string owner, Guid token) => drafts.Remove(owner, token);

    public async Task<Guid> ConfirmAsync(string owner, Guid token, string title, bool accepted, CancellationToken ct)
    {
        var draft = Draft(owner, token);
        if (draft.Warnings.Count > 0 && !accepted) throw new ReaderException("Leia e aceite os alertas da prévia para continuar.");
        title = title.Trim();
        if (title.Length is < 1 or > 200) throw new ReaderException("Informe um título com até 200 caracteres.");
        var revision = Hash(draft.Text);
        var id = await store.UpdateAsync(c =>
        {
            var duplicate = c.Books.FirstOrDefault(b => b.Revision == revision);
            if (duplicate is not null) return duplicate.Id;
            if (c.Books.Count >= Limits.MaxBooks) throw new ReaderException("O acervo atingiu o limite de 1.000 obras.");
            var book = new Book { Title = title, Format = draft.Format, Text = draft.Text, Revision = revision, Contents = draft.Contents };
            c.Books.Add(book);
            return book.Id;
        }, ct);
        drafts.Remove(owner, token);
        return id;
    }
    public Task<Book?> GetAsync(Guid id, CancellationToken ct) => store.ReadAsync(c => c.Books.FirstOrDefault(b => b.Id == id), ct);
    public Task<bool> DeleteAsync(Guid id, CancellationToken ct) => store.UpdateAsync(c => c.Books.RemoveAll(b => b.Id == id) > 0, ct);
    public Task<long> SaveProgressAsync(Guid id, ProgressCommand command, CancellationToken ct) => store.UpdateAsync(c =>
    {
        var book = Require(c, id);
        CheckVersion(book, command.Version);
        if (command.Position < 0 || command.Position > book.Text.Length || command.Theme is not ("paper" or "sepia" or "dark") || command.FontSize is < 14 or > 32)
            throw new ReaderException("Preferências ou posição inválidas.");
        book.Position = SafeOffset(book.Text, command.Position);
        book.Preferences = new() { Theme = command.Theme, FontSize = command.FontSize, Accessible = command.Accessible };
        book.LastOpenedAt = DateTimeOffset.UtcNow;
        return ++book.Version;
    }, ct);
    public Task<long> SaveAnnotationAsync(Guid id, Annotation annotation, long version, CancellationToken ct) => store.UpdateAsync(c =>
    {
        var book = Require(c, id);
        CheckVersion(book, version);
        if (annotation.Id == Guid.Empty || annotation.Kind is not ("bookmark" or "highlight" or "note") ||
            annotation.Start < 0 || annotation.End < annotation.Start || annotation.End > book.Text.Length ||
            annotation.Note is null || annotation.Note.Length > Limits.MaxNote || annotation.Color is not ("yellow" or "green" or "pink"))
            throw new ReaderException("A marcação contém dados inválidos.");
        annotation.Start = SafeOffset(book.Text, annotation.Start);
        annotation.End = SafeOffset(book.Text, annotation.End);
        var existing = book.Annotations.FindIndex(a => a.Id == annotation.Id);
        if (existing >= 0) book.Annotations[existing] = annotation; else book.Annotations.Add(annotation);
        return ++book.Version;
    }, ct);
    public Task<long> DeleteAnnotationAsync(Guid id, Guid annotationId, long version, CancellationToken ct) => store.UpdateAsync(c =>
    {
        var book = Require(c, id); CheckVersion(book, version);
        book.Annotations.RemoveAll(a => a.Id == annotationId);
        return ++book.Version;
    }, ct);
    public async Task<List<SearchHit>> SearchAsync(Guid id, string query, CancellationToken ct)
    {
        if (string.IsNullOrWhiteSpace(query) || query.Length > 256) throw new ReaderException("Busque entre 1 e 256 caracteres.");
        var book = await GetAsync(id, ct) ?? throw new ReaderException("Obra não encontrada.");
        var hits = new List<SearchHit>();
        // Comparação ordinal mantém o offset no texto original, inclusive para caracteres acentuados.
        for (var start = 0; start < book.Text.Length && hits.Count < 100;)
        {
            var found = book.Text.IndexOf(query, start, StringComparison.OrdinalIgnoreCase);
            if (found < 0) break;
            var left = Math.Max(0, found - 55);
            hits.Add(new(found, book.Text.Substring(left, Math.Min(170, book.Text.Length - left))));
            start = found + query.Length;
        }
        return hits;
    }
    public static string Hash(string text) => Convert.ToHexString(SHA256.HashData(Encoding.UTF8.GetBytes(text)));
    private static Book Require(Catalog c, Guid id) => c.Books.FirstOrDefault(b => b.Id == id) ?? throw new ReaderException("A obra não está mais no acervo.");
    private static void CheckVersion(Book book, long expected) { if (book.Version != expected) throw new VersionConflictException(); }
    private static int SafeOffset(string text, int offset)
    {
        // Evita dividir pares substitutos e sequências combinantes na âncora persistida.
        if (offset == text.Length) return offset;
        var starts = StringInfo.ParseCombiningCharacters(text);
        var index = Array.BinarySearch(starts, offset);
        return index >= 0 ? offset : starts[Math.Max(0, ~index - 1)];
    }
}
