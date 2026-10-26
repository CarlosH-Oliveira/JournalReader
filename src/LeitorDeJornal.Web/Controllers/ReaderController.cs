using LeitorDeJornal.Application;
using LeitorDeJornal.Domain;
using LeitorDeJornal.Web.Models;
using Microsoft.AspNetCore.Mvc;
namespace LeitorDeJornal.Web.Controllers;
public sealed class ReaderController(LibraryService library) : Controller
{
    public async Task<IActionResult> Index(Guid id, CancellationToken ct)
    {
        var book = await library.GetAsync(id, ct);
        return book is null ? NotFound("Obra não encontrada. Retorne ao acervo.") : View(book);
    }
    [HttpGet]
    public async Task<IActionResult> Data(Guid id, CancellationToken ct)
    {
        var book = await library.GetAsync(id, ct);
        return book is null ? NotFound() : Json(book);
    }
    [HttpGet]
    public async Task<IActionResult> Search(Guid id, string q, CancellationToken ct)
    {
        try { return Json(await library.SearchAsync(id, q, ct)); }
        catch (ReaderException ex) { return BadRequest(new { error = ex.Message }); }
    }
    [HttpPost]
    public Task<IActionResult> Progress(Guid id, [FromBody] ProgressCommand command, CancellationToken ct) =>
        Execute(() => library.SaveProgressAsync(id, command, ct));
    [HttpPost]
    public Task<IActionResult> Annotate(Guid id, [FromBody] AnnotationCommand command, CancellationToken ct) =>
        Execute(() => library.SaveAnnotationAsync(id, command.Annotation, command.Version, ct));
    [HttpPost]
    public Task<IActionResult> RemoveAnnotation(Guid id, [FromBody] DeleteAnnotationCommand command, CancellationToken ct) =>
        Execute(() => library.DeleteAnnotationAsync(id, command.AnnotationId, command.Version, ct));
    private async Task<IActionResult> Execute(Func<Task<long>> action)
    {
        if (!ModelState.IsValid) return BadRequest(new { error = "Comando inválido." });
        try { return Json(new { version = await action() }); }
        catch (VersionConflictException ex) { return Conflict(new { error = ex.Message }); }
        catch (ReaderException ex) { return BadRequest(new { error = ex.Message }); }
    }
}
