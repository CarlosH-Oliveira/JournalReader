using LeitorDeJornal.Application;
using LeitorDeJornal.Web.Models;
using Microsoft.AspNetCore.Mvc;
namespace LeitorDeJornal.Web.Controllers;
public sealed class LibraryController(LibraryService library) : Controller
{
    public async Task<IActionResult> Index(string? q, string? format, string? sort, CancellationToken ct) =>
        View(new LibraryViewModel(await library.ListAsync(q, format, sort, ct), q, format, sort));
    [HttpPost]
    public async Task<IActionResult> Delete(Guid id, CancellationToken ct)
    {
        TempData["Message"] = await library.DeleteAsync(id, ct) ? "Obra e anotações removidas do acervo. O arquivo original foi preservado." : "Obra não encontrada.";
        return RedirectToAction(nameof(Index));
    }
    [HttpGet, HttpPost]
    [IgnoreAntiforgeryToken]
    public IActionResult Error() => View();
}
