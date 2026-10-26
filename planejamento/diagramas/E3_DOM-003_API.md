---
{
  "id": "DIAG-DET-E3_DOM-003_API",
  "etapa": 3,
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
  "avaliacao": "AV-E3",
  "diagrama": "DIAG-003",
  "gate": "Pendente de ratificação humana; avanço documental delegado",
  "aprovado_por": null,
  "aprovado_em": null,
  "commit_pr": null
}
---

# DOM-003 — API

Fonte editável v1.0; estado Proposta; autor/conferência: mesma IA; revisão independente pendente. IDs: API-005, API-006. Legenda: setas indicam consumo, composição ou transição conforme rótulo; sem componente físico implícito.

```mermaid
flowchart TD
 A["Comando validado / sessão local"]
 A --> S0["API-005 / UC-005"]
 S0 --> R0["Resultado tipado ou erro; sem confirmação falsa"]
 A --> S1["API-006 / UC-006, UC-007"]
 S1 --> R1["Resultado tipado ou erro; sem confirmação falsa"]
```

Descrição acessível: Artefatos do tipo API em DOM-003, com finalidade, estados e consumidores; detalhes e justificativas nos seis arquivos do domínio. Simplificações: contratos/atributos completos no Markdown canônico. Semântica conferida contra fichas v1.0; renderização Mermaid não executada neste ambiente. PNG da etapa é síntese separada renderizada, e não renderização deste grafo.
