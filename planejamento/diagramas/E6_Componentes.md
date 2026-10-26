---
{
  "id": "DIAG-DET-E6_Componentes",
  "etapa": 6,
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
  "avaliacao": "AV-E6",
  "diagrama": "DIAG-006",
  "gate": "Pendente de ratificação humana; avanço documental delegado",
  "aprovado_por": null,
  "aprovado_em": null,
  "commit_pr": null
}
---

# Arquitetura lógica e limites

Fonte editável v1.0; estado Proposta; autor/conferência: mesma IA; revisão independente pendente. IDs: ADR-001–006, DOM-001–004. Legenda: setas indicam consumo, composição ou transição conforme rótulo; sem componente físico implícito.

```mermaid
flowchart TD
 U["1. Shell / UI sem Node"] -->|"bridge tipada"| H["Host e portas locais"]
 H --> I["2. Ingestão"]
 H --> L["4. Leitura e índice"]
 I --> T["6. Tarefas isoladas"]
 L --> T
 I -->|"blocos"| C["3. Composição"]
 L -->|"âncora e perfil"| C
 H --> A["5. Acervo / escritor único"]
 I -->|"documento pronto"| A
 L -->|"posição e notas"| A
 A --> D["SQLite + blobs + snapshot anterior"]
```

Descrição acessível: UI e host comunicam por bridge limitada; módulos locais mantêm propriedade lógica e acervo guarda dados; tarefas não recebem autoridade ilimitada. Simplificações: contratos/atributos completos no Markdown canônico. Semântica conferida contra fichas v1.0; renderização Mermaid não executada neste ambiente. PNG da etapa é síntese separada renderizada, e não renderização deste grafo.
