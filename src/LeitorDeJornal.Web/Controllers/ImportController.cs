using Microsoft.AspNetCore.DataProtection;
using LeitorDeJornal.Infrastructure;
using System.Text.RegularExpressions;
using LeitorDeJornal.Application;
using LeitorDeJornal.Domain;
using LeitorDeJornal.Web.Models;
using Microsoft.AspNetCore.Mvc;
namespace LeitorDeJornal.Web.Controllers;
public sealed class ImportController(LibraryService library, IDataProtectionProvider protection, IConfiguration configuration, IServiceProvider services) : Controller
{
    // A sessão vincula o token de prévia ao navegador que enviou o arquivo; não autentica usuários.
    private string Owner()
    {
        var protector = protection.CreateProtector("JournalReader.ImportOwner.v1");
        string? owner = null;
        if (Request.Cookies.TryGetValue("JournalReader.Owner", out var cookie))
        {
            try { owner = protector.Unprotect(cookie); } catch (System.Security.Cryptography.CryptographicException) { }
        }
        if (owner is null || !Regex.IsMatch(owner, "^[a-f0-9]{32}$"))
        {
            owner = Guid.NewGuid().ToString("N");
            Response.Cookies.Append("JournalReader.Owner", protector.Protect(owner), new CookieOptions
            { HttpOnly = true, Secure = !HttpContext.Request.Host.Host.Equals("localhost"), SameSite = SameSiteMode.Strict, MaxAge = TimeSpan.FromHours(8), IsEssential = true });
        }
        return owner;
    }
    public IActionResult Index() { Owner(); ViewData["DirectUpload"] = configuration["BlobBridge:Url"] is not null; return View(); }
    [HttpPost, RequestSizeLimit(16_384)]
    public async Task<IActionResult> PrepareBlob(string filename, long size, CancellationToken ct)
    {
        var extension = Path.GetExtension(filename ?? "").ToLowerInvariant();
        if (size <= 0 || size > Limits.MaxUpload || extension is not (".epub" or ".pdf" or ".txt"))
            return BadRequest(new { error = "Selecione TXT, PDF ou EPUB de até 50 MiB." });
        var bridge = services.GetService<BlobBridge>();
        if (bridge is null) return BadRequest(new { error = "Upload direto indisponível." });
        var path = $"uploads/{Owner()}/{Guid.NewGuid():N}{extension}";
        var ticket = await bridge.SignAsync(path, ct);
        return Json(new { path, uploadUrl = ticket.GetProperty("presignedUrl").GetString(), headers = ticket.GetProperty("headers") });
    }
    [HttpPost, RequestSizeLimit(16_384)]
    public async Task<IActionResult> FromBlob(string path, string filename, CancellationToken ct)
    {
        var bridge = services.GetService<BlobBridge>();
        var extension = Path.GetExtension(filename ?? "").ToLowerInvariant();
        if (bridge is null || path is null || !Regex.IsMatch(path, $"^uploads/{Owner()}/[a-f0-9]{{32}}\\.(epub|pdf|txt)$") || Path.GetExtension(path) != extension)
            return BadRequest("Arquivo de importação inválido.");
        try
        {
            using var result = await bridge.ReadAsync(path, ct);
            if (!result.IsSuccessStatusCode) throw new ReaderException("O envio não foi concluído. Selecione o arquivo novamente.");
            if (result.Content.Headers.ContentLength is not > 0 or > Limits.MaxUpload) throw new ReaderException("Arquivo vazio ou maior que 50 MiB.");
            await using var stream = await result.Content.ReadAsStreamAsync(ct);
            var draft = await library.PreviewAsync(Owner(), filename!, stream, ct);
            return RedirectToAction(nameof(Preview), new { token = draft.Token });
        }
        catch (ReaderException ex) { TempData["Message"] = ex.Message; return RedirectToAction(nameof(Index)); }
        finally { await bridge.DeleteAsync(path, CancellationToken.None); }
    }
    [HttpPost, RequestSizeLimit(55L * 1024 * 1024)]
    public async Task<IActionResult> Upload(IFormFile? file, CancellationToken ct)
    {
        if (file is null || file.Length == 0 || file.Length > Limits.MaxUpload)
        { ModelState.AddModelError("", "Selecione um arquivo de até 50 MiB."); return View("Index"); }
        try
        {
            await using var stream = file.OpenReadStream();
            var draft = await library.PreviewAsync(Owner(), file.FileName, stream, ct);
            return RedirectToAction(nameof(Preview), new { token = draft.Token });
        }
        catch (ReaderException ex) { ModelState.AddModelError("", ex.Message); return View("Index"); }
    }
    public IActionResult Preview(Guid token)
    {
        try { return View(library.Draft(Owner(), token)); }
        catch (ReaderException ex) { TempData["Message"] = ex.Message; return RedirectToAction(nameof(Index)); }
    }
    [HttpPost]
    public async Task<IActionResult> Confirm(ConfirmImportModel model, CancellationToken ct)
    {
        try
        {
            if (!ModelState.IsValid) return View("Preview", library.Draft(Owner(), model.Token));
            var id = await library.ConfirmAsync(Owner(), model.Token, model.Title, model.Accepted, ct);
            return RedirectToAction("Index", "Reader", new { id });
        }
        catch (ReaderException ex)
        {
            TempData["Message"] = ex.Message;
            return RedirectToAction(nameof(Preview), new { token = model.Token });
        }
    }
    [HttpPost]
    public IActionResult Cancel(Guid token) { library.Cancel(Owner(), token); return RedirectToAction("Index", "Library"); }
}
