---
{
  "id": "DIAG-006",
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

# DIAG-006 — Arquitetura e riscos

Etapa: 6; versão 1.0; estado Proposta. Fonte editável: ../imagens/etapa_06.svg. Imagem: ../imagens/etapa_06.png. Fonte de verdade: ../06_Arquitetura/ e avaliação AV-E6. Sem commit Git alegado.

Objetivo: resumir as decisões e limites para revisão. Legenda: cada cartão é um grupo de responsabilidades/requisitos; proximidade não representa dependência ou sequência. As relações detalhadas estão nos mapas Mermaid e no Markdown. Simplificações: não exibe todos os atributos, exceções e riscos. Não é captura de um aplicativo funcionando.

Descrição acessível: DESKTOP LOCAL · ADR-001: Monólito modular. Interface isolada; sem contas, servidor ou envio de documentos. PIPELINE · ADR-002/003: Texto canônico → layout derivado. PDF.js candidato; EPUB segue ordem do spine. DADOS · ADR-004/005: SQLite e blobs; âncoras por revisão/bloco/offset. Backup transacional. PROVAS PLANEJADAS: Corpus, Unicode, zoom, parser hostil, disco cheio, cancelamento e restauração.

Autor e conferência semântica: mesma IA; revisão independente pendente. Verificação: comparar títulos, IDs e quantidades com catálogos da etapa; imagem renderizada com fonte Unicode e inspecionada quanto a limites geométricos. Estado não apresentado como aprovado.
