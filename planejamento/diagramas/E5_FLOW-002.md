---
{
  "id": "DIAG-DET-E5_FLOW-002",
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

# FLOW-002 — Personalizar e reorganizar

Fonte editável v1.0; estado Proposta; autor/conferência: mesma IA; revisão independente pendente. IDs: FLOW-002, NUC-007, NUC-004, NUC-005, NUC-008, AC-003, AC-004, AC-006. Legenda: setas indicam consumo, composição ou transição conforme rótulo; sem componente físico implícito.

```mermaid
sequenceDiagram
 actor L as Leitor
 participant V as Interface
 participant N as Núcleo local
 participant D as Estado autoritativo
 L->>V: Ação explícita
 V->>N: Comando validado e IDs
 N->>D: Consultar ou alterar conforme contrato
 alt Resultado válido
 D-->>N: Estado/revisão ou commit confirmado
 N-->>V: Resultado real e âncora
 V-->>L: Personalizar e reorganizar concluído
 else Erro, cancelamento ou atraso
 D-->>N: Código e estado recuperável
 N-->>V: Sem sucesso presumido
 V-->>L: Motivo e ação de recuperação
 end
```

Sequência específica deste fluxo:

```mermaid
flowchart TD
 P0["Capturar âncora"]
 P1["validar perfil"]
 P0 --> P1
 P2["incrementar generation"]
 P1 --> P2
 P3["API-003 recompõe"]
 P2 --> P3
 P4["API-004 localiza"]
 P3 --> P4
 P5["MSG-002 pronto"]
 P4 --> P5
 P6["salvar perfil/posição e renderizar"]
 P5 --> P6

```

Descrição acessível: Capturar âncora → validar perfil → incrementar generation → API-003 recompõe → API-004 localiza → MSG-002 pronto → salvar perfil/posição e renderizar; erros: Fonte ausente usa fallback informado; generation obsoleta não substitui atual; falha mantém layout anterior; recuperação: Recomposição mostra ocupado; obra removida cancela e volta ao acervo; mudança rápida só aplica última geração; desfazer perfil é recuperação. Simplificações: contratos/atributos completos no Markdown canônico. Semântica conferida contra fichas v1.0; renderização Mermaid não executada neste ambiente. PNG da etapa é síntese separada renderizada, e não renderização deste grafo.
