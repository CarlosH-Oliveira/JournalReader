# Leitor de Jornal

Aplicação pessoal em **ASP.NET Core 8 MVC + Razor**, organizada em **Clean Architecture**, baseada no planejamento das etapas 1 a 6 fornecido pelo solicitante. Comentários e documentação estão em português.

**Estado da entrega:** código-fonte para revisão, compilação, testes e implantação pelo destinatário. O SDK .NET não estava disponível no ambiente de autoria; o acesso à rede impediu instalá-lo. Portanto, **não foram executados restore, build, testes .NET ou validação em navegador**. Foi verificada a sintaxe dos arquivos JavaScript com `node --check` e a estrutura XML dos projetos. Não considere esta entrega homologada para produção.

## Requisitos e execução

- SDK .NET 8.0 (versão suportada mais recente da linha 8.0), ou SDK superior capaz de compilar `net8.0`.
- Acesso ao NuGet para restaurar PdfPig 0.1.9 e AngleSharp 1.1.2.
- Navegador atual com JavaScript, CSS multicolunas, `dialog` e `crypto.randomUUID` (localhost ou HTTPS).
- Pasta de dados gravável e espaço para acervo + geração anterior + backups.

Na raiz da solução:

```bash
dotnet restore LeitorDeJornal.sln
dotnet build LeitorDeJornal.sln -c Release
dotnet run --project src/LeitorDeJornal.Web --launch-profile LeitorDeJornal
```

Acesse **http://localhost:5080**. Não é necessário Node.js, npm, banco externo ou ferramenta de frontend. Abra `LeitorDeJornal.sln` no Visual Studio 2022 atualizado, se preferir.

Os dados ficam por padrão em `src/LeitorDeJornal.Web/App_Data/catalog.json`. Configure `Storage:Directory` no `appsettings.json` ou a variável de ambiente `Storage__Directory` para usar outro diretório. Não armazene dados pessoais dentro de `wwwroot`.

## Funcionalidades entregues no código

- Acervo com busca por título, filtro por formato, ordenação e exclusão confirmada.
- Importação TXT UTF-8/UTF-16 com BOM, PDF com camada textual e EPUB refluível sem criptografia.
- Prévia integral antes de persistir, confirmação de alertas, cancelamento e detecção de texto duplicado.
- Leitura em quatro colunas sequenciais por folha, navegação por botões e teclado, folha horizontal em telas estreitas e modo acessível de uma coluna.
- Temas claro, sépia e escuro; fonte de 14 a 32 px.
- Busca textual com offsets no texto original, até 100 resultados. Busca ignora maiúsculas/minúsculas; diferencia acentos e formas Unicode distintas.
- Retomada por âncora UTF-16 em vez de página física, preservada nas alterações de layout.
- Marcadores de posição, destaques e notas com edição, remoção e navegação ao trecho.
- Salvamento com debounce e controle otimista de versão para detectar conflitos entre abas.
- Backup JSON versionado, SHA-256, validação integral antes de substituir o acervo e confirmação explícita.
- Tokens antifalsificação em formulários e comandos JSON, saída Razor escapada, extração somente de texto e limites de upload.

Consulte o [roteiro de testes](docs/TESTES.md) antes da implantação.

## Organização

```text
src/
  LeitorDeJornal.Domain/          Entidades, valores e limites do negócio
  LeitorDeJornal.Application/     Casos de uso e portas de infraestrutura
  LeitorDeJornal.Infrastructure/  Extração, persistência e prévias temporárias
  LeitorDeJornal.Web/             Controllers MVC, views Razor, CSS e JavaScript
    App_Data/                    Criada em execução; nunca incluir no controle de versão
      catalog.json               Acervo canônico
      catalog.json.previous      Geração anterior para recuperação manual
      catalog.json.tmp           Escrita transitória, não usar como backup
amostras/                        Corpus simples para os testes manuais
planejamento/                    Planejamento original fornecido pelo solicitante
```

Leia [ARQUITETURA.md](docs/ARQUITETURA.md) para entender responsabilidades, dependências e decisões. Os documentos originais são referência de planejamento; pedidos de ratificação neles não representam homologação desta implementação.

## Publicação

```bash
dotnet publish src/LeitorDeJornal.Web -c Release -o ./publish
```

Defina as variáveis de ambiente conforme sua plataforma e execute a DLL na pasta publicada:

```bash
dotnet LeitorDeJornal.Web.dll --urls http://127.0.0.1:5080
```

