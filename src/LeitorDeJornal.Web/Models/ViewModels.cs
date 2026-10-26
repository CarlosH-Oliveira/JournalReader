using System.ComponentModel.DataAnnotations;
using LeitorDeJornal.Application;
using LeitorDeJornal.Domain;
namespace LeitorDeJornal.Web.Models;
public sealed record LibraryViewModel(List<BookSummary> Books, string? Query, string? Format, string? Sort);
public sealed class ConfirmImportModel
{
    public Guid Token { get; set; }
    [Required(ErrorMessage = "Informe o título."), StringLength(200)]
    public string Title { get; set; } = "";
    public bool Accepted { get; set; }
}
public sealed class AnnotationCommand
{
    public long Version { get; set; }
    [Required] public Annotation Annotation { get; set; } = new();
}
public sealed record DeleteAnnotationCommand(Guid AnnotationId, long Version);
