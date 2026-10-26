---
{
  "id": "SPEC-DOM-001-DATA",
  "etapa": 3,
  "dominio": "DOM-001",
  "versao": "1.0",
  "estado": "Proposta",
  "fontes": [
    "Normativa v2.0 de 23/10/2026",
    "Solicitação do usuário de 26/10/2026"
  ],
  "ids_relacionados": [],
  "responsavel": "IA autora",
  "revisor": "Autoavaliação; independência não disponível",
  "avaliacao": "AV-E3",
  "diagrama": "DIAG-003",
  "gate": "Pendente de ratificação humana; avanço documental delegado",
  "aprovado_por": null,
  "aprovado_em": null,
  "commit_pr": null
}
---

# Entidades e estados

| ID | DOM | Entidade | Atributos e tipos | Relações | Invariantes/ciclo | Operações |
| --- | --- | --- | --- | --- | --- | --- |
| DATA-001 | DOM-001 | DocumentoNormalizado | docId UUID, revision SHA-256, sourceHash SHA-256, format enum, language string?, blocks Block[], toc TocEntry[], warnings string[] | Obra 1:N revisões; revisão 1:N blocos; bloco contém blockId e text string UTF-16, sourceRef string? | Prévia → confirmado ou descartado; revisão confirmada imutável; NFKC não aplicado ao texto canônico | Ingestão cria; composição/leitura leem; acervo persiste e exclui sob comando do dono |
| DATA-002 | DOM-001 | Importacao | jobId UUID, commandId UUID, status enum, progress int, warningCodes string[], tempRef string?, accepted bool | Uma importação candidata a uma obra; nenhuma obra pronta antes de aceite | Validando → extraindo → prévia → confirmado; erro/cancelado terminais | Ingestão cria/altera; UI de importação lê; temporários apagados em cancelamento |

Classificação: texto, títulos, notas e histórico podem conter conteúdo pessoal/sensível fornecido pelo usuário. Necessidade: leitura local e continuidade. Acesso: somente sessão local, sem telemetria de conteúdo. Retenção: até exclusão explícita da obra; temporários de importação são eliminados ao concluir/cancelar e resíduos no próximo início. Backups externos são responsabilidade de retenção do usuário e contêm conteúdo em claro; informar antes de exportar.

Índices e layouts são derivados reconstruíveis. Excluir obra remove dados ativos e temporários; não prometer apagamento forense de SSD, backups do SO ou cópias externas. Arquivo original selecionado permanece intocado. Nova extração cria outra revisão e não migra notas silenciosamente; âncoras incompatíveis são sinalizadas.
