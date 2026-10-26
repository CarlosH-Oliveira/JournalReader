---
{
  "id": "SPEC-DOM-003-UC",
  "etapa": 3,
  "dominio": "DOM-003",
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

# Casos de uso — Experiência de leitura

Ator padrão: leitor local; permissão: somente arquivo escolhido ou obra de seu acervo local. Eventos automáticos herdam o escopo do comando. Sem papéis remotos.

## UC-005 — Buscar e navegar

Feature: FEAT-005. Gatilho: ação explícita do leitor, exceto autosave de UC-006 após navegação. Pré-condição: Documento pronto aberto.

Fluxo: Buscar literal → listar resultados → escolher trecho; navegar sumário/folhas. Pós-condição: Âncora do trecho torna-se posição atual. Exceções: Sem ocorrência: estado vazio; arquivo sem sumário: entrada ausente com explicação; índice em carga tem progresso. Invariantes: texto canônico imutável, propriedade única e nenhuma confirmação falsa de persistência.

**AC-005** — Dado o contexto da pré-condição, quando o fluxo for acionado, então: Busca por frase com acento retorna offset correto; termo ausente mostra zero resultados; navegação integral funciona por teclado. Verificação planejada: TEST-005. Além disso, negar token de arquivo inválido deve resultar em DENIED sem leitura arbitrária.

## UC-006 — Retomar e marcar

Feature: FEAT-006. Gatilho: ação explícita do leitor, exceto autosave de UC-006 após navegação. Pré-condição: Obra aberta; posição válida.

Fluxo: Mover leitura → salvar âncora → fechar/reabrir; adicionar marcador. Pós-condição: Posição confirmada e marcador persistem. Exceções: Falha de disco mostra não salvo; âncora inválida não desloca silenciosamente para outro capítulo. Invariantes: texto canônico imutável, propriedade única e nenhuma confirmação falsa de persistência.

**AC-006** — Dado o contexto da pré-condição, quando o fluxo for acionado, então: Reabrir após salvamento confirmado retorna ao mesmo bloco/offset; repetir criar marcador com mesmo commandId não duplica. Verificação planejada: TEST-006. Além disso, negar token de arquivo inválido deve resultar em DENIED sem leitura arbitrária.

## UC-007 — Destacar e anotar

Feature: FEAT-007. Gatilho: ação explícita do leitor, exceto autosave de UC-006 após navegação. Pré-condição: Seleção textual válida em revisão atual.

Fluxo: Selecionar → escolher cor e nota → salvar → listar/editar/remover. Pós-condição: Nota vinculada a intervalo lógico, não a coordenadas. Exceções: Seleção entre colunas mantém continuidade; âncora órfã é sinalizada, nunca perdida sem aviso. Invariantes: texto canônico imutável, propriedade única e nenhuma confirmação falsa de persistência.

**AC-007** — Dado o contexto da pré-condição, quando o fluxo for acionado, então: Após mudar zoom, destaque cobre o mesmo intervalo; falha de gravação mantém rascunho visível e oferece repetir. Verificação planejada: TEST-007. Além disso, negar token de arquivo inválido deve resultar em DENIED sem leitura arbitrária.

## Universo de cenários críticos avaliado

| Caso | Sucesso | Erro de entrada/estado | Permissão | Repetição |
| --- | --- | --- | --- | --- |
| UC-005 | Pós-condição e AC do caso | Exceção descrita impede conclusão falsa | Token/obra fora do escopo resulta DENIED | Mesmo commandId preserva efeito único em mutação; leitura pura repetida não altera canônico |
| UC-006 | Pós-condição e AC do caso | Exceção descrita impede conclusão falsa | Token/obra fora do escopo resulta DENIED | Mesmo commandId preserva efeito único em mutação; leitura pura repetida não altera canônico |
| UC-007 | Pós-condição e AC do caso | Exceção descrita impede conclusão falsa | Token/obra fora do escopo resulta DENIED | Mesmo commandId preserva efeito único em mutação; leitura pura repetida não altera canônico |
