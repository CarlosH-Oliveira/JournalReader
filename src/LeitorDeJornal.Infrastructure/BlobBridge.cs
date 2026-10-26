using System.Net;
using System.Net.Http.Json;
using System.Text.Json;
using LeitorDeJornal.Application;
using LeitorDeJornal.Domain;
namespace LeitorDeJornal.Infrastructure;

/// <summary>Canal interno ao SDK oficial, disponível apenas na imagem Vercel.</summary>
public sealed class BlobBridge : IDisposable
{
    private readonly HttpClient client;
    public BlobBridge(string url, string secret, Func<string?>? oidcToken = null)
    {
        client = new HttpClient(new OidcHandler(oidcToken)) { BaseAddress = new Uri(url), Timeout = TimeSpan.FromMinutes(4) };
        client.DefaultRequestHeaders.Add("X-Internal-Secret", secret);
    }
    public Task<HttpResponseMessage> ReadAsync(string path, CancellationToken ct = default) =>
        client.GetAsync("/object?path=" + Uri.EscapeDataString(path), HttpCompletionOption.ResponseHeadersRead, ct);
    public async Task<bool> WriteAsync(string path, byte[] bytes, string? etag = null, CancellationToken ct = default)
    {
        using var request = new HttpRequestMessage(HttpMethod.Put, "/object?path=" + Uri.EscapeDataString(path)) { Content = new ByteArrayContent(bytes) };
        if (etag is not null) request.Headers.TryAddWithoutValidation("If-Match", etag);
        using var result = await client.SendAsync(request, ct);
        if (result.StatusCode == HttpStatusCode.PreconditionFailed) return false;
        result.EnsureSuccessStatusCode(); return true;
    }
    public async Task DeleteAsync(string path, CancellationToken ct = default)
    {
        using var result = await client.DeleteAsync("/object?path=" + Uri.EscapeDataString(path), ct);
        result.EnsureSuccessStatusCode();
    }
    public async Task<string> SignAsync(string path, CancellationToken ct)
    {
        using var result = await client.PostAsync("/sign?path=" + Uri.EscapeDataString(path), null, ct);
        result.EnsureSuccessStatusCode();
        var json = await result.Content.ReadFromJsonAsync<JsonElement>(cancellationToken: ct);
        return json.GetProperty("presignedUrl").GetString()!;
    }
    public async Task<string[]> KeysAsync() => await client.GetFromJsonAsync<string[]>("/keys") ?? [];
    public void Dispose() => client.Dispose();
    private sealed class OidcHandler(Func<string?>? provider) : DelegatingHandler(new HttpClientHandler())
    {
        protected override Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, CancellationToken ct)
        {
            var token = provider?.Invoke();
            if (!string.IsNullOrWhiteSpace(token)) request.Headers.TryAddWithoutValidation("x-vercel-oidc-token", token);
            return base.SendAsync(request, ct);
        }
    }
}

/// <summary>Acervo privado com controle otimista via ETag entre instâncias.</summary>
public sealed class BlobCatalogStore(BlobBridge bridge) : ICatalogStore
{
    private const string Path = "state/catalog.json";
    private async Task<(Catalog Catalog, string? Etag)> Read(CancellationToken ct)
    {
        using var response = await bridge.ReadAsync(Path, ct);
        if (response.StatusCode == HttpStatusCode.NotFound) return (new Catalog(), null);
        response.EnsureSuccessStatusCode();
        var catalog = await response.Content.ReadFromJsonAsync<Catalog>(cancellationToken: ct) ?? throw new InvalidDataException("Acervo vazio.");
        return (catalog, response.Headers.ETag?.ToString() ?? throw new InvalidDataException("ETag ausente."));
    }
    public async Task<T> ReadAsync<T>(Func<Catalog, T> query, CancellationToken ct = default) => query((await Read(ct)).Catalog);
    public async Task<T> UpdateAsync<T>(Func<Catalog, T> command, CancellationToken ct = default)
    {
        var (catalog, etag) = await Read(ct);
        var result = command(catalog);
        if (!await bridge.WriteAsync(Path, JsonSerializer.SerializeToUtf8Bytes(catalog), etag, ct))
            throw new ReaderException("O acervo foi alterado em outra aba. Recarregue e tente novamente.");
        return result;
    }
}

/// <summary>Prévias privadas compartilhadas, com prazo validado a cada leitura.</summary>
public sealed class BlobDraftStore(BlobBridge bridge) : IDraftStore
{
    private static string Path(string owner, Guid token) => $"drafts/{owner}/{token:N}.json";
    public void Put(string owner, ImportDraft draft) => bridge.WriteAsync(Path(owner, draft.Token), JsonSerializer.SerializeToUtf8Bytes(draft)).GetAwaiter().GetResult();
    public ImportDraft? Get(string owner, Guid token)
    {
        using var response = bridge.ReadAsync(Path(owner, token)).GetAwaiter().GetResult();
        if (response.StatusCode == HttpStatusCode.NotFound) return null;
        response.EnsureSuccessStatusCode();
        var draft = response.Content.ReadFromJsonAsync<ImportDraft>().GetAwaiter().GetResult();
        if (draft?.ExpiresAt <= DateTimeOffset.UtcNow) { Remove(owner, token); return null; }
        return draft;
    }
    public void Remove(string owner, Guid token) => bridge.DeleteAsync(Path(owner, token)).GetAwaiter().GetResult();
}
