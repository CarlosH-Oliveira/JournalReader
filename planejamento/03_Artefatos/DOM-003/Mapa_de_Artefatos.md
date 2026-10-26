---
{
  "id": "MAP-DOM-003",
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

# Composição rastreável

| UC | Feature | Dados próprios | Serviços | Workers | Mensagens | Telas próprias/consumidas | Aceite |
| --- | --- | --- | --- | --- | --- | --- | --- |
| UC-005 | FEAT-005 | DATA-005,DATA-006 | API-005 | JOB-002 | MSG-003 | VIEW-002 | AC-005 |
| UC-006 | FEAT-006 | DATA-005,DATA-006 | API-006 | N/A | MSG-003 | VIEW-002 | AC-006 |
| UC-007 | FEAT-007 | DATA-005,DATA-006 | API-006 | N/A | MSG-003 | VIEW-003 | AC-007 |

Consulte dependências interdomínio em 02_Dominios/Dependencias.md. Os vínculos auxiliares com API-008 e DATA-007 são infraestrutura de persistência compartilhada, sem mudar a propriedade lógica. Cada tipo é avaliado separadamente no painel; não se compensa reprovação por média.
