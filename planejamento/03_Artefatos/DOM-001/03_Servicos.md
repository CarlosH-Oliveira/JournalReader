---
{
  "id": "SPEC-DOM-001-API",
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

# Contratos locais

| ID | DOM | Casos | Entrada → saída | Validação/autorização | Erros e efeitos |
| --- | --- | --- | --- | --- | --- |
| API-001 | DOM-001 | UC-001, UC-002 | importar(token,commandId,formatHint?) → jobId | Assinatura, tamanho e token válido da sessão; token resolve somente arquivo escolhido | UNSUPPORTED, PROTECTED, LIMIT, INVALID, NO_TEXT; sem efeito final até aceite; repetir commandId devolve mesmo jobId |
| API-002 | DOM-001 | UC-002, UC-003 | confirmar(jobId,acceptedWarnings,commandId) → DocumentoNormalizado | Só sessão que iniciou; estado prévia; warnings críticos aceitos | STALE_STATE, CANCELLED, ORDER_WARNING; confirmação idempotente da mesma revisão; commit via API-008 |

Todas as APIs são interfaces locais, não HTTP. Ações com efeito usam commandId UUID e registro transacional; retenção de deduplicação até exclusão da obra, para restore até substituição do snapshot seguinte. expectedVersion impede sobrescrever atualização concorrente. As entidades lidas/escritas são as do mesmo domínio, mais referências de DATA-001 e DATA-007 pelos contratos da etapa 2. I/O físico delega a API-008. Erros são enums tipados; caminhos e texto não aparecem em logs.
