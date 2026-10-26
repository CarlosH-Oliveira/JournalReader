---
{
  "id": "SPEC-DOM-004-API",
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

# Contratos locais

| ID | DOM | Casos | Entrada → saída | Validação/autorização | Erros e efeitos |
| --- | --- | --- | --- | --- | --- |
| API-007 | DOM-004 | UC-008, UC-009 | gerirAcervo(action,docId?,fileToken?,commandId,confirmed?) → resultado | Ações delete/restore exigem confirmação com resumo; caminho sempre resolvido por token | DENIED, CORRUPT_BACKUP, SCHEMA_NEWER, STORAGE_FULL; delete idempotente; restore substitui snapshot inteiro após validação |
| API-008 | DOM-004 | UC-001, UC-002, UC-006, UC-007, UC-008, UC-009 | persistir(namespace,docId,commandId,expectedVersion,payload) → committedVersion | Canal interno tipado; namespace autoriza ingestão/documento, leitura/notas e composição/perfil; UI sem SQL | VERSION_CONFLICT, IO_ERROR; commit atômico por unidade; consumidores recebem erro verdadeiro, sem sucesso otimista definitivo |

Todas as APIs são interfaces locais, não HTTP. Ações com efeito usam commandId UUID e registro transacional; retenção de deduplicação até exclusão da obra, para restore até substituição do snapshot seguinte. expectedVersion impede sobrescrever atualização concorrente. As entidades lidas/escritas são as do mesmo domínio, mais referências de DATA-001 e DATA-007 pelos contratos da etapa 2. I/O físico delega a API-008. Erros são enums tipados; caminhos e texto não aparecem em logs.
