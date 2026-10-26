using System.Text.Json;
using LeitorDeJornal.Domain;
namespace LeitorDeJornal.Application;

public sealed record BackupEnvelope(int SchemaVersion, Guid SnapshotId, DateTimeOffset CreatedAt, string Sha256, string Payload);
/// <summary>Backup lógico versionado. O hash detecta corrupção; não autentica a origem.</summary>
public sealed class BackupService(ICatalogStore store)
{
    public async Task<byte[]> ExportAsync(CancellationToken ct)
    {
        var payload = await store.ReadAsync(c => JsonSerializer.Serialize(c), ct);
        return JsonSerializer.SerializeToUtf8Bytes(new BackupEnvelope(1, Guid.NewGuid(), DateTimeOffset.UtcNow, LibraryService.Hash(payload), payload));
    }
    public static Catalog Validate(byte[] bytes)
    {
        try
        {
            var envelope = JsonSerializer.Deserialize<BackupEnvelope>(bytes) ?? throw new ReaderException("Backup vazio.");
            if (envelope.SchemaVersion != 1 || envelope.Payload is null || LibraryService.Hash(envelope.Payload) != envelope.Sha256)
                throw new ReaderException("Versão incompatível ou hash do backup inválido. Nenhum dado foi alterado.");
            var catalog = JsonSerializer.Deserialize<Catalog>(envelope.Payload) ?? throw new ReaderException("Acervo inválido.");
            ValidateCatalog(catalog);
            return catalog;
        }
        catch (Exception ex) when (ex is JsonException or ArgumentException or NullReferenceException)
        { throw new ReaderException("O arquivo não é um backup válido do Leitor de Jornal."); }
    }
    public Task<int> RestoreAsync(byte[] bytes, CancellationToken ct)
    {
        var restored = Validate(bytes); // Validação integral ocorre antes de adquirir o commit do acervo ativo.
        return store.UpdateAsync(c => { c.Books = restored.Books; return c.Books.Count; }, ct);
    }
    public static void ValidateCatalog(Catalog c)
    {
        if (c.SchemaVersion != 1 || c.Books is null || c.Books.Count > Limits.MaxBooks ||
            c.Books.Any(b => b is null) || c.Books.Select(b => b.Id).Distinct().Count() != c.Books.Count)
            throw new ReaderException("Estrutura do acervo inválida.");
        foreach (var b in c.Books)
        {
            if (b.Id == Guid.Empty || string.IsNullOrWhiteSpace(b.Title) || b.Title.Length > 200 ||
                b.Text is null || string.IsNullOrWhiteSpace(b.Text) || b.Text.Length > Limits.MaxCharacters ||
                b.Format is not ("TXT" or "PDF" or "EPUB") || b.Revision != LibraryService.Hash(b.Text) ||
                b.Position < 0 || b.Position > b.Text.Length || b.Version < 0 || b.Preferences is null ||
                b.Preferences.Theme is not ("paper" or "sepia" or "dark") || b.Preferences.FontSize is < 14 or > 32 ||
                b.Contents is null || b.Annotations is null || b.Annotations.Any(a => a is null) ||
                b.Annotations.Select(a => a.Id).Distinct().Count() != b.Annotations.Count)
                throw new ReaderException("Uma obra contém texto, hash ou preferências inválidas.");
            foreach (var h in b.Contents)
                if (h is null || h.Title is null || h.Title.Length > 500 || h.Offset < 0 || h.Offset > b.Text.Length)
                    throw new ReaderException("Sumário inválido.");
            foreach (var a in b.Annotations)
                if (a.Id == Guid.Empty || a.Start < 0 || a.End < a.Start || a.End > b.Text.Length ||
                    a.Note is null || a.Note.Length > Limits.MaxNote || a.Kind is not ("bookmark" or "highlight" or "note") ||
                    a.Color is not ("yellow" or "green" or "pink"))
                    throw new ReaderException("Uma anotação contém dados inválidos.");
        }
    }
}
