---
{
  "id": "DIAG-DET-E3_DOM-003_DATA",
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

# DOM-003 — DATA

Fonte editável v1.0; estado Proposta; autor/conferência: mesma IA; revisão independente pendente. IDs: DATA-005, DATA-006. Legenda: setas indicam consumo, composição ou transição conforme rótulo; sem componente físico implícito.

```mermaid
flowchart TD
 A["DOM-003: autoridade lógica"]
 A --> D0["DATA-005: EstadoLeitura"]
 D0 --> C0["Anchor = revision + blockId + offset UTF-16 no texto canônico"]
 A --> D1["DATA-006: Anotacao"]
 D1 --> C1["Ativa → editada ou excluída"]
```

Descrição acessível: Artefatos do tipo DATA em DOM-003, com finalidade, estados e consumidores; detalhes e justificativas nos seis arquivos do domínio. Simplificações: contratos/atributos completos no Markdown canônico. Semântica conferida contra fichas v1.0; renderização Mermaid não executada neste ambiente. PNG da etapa é síntese separada renderizada, e não renderização deste grafo.
