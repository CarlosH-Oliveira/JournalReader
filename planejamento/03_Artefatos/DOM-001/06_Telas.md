---
{
  "id": "SPEC-DOM-001-VIEW",
  "etapa": 3,
  "dominio": "DOM-001",
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

| ID | DOM dono da composição | UC | Tela | Ações | Campos | Estados |
| --- | --- | --- | --- | --- | --- | --- |
| VIEW-001 | DOM-001 | UC-001, UC-002 | Importação e prévia | Selecionar arquivo; confirmar alertas; cancelar; repetir | Nome/tipo/tamanho, progresso e sequência de blocos; amostra paginada da fonte quando disponível; PDF mostra página de origem | Vazia: convite; carga: progresso e cancelar; erro: motivo e ação; sucesso: abrir; sem acesso: escolher arquivo novamente |

Regras transversais: foco visível, ordem de Tab lógica, nomes acessíveis, status assíncronos anunciados sem repetir a cada bloco. Setas/PageUp/PageDown navegam somente fora de campos; Escape fecha painel e devolve foco. Diálogos de exclusão/restauração têm foco contido e confirmação explícita. Não comunicar estado só por cor; contraste alvo 4,5:1 para texto comum.

VIEW-002 é definida apenas em DOM-003; consome composição de DOM-002. Em viewport 1280×800, folha de 1184px com quatro colunas; largura menor não reduz fonte automaticamente: folha virtual horizontal com controle “próxima coluna”, ou escolha de modo acessível de uma coluna. A 200% de zoom, modo acessível oferece reflow sem rolagem horizontal e mesma âncora. Ordem de leitura assistiva usa DOM textual contínuo e não quatro cópias do conteúdo. Sem acesso: arquivo removido/token expirado retorna à seleção ou acervo, com motivo visível.
