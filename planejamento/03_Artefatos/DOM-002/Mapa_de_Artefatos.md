---
{
  "id": "MAP-DOM-002",
  "etapa": 3,
  "dominio": "DOM-002",
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
| UC-003 | FEAT-003 | DATA-003,DATA-004 | API-003 | N/A | MSG-002 | VIEW-002 | AC-003 |
| UC-004 | FEAT-004 | DATA-003,DATA-004 | API-003 | N/A | MSG-002 | VIEW-002 | AC-004 |

Consulte dependências interdomínio em 02_Dominios/Dependencias.md. Os vínculos auxiliares com API-008 e DATA-007 são infraestrutura de persistência compartilhada, sem mudar a propriedade lógica. Cada tipo é avaliado separadamente no painel; não se compensa reprovação por média.
