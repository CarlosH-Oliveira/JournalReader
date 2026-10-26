using System.Globalization;
using LeitorDeJornal.Application;
using LeitorDeJornal.Infrastructure;
using Microsoft.AspNetCore.Http.Features;
using Microsoft.AspNetCore.Mvc;

var builder = WebApplication.CreateBuilder(args);
CultureInfo.DefaultThreadCurrentCulture = CultureInfo.GetCultureInfo("pt-BR");
CultureInfo.DefaultThreadCurrentUICulture = CultureInfo.GetCultureInfo("pt-BR");
builder.Services.AddControllersWithViews(options => options.Filters.Add(new AutoValidateAntiforgeryTokenAttribute()));
builder.Services.AddDistributedMemoryCache();
builder.Services.AddSession(options =>
{
    options.Cookie.Name = ".LeitorDeJornal.Session";
    options.Cookie.HttpOnly = true;
    options.Cookie.IsEssential = true;
    options.Cookie.SameSite = SameSiteMode.Strict;
    options.IdleTimeout = TimeSpan.FromHours(8);
});
builder.Services.Configure<FormOptions>(o => o.MultipartBodyLengthLimit = 220L * 1024 * 1024);
builder.WebHost.ConfigureKestrel(o => o.Limits.MaxRequestBodySize = 220L * 1024 * 1024);
var directory = builder.Configuration["Storage:Directory"] ?? "App_Data";
if (!Path.IsPathRooted(directory)) directory = Path.Combine(builder.Environment.ContentRootPath, directory);
builder.Services.AddSingleton<ICatalogStore>(_ => new JsonCatalogStore(directory));
builder.Services.AddSingleton<IDocumentExtractor, DocumentExtractor>();
builder.Services.AddSingleton<IDraftStore, MemoryDraftStore>();
builder.Services.AddScoped<LibraryService>();
builder.Services.AddScoped<BackupService>();
var app = builder.Build();
if (!app.Environment.IsDevelopment()) app.UseExceptionHandler("/Library/Error");
app.Use(async (context, next) =>
{
    context.Response.Headers["X-Content-Type-Options"] = "nosniff";
    context.Response.Headers["X-Frame-Options"] = "DENY";
    context.Response.Headers["Referrer-Policy"] = "same-origin";
    context.Response.Headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; frame-ancestors 'none'; base-uri 'self'; form-action 'self'";
    // Textos pessoais e backups não devem ficar no cache de um proxy compartilhado.
    context.Response.Headers.CacheControl = "no-store";
    await next();
});
app.UseStaticFiles();
app.UseRouting();
app.UseSession();
app.MapControllerRoute("default", "{controller=Library}/{action=Index}/{id?}");
app.Run();
