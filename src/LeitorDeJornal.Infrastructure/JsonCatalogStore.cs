using System.Text.Json;
using LeitorDeJornal.Application;
using LeitorDeJornal.Domain;
namespace LeitorDeJornal.Infrastructure;

/// <summary>
/// Adaptador de arquivo JSON para instalação pessoal de instância única.
/// O lock cobre leitura + comando + commit, evitando atualizações perdidas entre requisições.
/// Para múltiplas instâncias substitua esta implementação por banco transacional.
/// </summary>
public sealed class JsonCatalogStore : ICatalogStore
{
    private readonly string path;
    private readonly SemaphoreSlim gate = new(1, 1);
    public JsonCatalogStore(string directory)
    {
        Directory.CreateDirectory(directory);
        path = Path.Combine(directory, "catalog.json");
        // Não sobrescrever silenciosamente um acervo corrompido durante a inicialização.
        if (File.Exists(path)) BackupService.ValidateCatalog(Read());
    }
    private Catalog Read() => File.Exists(path)
        ? JsonSerializer.Deserialize<Catalog>(File.ReadAllBytes(path)) ?? throw new InvalidDataException("Acervo vazio.")
        : new Catalog();
    public async Task<T> ReadAsync<T>(Func<Catalog, T> query, CancellationToken ct = default)
    {
        await gate.WaitAsync(ct);
        try { return query(Read()); } finally { gate.Release(); }
    }
    public async Task<T> UpdateAsync<T>(Func<Catalog, T> command, CancellationToken ct = default)
    {
        await gate.WaitAsync(ct);
        var temporary = path + ".tmp";
        try
        {
            var catalog = Read();
            var result = command(catalog);
            var bytes = JsonSerializer.SerializeToUtf8Bytes(catalog);
            await using (var stream = new FileStream(temporary, FileMode.Create, FileAccess.Write, FileShare.None))
            {
                await stream.WriteAsync(bytes, ct);
                stream.Flush(flushToDisk: true);
            }
            // Renomeação no mesmo volume: leitores nunca observam JSON parcialmente escrito.
            // A geração anterior fica disponível para recuperação manual; não substitui backup externo.
            if (File.Exists(path)) File.Copy(path, path + ".previous", overwrite: true);
            File.Move(temporary, path, overwrite: true);
            return result;
        }
        finally
        {
            try { if (File.Exists(temporary)) File.Delete(temporary); }
            finally { gate.Release(); }
        }
    }
}