- `ASPNETCORE_ENVIRONMENT=Production`
- `Storage__Directory=/caminho/absoluto/persistente/acervo`
- `AllowedHosts=seu-host.exemplo;localhost` quando houver domínio próprio.
- Instale o ASP.NET Core Runtime 8 na máquina de destino (ou publique como self-contained para o RID desejado).
- Em IIS, instale o Hosting Bundle correspondente. Em Linux, configure serviço e proxy reverso HTTPS.
- Configure no proxy o limite de upload adequado (55 MiB para documentos; até 210 MiB para requisição de backup) e timeout para extração.

Há um `Dockerfile` opcional e exemplo de Compose em `compose.yaml`; veja [IMPLANTACAO.md](docs/IMPLANTACAO.md).

## Limites e adaptações conscientes

1. O planejamento original propunha Electron/TypeScript/SQLite. O pedido atual determina ASP.NET MVC; o runtime foi substituído por servidor ASP.NET Core, views Razor e JavaScript nativo no navegador.
2. A persistência desta entrega usa **JSON em disco**, com escritor único em memória, arquivo temporário, flush e renomeação no mesmo volume. Não usa SQLite nem Entity Framework. Foi escolhida para permitir instalação pessoal sem banco ou migrações. O contrato `ICatalogStore` permite trocar por SQLite/EF Core sem mover regras para controllers.
3. **Instância única, acervo compartilhado e sem autenticação**, conforme o escopo pessoal sem contas. Sessão isola apenas prévias, não o acervo. Para acesso remoto, coloque autenticação no proxy ou implemente contas/autorização e isolamento antes de expor o serviço. Não execute várias réplicas sobre a mesma pasta.
4. PDF usa extração heurística; ordem editorial, fórmulas e tabelas não são garantidas. Páginas sem texto geram alerta; documentos inteiramente digitalizados não são aceitos. Não há OCR. Arquivos que o extrator não consegue abrir são recusados.
5. EPUB é convertido em texto, sem layout visual, scripts, recursos remotos ou links ativos. Sumário é derivado de títulos/capítulos; notas de rodapé entram na sequência, sem resolução navegável de links internos. EPUB com `encryption.xml` é recusado conservadoramente, inclusive pacotes com apenas fontes ofuscadas. EPUB 2 com layout fixo declarado por metadados de fornecedor pode exigir detecção adicional.
6. Backup é JSON, não ZIP. Limite de 200 MiB por backup: um acervo maior deve ser copiado administrativamente com o processo parado. SHA-256 detecta corrupção, não autentica nem cifra o arquivo. Não há criptografia do acervo.
7. O arquivo `.previous` guarda apenas a geração imediatamente anterior e é substituído a cada escrita. Não há diário transacional entre múltiplos arquivos nem recuperação automática após corrupção. Não se promete durabilidade de metadados de diretório em falha de energia.
8. Extração roda no processo do servidor com limites, sem sandbox de processo utilitário; o custo de parsing depende do documento. Uso público requer isolamento do parser e limites operacionais adicionais.
9. Paginação é calculada pelo navegador. Altura textual inicial de 560 px, folha com quatro colunas fixas e fonte local. Validar corpus, zoom e acessibilidade nos navegadores de destino. A última folha pode ter colunas vazias. Nenhum trecho deve ser resumido ou duplicado; use o corpus de teste para verificar.
10. Sem voz, dicionário, OCR, sincronização em nuvem, exportação editorial PDF ou aplicativo mobile.

## Recuperação administrativa

Se `catalog.json` estiver corrompido, a inicialização falha para evitar apagamento silencioso. Pare a aplicação, preserve uma cópia dos arquivos, valide a geração `catalog.json.previous` e, se íntegra, copie-a para `catalog.json`. Alternativamente, restaure um backup exportado em uma instalação com pasta de dados vazia pela tela de backup. Não copie o envelope de backup diretamente sobre `catalog.json`: os formatos são diferentes.

## Dependências

- ASP.NET Core / .NET 8: Microsoft.
- PdfPig 0.1.9: extração PDF; licença Apache-2.0.
- AngleSharp 1.1.2: parser HTML de EPUB; licença MIT.

Versões diretas estão fixadas no `.csproj`. Dependências transitivas são resolvidas pelo NuGet; audite-as antes de publicar e gere lock files se seu processo exigir builds reprodutíveis. Consulte `dotnet list package --include-transitive` e `dotnet list package --vulnerable --include-transitive`. Nenhuma biblioteca ou fonte é carregada de CDN no navegador.
