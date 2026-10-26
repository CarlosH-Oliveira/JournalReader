---
{
  "id": "SPEC-DOM-003-MSG",
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

# Eventos e feedback

| ID | DOM | UC | Evento | Produtor → consumidor | Payload | Entrega e falha |
| --- | --- | --- | --- | --- | --- | --- |
| MSG-003 | DOM-003 | UC-005, UC-006, UC-007 | LeituraEstado | Leitura → VIEW-002/003 | commandId,saveState,indexState,errorCode? | Canal local; confirmado somente após commit; dedup commandId/version; consulta de estado recupera perda |

Natureza: eventos internos e feedback na interface; prioridade normal, falhas finais imediatas. Destinatário é somente a janela da sessão da obra/job. Prazo alvo de feedback: 250ms após estado do serviço. Consentimento para push/e-mail: N/A, canais externos inexistentes. Indicadores de erro essencial não podem ser silenciados por preferência. Não há broker, e-mail ou notificação do SO. EventId e sequence permitem deduplicação; estado autoritativo pode ser consultado, portanto perda de evento não perde resultado.
