---
{
  "id": "SPEC-DOM-004-DATA",
  "etapa": 3,
  "dominio": "DOM-004",
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
| DATA-007 | DOM-004 | Obra | docId UUID, title string, format enum, sourceHash hash, blobRef path relativo, currentRevision hash, createdAt instant | Obra 1:N revisões; aponta para uma revisão atual; blob em diretório interno | Pendente → pronta → excluindo → excluída; mesmo hash oferece abrir existente ou importar como cópia explícita | Acervo cria/altera/exclui; outros domínios leem por ID |
| DATA-008 | DOM-004 | Snapshot | snapshotId UUID, schemaVersion int, manifest object, entries hash[], createdAt instant | Snapshot inclui N obras e namespaces de leitura; nenhum caminho absoluto | Preparando → validado → finalizado; falha elimina staging; backup externo sob controle do usuário | Acervo cria/lê/restaura; não indexa diretórios externos |

Classificação: texto, títulos, notas e histórico podem conter conteúdo pessoal/sensível fornecido pelo usuário. Necessidade: leitura local e continuidade. Acesso: somente sessão local, sem telemetria de conteúdo. Retenção: até exclusão explícita da obra; temporários de importação são eliminados ao concluir/cancelar e resíduos no próximo início. Backups externos são responsabilidade de retenção do usuário e contêm conteúdo em claro; informar antes de exportar.

Índices e layouts são derivados reconstruíveis. Excluir obra remove dados ativos e temporários; não prometer apagamento forense de SSD, backups do SO ou cópias externas. Arquivo original selecionado permanece intocado. Nova extração cria outra revisão e não migra notas silenciosamente; âncoras incompatíveis são sinalizadas.
