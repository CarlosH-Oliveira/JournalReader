using System.IO.Compression;
using System.Text;
using System.Xml;
using System.Xml.Linq;
using AngleSharp.Html.Parser;
using AngleSharp.Dom;
using System.Text.RegularExpressions;
using LeitorDeJornal.Application;
using LeitorDeJornal.Domain;
using UglyToad.PdfPig;
using UglyToad.PdfPig.DocumentLayoutAnalysis.TextExtractor;
namespace LeitorDeJornal.Infrastructure;

/// <summary>Extrai somente texto: nenhum HTML, script ou recurso remoto do arquivo chega à view.</summary>
public sealed class DocumentExtractor : IDocumentExtractor
{
    public async Task<ExtractedDocument> ExtractAsync(Stream input, string extension, CancellationToken ct)
    {
        using var buffer = new MemoryStream();
        var chunk = new byte[81920];
        int read;
        while ((read = await input.ReadAsync(chunk, ct)) > 0)
        {
            if (buffer.Length + read > Limits.MaxUpload) throw new ReaderException("O arquivo excede 50 MiB.");
            await buffer.WriteAsync(chunk.AsMemory(0, read), ct);
        }
        var bytes = buffer.ToArray();
        try
        {
            return extension switch
            {
                ".txt" => new(DecodeText(bytes), [], []),
                ".pdf" => ExtractPdf(bytes, ct),
                ".epub" => ExtractEpub(bytes, ct),
                _ => throw new ReaderException("Formato não suportado.")
            };
        }
        catch (ReaderException) { throw; }
        catch (OperationCanceledException) { throw; }
        catch (Exception ex) when (ex is not OutOfMemoryException)
        { throw new ReaderException("Não foi possível extrair o arquivo. Verifique se está íntegro, sem senha/DRM e em formato suportado."); }
    }
    private static string DecodeText(byte[] bytes)
    {
        Encoding encoding = new UTF8Encoding(false, true);
        var skip = 0;
        if (bytes.AsSpan().StartsWith(new byte[] { 0xEF, 0xBB, 0xBF })) skip = 3;
        else if (bytes.AsSpan().StartsWith(new byte[] { 0xFF, 0xFE })) { encoding = new UnicodeEncoding(false, false, true); skip = 2; }
        else if (bytes.AsSpan().StartsWith(new byte[] { 0xFE, 0xFF })) { encoding = new UnicodeEncoding(true, false, true); skip = 2; }
        try
        {
            var text = encoding.GetString(bytes, skip, bytes.Length - skip).Replace("\r\n", "\n").Replace('\r', '\n');
            if (text.Contains('\0')) throw new ReaderException("O TXT contém bytes nulos. Use UTF-8 ou UTF-16 com BOM.");
            return text;
        }
        catch (DecoderFallbackException) { throw new ReaderException("Codificação inválida. Salve o TXT como UTF-8 ou UTF-16 com BOM."); }
    }
    private static ExtractedDocument ExtractPdf(byte[] bytes, CancellationToken ct)
    {
        using var pdf = PdfDocument.Open(bytes);
        if (pdf.NumberOfPages > 2000) throw new ReaderException("O PDF excede 2.000 páginas.");
        var text = new StringBuilder(); var headings = new List<Heading>();
        var warnings = new List<string> { "PDF: confira a ordem da extração na prévia. Colunas, fórmulas e tabelas podem ser linearizadas incorretamente; o layout original não é preservado." };
        var empty = 0;
        for (var i = 1; i <= pdf.NumberOfPages; i++)
        {
            ct.ThrowIfCancellationRequested();
            var page = ContentOrderTextExtractor.GetText(pdf.GetPage(i)).Replace("\r\n", "\n").Replace('\r', '\n');
            if (string.IsNullOrWhiteSpace(page)) { empty++; continue; }
            if (text.Length > 0) text.Append("\n\n");
            headings.Add(new($"Página de origem {i}", text.Length));
            text.Append(page);
            if (text.Length > Limits.MaxCharacters) throw new ReaderException("Texto acima do limite de 5 milhões de caracteres.");
        }
        if (empty > 0) warnings.Add($"{empty} página(s) sem texto extraível não foram incluídas. Não há OCR; confira se faltam trechos antes de aceitar.");
        return new(text.ToString(), headings, warnings);
    }
    private static XDocument ReadXml(ZipArchiveEntry entry)
    {
        using var stream = entry.Open();
        using var reader = XmlReader.Create(stream, new XmlReaderSettings { DtdProcessing = DtdProcessing.Prohibit,
            XmlResolver = null, MaxCharactersInDocument = 20_000_000 });
        return XDocument.Load(reader);
    }
    private static string Resolve(string origin, string relative)
    {
        relative = Uri.UnescapeDataString(relative.Split('#')[0]);
        if (relative.Contains(':') || relative.Contains('\\') || relative.StartsWith('/')) throw new ReaderException("EPUB contém referência externa ou caminho inválido.");
        var parts = new List<string>();
        var prefix = origin.Contains('/') ? origin[..(origin.LastIndexOf('/') + 1)] : "";
        foreach (var p in (prefix + relative).Split('/'))
        {
            if (p is "" or ".") continue;
            if (p == "..") { if (parts.Count == 0) throw new ReaderException("Caminho EPUB fora do pacote."); parts.RemoveAt(parts.Count - 1); }
            else parts.Add(p);
        }
        return string.Join('/', parts);
    }
    private static ExtractedDocument ExtractEpub(byte[] bytes, CancellationToken ct)
    {
        using var zip = new ZipArchive(new MemoryStream(bytes), ZipArchiveMode.Read);
        if (zip.Entries.Count > 10000) throw new ReaderException("EPUB excede 10.000 entradas.");
        long total = 0;
        var entries = new Dictionary<string, ZipArchiveEntry>(StringComparer.OrdinalIgnoreCase);
        foreach (var entry in zip.Entries)
        {
            var name = entry.FullName.Normalize(NormalizationForm.FormC);
            if (name.StartsWith('/') || name.Contains('\\') || name.Contains(':') || name.Split('/').Contains("..") ||
                ((entry.ExternalAttributes >> 16) & 0xF000) == 0xA000 || !entries.TryAdd(name, entry))
                throw new ReaderException("EPUB contém caminhos inseguros ou entradas duplicadas.");
            total += entry.Length;
            if (total > 200L * 1024 * 1024 || entry.Length > 20L * 1024 * 1024 ||
                (entry.Length > 0 && (entry.CompressedLength == 0 || entry.Length / (double)entry.CompressedLength > 100)))
                throw new ReaderException("EPUB excede os limites de descompactação (200 MiB totais, 20 MiB por entrada, razão 100:1).");
        }
        ZipArchiveEntry Entry(string name) => entries.TryGetValue(name.Normalize(NormalizationForm.FormC), out var e) ? e : throw new ReaderException("EPUB incompleto: recurso ausente.");
        if (entries.ContainsKey("META-INF/encryption.xml")) throw new ReaderException("EPUB com recursos criptografados não é suportado nesta versão.");
        var container = ReadXml(Entry("META-INF/container.xml"));
        var packagePath = container.Descendants().FirstOrDefault(x => x.Name.LocalName == "rootfile")?.Attribute("full-path")?.Value
            ?? throw new ReaderException("EPUB sem package válido.");
        packagePath = Resolve("", packagePath);
        var package = ReadXml(Entry(packagePath));
        if (package.Descendants().Any(x => x.Name.LocalName == "meta" && x.Attribute("property")?.Value == "rendition:layout" && x.Value.Trim() == "pre-paginated"))
            throw new ReaderException("EPUB de layout fixo não é suportado. Use um EPUB refluível.");
        var manifest = package.Descendants().Where(x => x.Name.LocalName == "item")
            .ToDictionary(x => x.Attribute("id")!.Value, x => x);
        var spine = package.Descendants().Where(x => x.Name.LocalName == "itemref").ToList();
        if (spine.Count == 0) throw new ReaderException("EPUB sem ordem de leitura (spine).");
        var parser = new HtmlParser(); var text = new StringBuilder(); var headings = new List<Heading>();
        var warnings = new List<string> { "EPUB convertido em texto na ordem do spine. Estilos, imagens e links ativos não são executados; o sumário é derivado dos títulos e capítulos." };
        foreach (var itemref in spine)
        {
            ct.ThrowIfCancellationRequested();
            if (!manifest.TryGetValue(itemref.Attribute("idref")?.Value ?? "", out var item)) throw new ReaderException("Referência de capítulo EPUB inválida.");
            if ((item.Attribute("properties")?.Value ?? "").Contains("rendition:layout-pre-paginated")) throw new ReaderException("Capítulo de layout fixo não suportado.");
            if (item.Attribute("media-type")?.Value is not ("application/xhtml+xml" or "text/html")) throw new ReaderException("Capítulo EPUB não textual não suportado.");
            var name = Resolve(packagePath, item.Attribute("href")?.Value ?? "");
            using var stream = Entry(name).Open();
            using var sr = new StreamReader(stream, Encoding.UTF8, detectEncodingFromByteOrderMarks: true);
            using var document = parser.ParseDocument(sr.ReadToEnd());
            foreach (var unsafeNode in document.QuerySelectorAll("script,style,iframe,object,svg,nav,head")) unsafeNode.Remove();
            foreach (var img in document.QuerySelectorAll("img"))
            {
                var alt = img.GetAttribute("alt");
                img.Replace(document.CreateTextNode(string.IsNullOrWhiteSpace(alt) ? "[Imagem sem descrição]" : $"[Imagem: {alt}]"));
            }
            if (document.QuerySelector("table") is not null && !warnings.Contains("Tabelas foram linearizadas; confira sua ordem na prévia.")) warnings.Add("Tabelas foram linearizadas; confira sua ordem na prévia.");
            var body = document.Body;
            if (body is null) continue;

            // Percorrer todos os nós preserva também texto diretamente em <div> e notas de rodapé.
            // Não selecionar apenas <p>: isso omitiria textos válidos de EPUBs menos estruturados.
            var chapter = new StringBuilder();
            var chapterHeadings = new List<Heading>();
            var blockTags = new HashSet<string> { "P", "DIV", "SECTION", "ARTICLE", "ASIDE", "H1", "H2", "H3", "H4", "H5", "H6", "LI", "PRE", "BLOCKQUOTE", "TR", "FIGCAPTION" };
            void Break()
            {
                while (chapter.Length > 0 && chapter[^1] == ' ') chapter.Length--;
                if (chapter.Length > 0 && chapter[^1] != '\n') chapter.Append("\n\n");
            }
            void Visit(INode node, int depth, bool preformatted = false)
            {
                if (depth > 128) throw new ReaderException("EPUB excede 128 níveis de aninhamento.");
                ct.ThrowIfCancellationRequested();
                if (node is IText textNode)
                {
                    var value = preformatted ? textNode.Data : Regex.Replace(textNode.Data, @"[\t\r\n ]+", " ");
                    if (!preformatted && (chapter.Length == 0 || chapter[^1] is '\n' or ' ')) value = value.TrimStart(' ');
                    chapter.Append(value);
                }
                else if (node is IElement element)
                {
                    var block = blockTags.Contains(element.TagName);
                    if (block) Break();
                    if (element.TagName is "H1" or "H2" or "H3" or "H4" or "H5" or "H6")
                    {
                        var title = element.TextContent.Trim();
                        if (title.Length > 0) chapterHeadings.Add(new(title[..Math.Min(title.Length, 500)], chapter.Length));
                    }
                    if (element.TagName == "BR") chapter.Append('\n');
                    foreach (var child in element.ChildNodes) Visit(child, depth + 1, preformatted || element.TagName == "PRE");
                    if (element.TagName is "TD" or "TH") chapter.Append(' ');
                    if (block) Break();
                }
                if (chapter.Length + text.Length > Limits.MaxCharacters) throw new ReaderException("Texto acima do limite de 5 milhões de caracteres.");
            }
            Visit(body, 0);
            var chapterText = chapter.ToString().TrimEnd('\n', ' ');
            if (string.IsNullOrWhiteSpace(chapterText)) continue;
            if (text.Length > 0) text.Append("\n\n");
            var chapterStart = text.Length;
            text.Append(chapterText);
            if (chapterHeadings.Count == 0) headings.Add(new($"Capítulo {spine.IndexOf(itemref) + 1}", chapterStart));
            else headings.AddRange(chapterHeadings.Where(h => h.Offset < chapterText.Length).Select(h => new Heading(h.Title, chapterStart + h.Offset)));

        }
        return new(text.ToString(), headings, warnings);
    }
}
