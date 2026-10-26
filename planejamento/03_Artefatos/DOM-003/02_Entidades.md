---
{
  "id": "SPEC-DOM-003-DATA",
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

# Entidades e estados

| ID | DOM | Entidade | Atributos e tipos | Relações | Invariantes/ciclo | Operações |
| --- | --- | --- | --- | --- | --- | --- |
| DATA-005 | DOM-003 | EstadoLeitura | docId UUID, revision hash, anchor Anchor, updatedAt instant, saveState enum | Obra 1:1 posição atual por instalação | Anchor = revision + blockId + offset UTF-16 no texto canônico; não cortar surrogate/grapheme; página não é identidade | Leitura cria/altera; acervo persiste; exclusão da obra elimina estado |
| DATA-006 | DOM-003 | Anotacao | annotationId UUID, commandId UUID, docId UUID, revision hash, start Anchor, end Anchor?, kind enum, color enum?, note string? | Obra 1:N anotações; marcador tem end null; destaque usa intervalo [start,end) | Ativa → editada ou excluída; revisão ausente → órfã com aviso; nota até 10000 caracteres | Leitor cria/lê/altera/exclui via leitura; conteúdo privado local |

Classificação: texto, títulos, notas e histórico podem conter conteúdo pessoal/sensível fornecido pelo usuário. Necessidade: leitura local e continuidade. Acesso: somente sessão local, sem telemetria de conteúdo. Retenção: até exclusão explícita da obra; temporários de importação são eliminados ao concluir/cancelar e resíduos no próximo início. Backups externos são responsabilidade de retenção do usuário e contêm conteúdo em claro; informar antes de exportar.

Índices e layouts são derivados reconstruíveis. Excluir obra remove dados ativos e temporários; não prometer apagamento forense de SSD, backups do SO ou cópias externas. Arquivo original selecionado permanece intocado. Nova extração cria outra revisão e não migra notas silenciosamente; âncoras incompatíveis são sinalizadas.
