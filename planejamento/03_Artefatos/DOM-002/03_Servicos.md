---
{
  "id": "SPEC-DOM-002-API",
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

# Contratos locais

| ID | DOM | Casos | Entrada → saída | Validação/autorização | Erros e efeitos |
| --- | --- | --- | --- | --- | --- |
| API-003 | DOM-002 | UC-003, UC-004 | compor(docId,revision,profile,viewport,generation) → MapaLayout | Revisão pronta; perfil validado; viewport >0; documento acessível ao processo local | INVALID_PROFILE, LAYOUT_FAILED, STALE_GENERATION; não altera texto; preserva último layout utilizável |
| API-004 | DOM-002 | UC-005, UC-006, UC-007 | localizar(anchor,generation) → page,column,rangeRect | Âncora na revisão e geração correntes | ORPHAN_ANCHOR, STALE_GENERATION; sem side effect; coordenadas são efêmeras |

Todas as APIs são interfaces locais, não HTTP. Ações com efeito usam commandId UUID e registro transacional; retenção de deduplicação até exclusão da obra, para restore até substituição do snapshot seguinte. expectedVersion impede sobrescrever atualização concorrente. As entidades lidas/escritas são as do mesmo domínio, mais referências de DATA-001 e DATA-007 pelos contratos da etapa 2. I/O físico delega a API-008. Erros são enums tipados; caminhos e texto não aparecem em logs.
