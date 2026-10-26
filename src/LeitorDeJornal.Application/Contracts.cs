using LeitorDeJornal.Domain;
namespace LeitorDeJornal.Application;

/// <summary>A aplicação depende desta porta; a infraestrutura decide onde e como persistir.</summary>
public interface ICatalogStore
{
    Task<T> ReadAsync<T>(Func<Catalog, T> query, CancellationToken ct = default);
    Task<T> UpdateAsync<T>(Func<Catalog, T> command, CancellationToken ct = default);
}
public sealed record ExtractedDocument(string Text, List<Heading> Contents, List<string> Warnings);
public interface IDocumentExtractor
{
    Task<ExtractedDocument> ExtractAsync(Stream input, string extension, CancellationToken ct);
}
public sealed record ImportDraft(Guid Token, string Title, string Format, string Text,
    List<Heading> Contents, List<string> Warnings, DateTimeOffset ExpiresAt);
public interface IDraftStore
{
    void Put(string owner, ImportDraft draft);
    ImportDraft? Get(string owner, Guid token);
    void Remove(string owner, Guid token);
}
public sealed record BookSummary(Guid Id, string Title, string Format, int Characters, int Position,
    DateTimeOffset ImportedAt, DateTimeOffset? LastOpenedAt, int Annotations);
public sealed record SearchHit(int Offset, string Excerpt);
public sealed record ProgressCommand(int Position, string Theme, int FontSize, bool Accessible, long Version);
