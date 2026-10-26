# Arquitetura e manutenção

## Dependências permitidas

```text
Web ────────────→ Application ───→ Domain
 │                     ↑
 └──→ Infrastructure ───┘
```

O projeto Web referencia Infrastructure exclusivamente como composição das implementações em `Program.cs`. Controllers dependem dos casos de uso. Domain não conhece ASP.NET, JSON, arquivos, PdfPig ou HTML. Application define as portas `ICatalogStore`, `IDocumentExtractor` e `IDraftStore`.

- **Domain/Models.cs:** entidades Book, Annotation, ReaderPreferences, limites e erros esperados.
- **Application/LibraryService.cs:** listar, pré-visualizar, confirmar importação, salvar posição, buscar e manter marcações. Centraliza validação e controle de versão.
- **Application/BackupService.cs:** envelope de backup, hash e validação dos dados restaurados.
- **Infrastructure/DocumentExtractor.cs:** TXT estrito, PDF via PdfPig e EPUB ZIP/package/spine/HTML. Converte tudo para texto antes da apresentação.
- **Infrastructure/JsonCatalogStore.cs:** lê um snapshot por operação. Em comandos, só grava se o delegado concluir sem erro. Serializa comandos concorrentes com SemaphoreSlim.
- **Infrastructure/MemoryDraftStore.cs:** uma prévia por sessão, expiração em 15 minutos e até dez prévias no processo. Documentos não confirmados não chegam ao acervo.
- **Web/Controllers:** convertem HTTP/formulários em chamadas dos casos de uso. Ações mutáveis são POST e recebem validação CSRF global.
- **Web/Views:** composição Razor das telas e formulários. Texto enviado pelo usuário nunca é renderizado com `Html.Raw`.
- **Web/wwwroot/js/reader.js:** layout multicolunas, Range DOM, navegação, seleção e comandos JSON. Não contém regras de persistência.

## Correspondência com os domínios do planejamento

| Planejamento | Implementação |
|---|---|
| DOM-001 Ingestão | DocumentExtractor, ImportDraft, ImportController, views Import |
| DOM-002 Composição | CSS multicolunas e funções de layout do reader.js |
| DOM-003 Leitura | Book/Annotation/Preferences, LibraryService, ReaderController, view Reader |
| DOM-004 Acervo | ICatalogStore, JsonCatalogStore, Library/Backup controllers, BackupService |

Trata-se de monólito modular por responsabilidades e camadas. Os quatro domínios não viraram quatro serviços distribuídos: isso não é necessário para este produto pessoal.

## Fluxo de importação

1. Receber upload até 50 MiB e validar extensão.
2. Extrair com adaptador específico; rejeitar conteúdo inválido ou acima dos limites.
3. Construir texto canônico e sumário de origem. TXT só normaliza BOM/finais de linha; PDF e EPUB necessariamente passam por extração.
4. Armazenar prévia em memória, vinculada à sessão.
5. Apresentar texto completo e alertas na view escapada.
6. Confirmar título e avisos. Deduplicar por SHA-256 do texto, gravar o acervo e remover a prévia.

Cancelamento, expiração ou erro antes de confirmar não adicionam obra ao catálogo. A sessão de prévia é volátil e não é sistema de identidade.

## Âncoras e paginação

A âncora é o offset UTF-16 no texto de `Book.Text`. Não é página física nem número de coluna. A revisão do texto é SHA-256; neste escopo não existe edição do texto depois de importar.

`reader.js` divide os parágrafos preservando offsets dos separadores, constrói nós com `textContent`, aplica destaques por intervalos e usa DOM Range para localizar a âncora na folha. Quatro colunas fixas de 266 px e gutter de 24 px produzem passo de 1160 px entre folhas. O viewport útil de 1136 px mostra as quatro colunas sem o gutter final. Alterar fonte ou modo recalcula a projeção a partir da mesma âncora.

Ao salvar, o backend ajusta a posição para fronteira de grafema com `StringInfo`. Uma seleção pode atravessar parágrafos; o intervalo continua sendo canônico. Destaques sobrepostos são segmentados no DOM; quando há cores sobrepostas, a primeira anotação cobre visualmente a região, mas todas permanecem no catálogo.

## Concorrência e erros

Cada obra tem `Version`. O navegador envia a versão conhecida em cada mutação; o caso de uso compara sob o lock do repositório e incrementa após aplicar. Divergência retorna HTTP 409. O leitor mostra erro e pede recarregamento; não sobrescreve silenciosamente outra aba.

A fila JavaScript serializa as mutações do mesmo leitor e usa a versão confirmada pelo comando anterior. Posição usa debounce de 500 ms; sucesso só aparece depois da resposta do servidor. Nota com falha de gravação mantém o diálogo/rascunho aberto. Em encerramento abrupto podem se perder os movimentos ainda não confirmados; `visibilitychange` tenta reduzir essa janela.

Erros esperados usam `ReaderException`; problemas de I/O não são transformados em sucesso. Em produção o middleware mostra página genérica e os detalhes ficam nos logs.

## Evolução recomendada

- Banco: implementar `ICatalogStore` com transação e concorrência otimista real. A interface atual trabalha com snapshot inteiro; em grandes acervos, evoluir para repositórios por agregado e paginação de consultas.
- Multiusuário: introduzir usuário/proprietário no domínio, autenticação e autorização de todas as ações e consultas. A sessão existente não resolve isso.
- Extração isolada: mover parsing para worker com limites de memória/CPU e fila limitada; manter a porta `IDocumentExtractor`.
- Sumário EPUB: interpretar nav/NCX e mapear IDs HTML a offsets antes da remoção de markup; manter navegação interna separada de recursos ativos.
- Recuperação: substituir `.previous` por snapshots imutáveis e ponteiro/diário ou usar transações de banco sem prometer atomicidade conjunta com blobs.
- Capacidade: o adaptador JSON reserializa o acervo a cada escrita; adequado apenas ao uso pessoal pequeno. O limite lógico de 1.000 obras não é uma garantia de desempenho com 1.000 obras no tamanho máximo.
