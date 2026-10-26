# Build em estágio separado; o runtime final não contém o SDK.
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /source
COPY Directory.Build.props LeitorDeJornal.sln ./
COPY src/ ./src/
RUN dotnet restore src/LeitorDeJornal.Web/LeitorDeJornal.Web.csproj
RUN dotnet publish src/LeitorDeJornal.Web/LeitorDeJornal.Web.csproj -c Release --no-restore -o /out

FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS runtime
WORKDIR /app
COPY --from=build /out ./
RUN mkdir -p /app/data && chown app:app /app/data
ENV ASPNETCORE_HTTP_PORTS=8080
ENV ASPNETCORE_ENVIRONMENT=Production
ENV Storage__Directory=/app/data
USER app
EXPOSE 8080
ENTRYPOINT ["dotnet", "LeitorDeJornal.Web.dll"]
