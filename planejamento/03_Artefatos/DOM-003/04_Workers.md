---
{
  "id": "SPEC-DOM-003-JOB",
  "etapa": 3,
  "dominio": "DOM-003",
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

# Workers e rotinas

| ID | DOM | UC | Objetivo | Gatilho | Dados/resultado | Concorrência, falha e limites |
| --- | --- | --- | --- | --- | --- | --- |
| JOB-002 | DOM-003 | UC-005 | Indexar texto | Documento confirmado ou índice ausente | Lê DATA-001; índice derivado da revisão | Um índice por docId/revision; staging e troca; descartar geração velha; até uma repetição transitória; índice removível/reconstruível; progresso e erro na busca |


Jobs aplicáveis executam fora da UI, sem permissão de rede. Falha e término são observáveis por MSG-001 ou MSG-003; fechamento encerra o processo, e o próximo início descarta staging não confirmado. Não há alegação de job já implementado.
