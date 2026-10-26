using LeitorDeJornal.Web;
using Microsoft.AspNetCore.DataProtection;
using Microsoft.AspNetCore.DataProtection.KeyManagement;
using System.Globalization;
using LeitorDeJornal.Application;
using LeitorDeJornal.Infrastructure;
using Microsoft.AspNetCore.Http.Features;
using Microsoft.AspNetCore.Mvc;

var builder = WebApplication.CreateBuilder(args);
CultureInfo.DefaultThreadCurrentCulture = CultureInfo.GetCultureInfo("pt-BR");
CultureInfo.DefaultThreadCurrentUICulture = CultureInfo.GetCultureInfo("pt-BR");
builder.Services.AddControllersWithViews(options => options.Filters.Add(new AutoValidateAntiforgeryTokenAttribute()));
var blobEnabled = !string.IsNullOrWhiteSpace(builder.Configuration["BlobBridge:Url"]);
if (blobEnabled)
{
    IHttpContextAccessor accessor = new HttpContextAccessor();
    builder.Services.AddSingleton(accessor);
    var bridge = new BlobBridge(builder.Configuration["BlobBridge:Url"]!, builder.Configuration["BlobBridge:Secret"]!,
        () => accessor.HttpContext?.Request.Headers["x-vercel-oidc-token"].ToString());
    builder.Services.AddSingleton(bridge);
    builder.Services.AddDataProtection().SetApplicationName("JournalReader");
    builder.Services.Configure<KeyManagementOptions>(o => o.XmlRepository = new BlobKeyRepository(bridge));
}
else builder.Services.AddDataProtection();
builder.Services.Configure<FormOptions>(o => o.MultipartBodyLengthLimit = 220L * 1024 * 1024);
builder.WebHost.ConfigureKestrel(o => o.Limits.MaxRequestBodySize = 220L * 1024 * 1024);
var directory = builder.Configuration["Storage:Directory"] ?? "App_Data";
if (!Path.IsPathRooted(directory)) directory = Path.Combine(builder.Environment.ContentRootPath, directory);
if (blobEnabled) builder.Services.AddSingleton<ICatalogStore, BlobCatalogStore>();
else builder.Services.AddSingleton<ICatalogStore>(_ => new JsonCatalogStore(directory));
builder.Services.AddSingleton<IDocumentExtractor, DocumentExtractor>();
if (blobEnabled) builder.Services.AddSingleton<IDraftStore, BlobDraftStore>();
else builder.Services.AddSingleton<IDraftStore, MemoryDraftStore>();
builder.Services.AddScoped<LibraryService>();
builder.Services.AddScoped<BackupService>();
var app = builder.Build();
if (!app.Environment.IsDevelopment()) app.UseExceptionHandler("/Library/Error");
app.Use(async (context, next) =>
{
    context.Response.Headers["X-Content-Type-Options"] = "nosniff";
    context.Response.Headers["X-Frame-Options"] = "DENY";
    context.Response.Headers["Referrer-Policy"] = "same-origin";
    context.Response.Headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self' https://*.blob.vercel-storage.com https://blob.vercel-storage.com; frame-ancestors 'none'; base-uri 'self'; form-action 'self'";
    // Textos pessoais e backups não devem ficar no cache de um proxy compartilhado.
    context.Response.Headers.CacheControl = "no-store";
    await next();
});
app.UseStaticFiles();
app.UseRouting();

app.MapControllerRoute("default", "{controller=Library}/{action=Index}/{id?}");
app.Run();
