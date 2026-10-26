---
{
  "id": "DIAG-DET-E5_FLOW-005",
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

# FLOW-005 — Destacar e escrever nota

Fonte editável v1.0; estado Proposta; autor/conferência: mesma IA; revisão independente pendente. IDs: FLOW-005, NUC-007, NUC-005, NUC-008, NUC-004, AC-007. Legenda: setas indicam consumo, composição ou transição conforme rótulo; sem componente físico implícito.

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
 V-->>L: Destacar e escrever nota concluído
 else Erro, cancelamento ou atraso
 D-->>N: Código e estado recuperável
 N-->>V: Sem sucesso presumido
 V-->>L: Motivo e ação de recuperação
 end
```

Sequência específica deste fluxo:

```mermaid
flowchart TD
 P0["Selecionar intervalo DOM"]
 P1["converter em âncoras canônicas"]
 P0 --> P1
 P2["editar nota"]
 P1 --> P2
 P3["API-006 valida e grava via API-008"]
 P2 --> P3
 P4["MSG-003 confirma"]
 P3 --> P4
 P5["painel lista"]
 P4 --> P5
 P6["ir ao trecho por API-004"]
 P5 --> P6

```

Descrição acessível: Selecionar intervalo DOM → converter em âncoras canônicas → editar nota → API-006 valida e grava via API-008 → MSG-003 confirma → painel lista → ir ao trecho por API-004; erros: Seleção inválida não grava; nota acima do limite pede reduzir; erro de disco preserva rascunho; revisão antiga mostra nota órfã; recuperação: Escrita em atraso mostra pendente; obra excluída impede salvar; repetir commandId devolve mesma nota; cancelar antes de salvar descarta somente com aviso se rascunho. Simplificações: contratos/atributos completos no Markdown canônico. Semântica conferida contra fichas v1.0; renderização Mermaid não executada neste ambiente. PNG da etapa é síntese separada renderizada, e não renderização deste grafo.
