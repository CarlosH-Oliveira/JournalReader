---
{
  "id": "SPEC-DOM-004-UC",
  "etapa": 3,
  "dominio": "DOM-004",
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

# Casos de uso — Acervo e continuidade

Ator padrão: leitor local; permissão: somente arquivo escolhido ou obra de seu acervo local. Eventos automáticos herdam o escopo do comando. Sem papéis remotos.

## UC-008 — Gerir biblioteca e excluir

Feature: FEAT-008. Gatilho: ação explícita do leitor, exceto autosave de UC-006 após navegação. Pré-condição: Acervo aberto; obra selecionada para exclusão.

Fluxo: Listar/filtrar → abrir; para excluir mostrar impacto → confirmar → apagar vínculos e blobs. Pós-condição: Obra removida e sem referências ativas. Exceções: Cancelar preserva tudo; disco falha causa rollback; exclusão pendente de blobs é exibida e retentável. Invariantes: texto canônico imutável, propriedade única e nenhuma confirmação falsa de persistência.

**AC-008** — Dado o contexto da pré-condição, quando o fluxo for acionado, então: Confirmar exclusão remove catálogo, texto, índice e notas vinculadas; arquivos originais fora do acervo nunca são apagados. Verificação planejada: TEST-008. Além disso, negar token de arquivo inválido deve resultar em DENIED sem leitura arbitrária.

## UC-009 — Salvar e restaurar backup

Feature: FEAT-009. Gatilho: ação explícita do leitor, exceto autosave de UC-006 após navegação. Pré-condição: Destino/origem selecionado; espaço estimado suficiente.

Fluxo: Exportar manifesto, documentos e leitura → validar hashes; para restaurar validar e preparar → confirmar → trocar atomicamente. Pós-condição: Snapshot íntegro exportado ou restaurado. Exceções: Backup inválido/incompatível não altera acervo; restauração interrompida mantém snapshot anterior. Invariantes: texto canônico imutável, propriedade única e nenhuma confirmação falsa de persistência.

**AC-009** — Dado o contexto da pré-condição, quando o fluxo for acionado, então: Restaurar backup conhecido em acervo isolado preserva obras/notas/âncoras; hash alterado aborta sem escrever no acervo ativo. Verificação planejada: TEST-009. Além disso, negar token de arquivo inválido deve resultar em DENIED sem leitura arbitrária.

## Universo de cenários críticos avaliado

| Caso | Sucesso | Erro de entrada/estado | Permissão | Repetição |
| --- | --- | --- | --- | --- |
| UC-008 | Pós-condição e AC do caso | Exceção descrita impede conclusão falsa | Token/obra fora do escopo resulta DENIED | Mesmo commandId preserva efeito único em mutação; leitura pura repetida não altera canônico |
| UC-009 | Pós-condição e AC do caso | Exceção descrita impede conclusão falsa | Token/obra fora do escopo resulta DENIED | Mesmo commandId preserva efeito único em mutação; leitura pura repetida não altera canônico |
