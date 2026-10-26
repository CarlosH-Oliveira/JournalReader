---
{
  "id": "DIAG-DET-E2_Dominios",
  "etapa": 2,
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
  "avaliacao": "AV-E2",
  "diagrama": "DIAG-002",
  "gate": "Pendente de ratificação humana; avanço documental delegado",
  "aprovado_por": null,
  "aprovado_em": null,
  "commit_pr": null
}
---

# Fronteiras e contratos

Fonte editável v1.0; estado Proposta; autor/conferência: mesma IA; revisão independente pendente. IDs: DOM-001–004. Legenda: setas indicam consumo, composição ou transição conforme rótulo; sem componente físico implícito.

```mermaid
flowchart TD
 A["DOM-004: acervo / FEAT-008,009"] -->|"arquivo escolhido / API-001"| I["DOM-001: ingestão / FEAT-001,002"]
 I -->|"revisão confirmada / API-008"| A
 I -->|"blocos imutáveis"| C["DOM-002: composição / FEAT-003,004"]
 C -->|"layout e âncoras"| L["DOM-003: leitura / FEAT-005–007"]
 L -->|"posição e notas / API-008"| A
```

Descrição acessível: Acervo seleciona e persiste, ingestão fornece blocos, composição calcula layout e leitura grava continuidade; setas de dados não são chamadas recursivas. Simplificações: contratos/atributos completos no Markdown canônico. Semântica conferida contra fichas v1.0; renderização Mermaid não executada neste ambiente. PNG da etapa é síntese separada renderizada, e não renderização deste grafo.
