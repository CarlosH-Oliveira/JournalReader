---
{
  "id": "MAP-FLOW",
  "etapa": 5,
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
  "avaliacao": "AV-E5",
  "diagrama": "DIAG-005",
  "gate": "Pendente de ratificação humana; avanço documental delegado",
  "aprovado_por": null,
  "aprovado_em": null,
  "commit_pr": null
}
---

# Jornadas ponta a ponta

| ID | Objetivo | Telas | Núcleos | UC | Aceites |
| --- | --- | --- | --- | --- | --- |
| FLOW-001 | Importar e abrir | VIEW-004 → VIEW-001 → VIEW-002 | NUC-009, NUC-003, NUC-001, NUC-002, NUC-008, NUC-004, NUC-007 | UC-001, UC-002, UC-003 | AC-001, AC-002, AC-003 |
| FLOW-002 | Personalizar e reorganizar | VIEW-002 → VIEW-002 | NUC-007, NUC-004, NUC-005, NUC-008 | UC-003, UC-004, UC-006 | AC-003, AC-004, AC-006 |
| FLOW-003 | Buscar e usar sumário | VIEW-002 → VIEW-002 | NUC-007, NUC-006, NUC-005, NUC-004 | UC-005 | AC-005 |
| FLOW-004 | Retomar e marcar posição | VIEW-004 → VIEW-002 | NUC-009, NUC-007, NUC-005, NUC-004, NUC-008 | UC-006 | AC-006 |
| FLOW-005 | Destacar e escrever nota | VIEW-002 → VIEW-003 → VIEW-002 | NUC-007, NUC-005, NUC-008, NUC-004 | UC-007 | AC-007 |
| FLOW-006 | Excluir obra do acervo | VIEW-004 → VIEW-004 | NUC-009, NUC-008, NUC-007 | UC-008 | AC-008 |
| FLOW-007 | Exportar e restaurar backup | VIEW-004 → VIEW-004 | NUC-009, NUC-008 | UC-009 | AC-009 |

Cobertura: FLOW-001 cobre FEAT-001–003; FLOW-002 FEAT-003/004; FLOW-003 FEAT-005; FLOW-004 FEAT-006; FLOW-005 FEAT-007; FLOW-006 FEAT-008; FLOW-007 FEAT-009. A sessão começa na biblioteca e alcança resultado persistido ou erro recuperável. Todas as ações de abrir/retomar e backup são locais; conectividade externa não participa.
