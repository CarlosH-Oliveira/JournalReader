using LeitorDeJornal.Application;
using LeitorDeJornal.Domain;
using Microsoft.AspNetCore.Mvc;
namespace LeitorDeJornal.Web.Controllers;
public sealed class BackupController(BackupService backups) : Controller
{
    public IActionResult Index() => View();
    // Exportar não altera estado; download exige uma ação explícita pelo formulário.
    [HttpPost]
    public async Task<IActionResult> Export(CancellationToken ct) =>
        File(await backups.ExportAsync(ct), "application/json", $"leitor-de-jornal-{DateTime.UtcNow:yyyyMMdd-HHmmss}.json");
    [HttpPost, RequestSizeLimit(210L * 1024 * 1024)]
    public async Task<IActionResult> Restore(IFormFile? file, bool confirmed, CancellationToken ct)
    {
        if (!confirmed || file is null || file.Length == 0 || file.Length > 200L * 1024 * 1024)
        { ModelState.AddModelError("", "Selecione um backup de até 200 MiB e confirme a substituição do acervo."); return View("Index"); }
        try
        {
            using var memory = new MemoryStream();
            await file.CopyToAsync(memory, ct);
            var count = await backups.RestoreAsync(memory.ToArray(), ct);
            TempData["Message"] = $"Backup restaurado. {count} obra(s) no acervo.";
            return RedirectToAction("Index", "Library");
        }
        catch (ReaderException ex) { ModelState.AddModelError("", ex.Message); return View("Index"); }
    }
}
