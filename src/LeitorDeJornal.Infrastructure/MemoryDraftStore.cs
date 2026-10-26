using System.Collections.Concurrent;
using LeitorDeJornal.Application;
using LeitorDeJornal.Domain;
namespace LeitorDeJornal.Infrastructure;

/// <summary>Prévia temporária vinculada à sessão. Reiniciar o servidor descarta importações não confirmadas.</summary>
public sealed class MemoryDraftStore : IDraftStore
{
    private readonly ConcurrentDictionary<string, ImportDraft> items = new();
    public void Put(string owner, ImportDraft draft)
    {
        foreach (var pair in items.Where(x => x.Value.ExpiresAt <= DateTimeOffset.UtcNow).ToArray()) items.TryRemove(pair.Key, out _);
        if (items.Count >= 10) throw new ReaderException("Há muitas prévias abertas. Cancele uma ou aguarde sua expiração.");
        // Uma única prévia por sessão limita retenção de documentos grandes.
        items[owner] = draft;
    }
    public ImportDraft? Get(string owner, Guid token) => items.TryGetValue(owner, out var draft) && draft.Token == token &&
        draft.ExpiresAt > DateTimeOffset.UtcNow ? draft : null;
    public void Remove(string owner, Guid token)
    {
        if (Get(owner, token) is not null) items.TryRemove(owner, out _);
    }
}
