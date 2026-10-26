using System.Text;
using System.Xml.Linq;
using LeitorDeJornal.Infrastructure;
using Microsoft.AspNetCore.DataProtection.Repositories;
namespace LeitorDeJornal.Web;

// Cookies e antifalsificação permanecem válidos entre reinícios e instâncias.
public sealed class BlobKeyRepository(BlobBridge bridge) : IXmlRepository
{
    public IReadOnlyCollection<XElement> GetAllElements() => bridge.KeysAsync().GetAwaiter().GetResult().Select(XElement.Parse).ToArray();
    public void StoreElement(XElement element, string friendlyName)
    {
        if (!bridge.WriteAsync($"keys/{Guid.NewGuid():N}.xml", Encoding.UTF8.GetBytes(element.ToString(SaveOptions.DisableFormatting))).GetAwaiter().GetResult())
            throw new InvalidOperationException("Não foi possível persistir a chave.");
    }
}
