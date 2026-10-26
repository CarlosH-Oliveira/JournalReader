---
{
  "id": "SPEC-DOM-002-VIEW",
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

# Telas e acessibilidade

Sem tela canônica própria: DOM-002 é headless; UC-003/004 usam VIEW-002 de DOM-003. Estado visual, controles e permissões estão definidos uma vez no dono de composição. A ausência de tela própria não dispensa os casos interativos.
Regras transversais: foco visível, ordem de Tab lógica, nomes acessíveis, status assíncronos anunciados sem repetir a cada bloco. Setas/PageUp/PageDown navegam somente fora de campos; Escape fecha painel e devolve foco. Diálogos de exclusão/restauração têm foco contido e confirmação explícita. Não comunicar estado só por cor; contraste alvo 4,5:1 para texto comum.

VIEW-002 é definida apenas em DOM-003; consome composição de DOM-002. Em viewport 1280×800, folha de 1184px com quatro colunas; largura menor não reduz fonte automaticamente: folha virtual horizontal com controle “próxima coluna”, ou escolha de modo acessível de uma coluna. A 200% de zoom, modo acessível oferece reflow sem rolagem horizontal e mesma âncora. Ordem de leitura assistiva usa DOM textual contínuo e não quatro cópias do conteúdo. Sem acesso: arquivo removido/token expirado retorna à seleção ou acervo, com motivo visível.
