# Implantação na Vercel

O projeto usa o preset `container`, definido em `vercel.json`, e `Dockerfile.vercel` na raiz. O SDK .NET 8 compila a aplicação em um estágio separado; a imagem final executa ASP.NET Core na porta 80. O filtro de host permite localhost e subdomínios vercel.app. Domínios personalizados precisam ser adicionados a AllowedHosts.

## Limitações que impedem homologação de produção

- `/tmp/journalreader` é apenas armazenamento temporário para validar a execução na prévia. O catálogo pode desaparecer em reinícios e não é compartilhado entre instâncias. Não importe documentos reais nessa configuração.
- Para produção, substituir `JsonCatalogStore` por persistência transacional externa e `MemoryDraftStore` e sessões em memória por estado compartilhado. Persistir também as chaves de Data Protection usadas por cookies e antifalsificação.
- Manter Deployment Protection: a aplicação é pessoal, tem acervo compartilhado e não implementa autenticação própria.
- A aplicação permite upload de até 220 MB, mas a Vercel limita corpos de requisição a 4,5 MB. Arquivos maiores exigem upload direto para armazenamento privado e extração posterior.
- O build detectou aviso NU1902 no AngleSharp 1.1.2. A atualização requer validação do extrator EPUB antes da liberação.

## Verificação

Confirmar build `dotnet publish` nos logs e resposta HTTP 200 da biblioteca, importação e backup. Antes da produção, testar importação/confirmar/leitura, reinício de instância, múltiplas instâncias, retomada, destaques e restauração de backup com a persistência externa real.
