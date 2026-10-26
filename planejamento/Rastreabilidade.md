---
{
  "id": "TRACE-001",
  "etapa": 0,
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
  "avaliacao": "Ver Avaliacoes/Painel.md",
  "diagrama": null,
  "gate": "Pendente de ratificação humana; avanço documental delegado",
  "aprovado_por": null,
  "aprovado_em": null,
  "commit_pr": null
}
---

# Cadeia de rastreabilidade principal

Origem comum IDEA-001 → MOD-001 → SET-003. Todas as versões abaixo são 1.0 Proposta.

| FEAT | DOM | UC | AC | NUC participantes | FLOW representativo | TEST futuro | Evidência |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FEAT-001 | DOM-001 | UC-001 | AC-001 | NUC-001, NUC-002, NUC-003, NUC-008 | FLOW-001 | TEST-001 | Planejado; EV reservado |
| FEAT-002 | DOM-001 | UC-002 | AC-002 | NUC-001, NUC-002, NUC-003 | FLOW-001 | TEST-002 | Planejado; EV reservado |
| FEAT-003 | DOM-002 | UC-003 | AC-003 | NUC-004, NUC-007 | FLOW-001 | TEST-003 | Planejado; EV reservado |
| FEAT-004 | DOM-002 | UC-004 | AC-004 | NUC-004, NUC-007 | FLOW-002 | TEST-004 | Planejado; EV reservado |
| FEAT-005 | DOM-003 | UC-005 | AC-005 | NUC-005, NUC-006, NUC-007 | FLOW-003 | TEST-005 | Planejado; EV reservado |
| FEAT-006 | DOM-003 | UC-006 | AC-006 | NUC-005, NUC-007 | FLOW-002 | TEST-006 | Planejado; EV reservado |
| FEAT-007 | DOM-003 | UC-007 | AC-007 | NUC-005, NUC-007 | FLOW-005 | TEST-007 | Planejado; EV reservado |
| FEAT-008 | DOM-004 | UC-008 | AC-008 | NUC-008, NUC-009 | FLOW-006 | TEST-008 | Planejado; EV reservado |
| FEAT-009 | DOM-004 | UC-009 | AC-009 | NUC-008, NUC-009 | FLOW-007 | TEST-009 | Planejado; EV reservado |

Cada feature agora tem UC/AC/FLOW/TEST e dono; o grafo completo de dados, serviços, jobs, mensagens e telas está em Mapa_de_Artefatos de cada domínio. Um fluxo representativo não exclui outros vínculos do catálogo. ADR-001–006 e riscos se vinculam por UC/fluxo nas respectivas fichas. TEST não é execução; EV-001–015 não foram produzidos. Não há TKT/INC/REL porque as etapas 7–9 não fazem parte desta entrega.
