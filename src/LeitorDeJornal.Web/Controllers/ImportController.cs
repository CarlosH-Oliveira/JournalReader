using LeitorDeJornal.Application;
using LeitorDeJornal.Domain;
using LeitorDeJornal.Web.Models;
using Microsoft.AspNetCore.Mvc;
namespace LeitorDeJornal.Web.Controllers;
public sealed class ImportController(LibraryService library) : Controller
{
    // A sessão vincula o token de prévia ao navegador que enviou o arquivo; não autentica usuários.
    private string Owner()
    {
        var owner = HttpContext.Session.GetString("owner");
        if (owner is null) { owner = Guid.NewGuid().ToString("N"); HttpContext.Session.SetString("owner", owner); }
        return owner;
    }
    public IActionResult Index() { Owner(); return View(); }
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
