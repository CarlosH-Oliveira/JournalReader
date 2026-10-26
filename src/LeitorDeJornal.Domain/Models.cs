namespace LeitorDeJornal.Domain;

/// <summary>Limites compartilhados por importação, comandos e restauração.</summary>
public static class Limits
{
    public const int MaxCharacters = 5_000_000;
    public const int MaxBooks = 1_000;
    public const long MaxUpload = 50L * 1024 * 1024;
    public const int MaxNote = 10_000;
}

/// <summary>Offsets sempre representam unidades UTF-16 no texto canônico, nunca páginas físicas.</summary>
public sealed class Book
{
    public Guid Id { get; set; } = Guid.NewGuid();
    public string Title { get; set; } = "";
    public string Format { get; set; } = "TXT";
    public string Text { get; set; } = "";
    public string Revision { get; set; } = "";
    public DateTimeOffset ImportedAt { get; set; } = DateTimeOffset.UtcNow;
    public DateTimeOffset? LastOpenedAt { get; set; }
    public int Position { get; set; }
    public long Version { get; set; }
    public ReaderPreferences Preferences { get; set; } = new();
    public List<Heading> Contents { get; set; } = [];
    public List<Annotation> Annotations { get; set; } = [];
}
public sealed record Heading(string Title, int Offset);
public sealed class ReaderPreferences
{
    public string Theme { get; set; } = "paper";
    public int FontSize { get; set; } = 18;
    public bool Accessible { get; set; }
}
public sealed class Annotation
{
    // O ID é fornecido pelo cliente: repetir a mesma criação não duplica a marcação.
    public Guid Id { get; set; } = Guid.NewGuid();
    public string Kind { get; set; } = "bookmark";
    public int Start { get; set; }
    public int End { get; set; }
    public string Note { get; set; } = "";
    public string Color { get; set; } = "yellow";
}
public sealed class Catalog
{
    public int SchemaVersion { get; set; } = 1;
    public List<Book> Books { get; set; } = [];
}
/// <summary>Erro esperado que pode ser apresentado ao leitor sem detalhes de infraestrutura.</summary>
public sealed class ReaderException(string message) : Exception(message);
public sealed class VersionConflictException() : Exception("A obra foi alterada em outra aba. Recarregue antes de salvar.");
