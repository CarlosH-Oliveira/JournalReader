---
{
  "id": "CONTRACT-001",
  "etapa": 6,
  "dominio": null,
  "versao": "1.0",
  "estado": "Proposta",
  "fontes": [
    "Normativa v2.0 de 23/10/2026",
    "Solicitação do usuário de 26/10/2026"
  ],
  "ids_relacionados": [],
  "responsavel": "IA autora",
  "revisor": "Autoavaliação; independência não disponível",
  "avaliacao": "AV-E6",
  "diagrama": "DIAG-006",
  "gate": "Pendente de ratificação humana; avanço documental delegado",
  "aprovado_por": null,
  "aprovado_em": null,
  "commit_pr": null
}
---

# Contratos, limites e invariantes

## Envelope e confiança

Comando local: `{commandId:uuid, type:enum, docId?:uuid, revision?:sha256, expectedVersion?:int, payload:validated}`. Resposta: `{commandId,status:ok|pending|error,version?,data?,error?:{code,retryable}}`. Evento: `{eventId,sequence,commandId,docId?,type,status,errorCode?}`. Nunca expor SQL, execução de shell ou abertura de caminho arbitrário à UI. Tokens são opacos, curtos e ligados à janela/comando; duração de 15 minutos ou revogação ao fechar/cancelar. Validação de remetente IPC ocorre no host.

## Documento e texto

TXT UTF-8 padrão; BOM suportado; se decodificação substituir caracteres, pedir codificação ou recusar, sem silenciosamente salvar “�”. Detectar UTF-16 por BOM; codificação legada depende de escolha explícita. Preservar parágrafos; finais de linha normalizados; espaços e pontuação não são “corrigidos” por IA.

PDF: camada textual por página, referências de origem, agrupamento heurístico por coordenadas, alerta de possível ordem ruim. Imagem sem texto e proteção são recusadas. Não prometer extração de fórmulas/tabelas complexas. Tabela extraída de forma ambígua exige alerta e não vira texto supostamente fiel.

EPUB: container e package válidos, spine na ordem canônica; navegação gera sumário quando disponível; conteúdo não linear acessível por link interno se textual. Remover scripts/estilos ativos, handlers e recursos externos. Texto alternativo de imagem é exibido como bloco identificado; imagem sem alt gera aviso; preservação visual de figuras não é objetivo. Tabelas simples podem ser linearizadas com aviso; estruturas não textuais complexas são diagnosticadas. Notas e links internos resolvem âncoras de origem; link externo só abre navegador após ação explícita e confirmação de saída, nunca durante importação.

## Limites iniciais — hipóteses de capacidade

Até 50 MiB por arquivo; PDF até 2000 páginas; EPUB até 10000 entradas, 200 MiB descompactados e razão máxima 100:1 por entrada; documento normalizado até 5 milhões de caracteres UTF-16. Exceder qualquer limite interrompe antes de commit e mostra LIMIT. Biblioteca até 1000 obras no piloto, índice por obra carregado sob demanda. Nota até 10000 caracteres, consulta 1–256, 100 resultados por lote. Limites são configuração versionada do produto, não propriedade conhecida das bibliotecas.

Validação de ZIP: contagem/tamanho real durante leitura, proibir paths absolutos, `..`, symlinks, nomes equivalentes após normalização e colisões case-insensitive. XML sem entidades externas/DTD e com limite de profundidade 128. Arquivos restaurados não escapam do staging. Checagem de espaço livre é estimativa e não substitui tratamento de erro de I/O.

## Paginação e âncoras

Folha de largura padrão 1184px, margens internas 24px, três gutters de 24px: largura útil de texto por coluna = (1184 − 48 − 72)/4 = 266px. Altura útil deriva da janela descontando controles/margens e nunca é infinita. Fonte inicial serif 18px, entrelinha 1,5; carregar fontes antes de medir. Não usar column-width que altere count sem controle; contabilizar overflow em grupos de quatro colunas. Última folha pode ter colunas vazias.

Âncoras não dependem de coluna/folha. Offset UTF-16 no texto canônico com ajuste para fronteiras de grafema. Índice pode usar normalização para comparação, mas retorna offsets pelo mapa inverso. Alterar perfil incrementa generation; resultado antigo é descartado. Títulos são blocos, hifenização apenas visual; buscar usa texto sem hifens visuais. Palavra longa admite quebra de emergência sem inserir caracteres no canônico. Modo acessível usa uma coluna refluível, ativada explicitamente e anunciada.

## Persistência e recuperação

Posição salva com debounce alvo 500ms após movimento, em mudança de obra e no fechamento; só “salvo” após commit. Encerrar abruptamente antes do commit pode perder o último movimento e deve ser risco explícito; nota nunca some sem aviso de rascunho. Repetir commandId retorna resultado lógico existente. Não há conflito entre dispositivos; concorrência local usa expectedVersion e único escritor.

Backup v1: manifesto com schemaVersion, snapshotId, obras/revisões/âncoras e hashes SHA-256; exportação lógica consistente para ZIP local, sem caminhos absolutos. Hash detecta corrupção, não autentica origem; backup não confiável sempre é validado. Restauração substitui acervo inteiro com confirmação, sem merge silencioso. Preparar geração nova, flush/fsync quando suportado, validar, gravar diário de intenção e trocar ponteiro; iniciar reconciliando diário. Preservar geração anterior até confirmar abertura; rollback retorna ponteiro anterior. Não afirmar atomicidade conjunta banco/filesystem apenas por usar SQLite.

Exclusão bloqueia novas escritas da obra e invalida sessões; primeiro remove referências em transação, depois remove blobs sem referência. Falha posterior é pendência de limpeza visível, não rollback fictício de arquivo apagado. Não apagar originais ou cópias externas. Índice é reconstruível; nunca restaurar índice de versão incompatível como fonte de verdade.
