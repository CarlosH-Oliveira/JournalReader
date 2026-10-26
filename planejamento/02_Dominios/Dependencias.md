---
{
  "id": "DEP-001",
  "etapa": 2,
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
  "avaliacao": "AV-E2",
  "diagrama": "DIAG-002",
  "gate": "Pendente de ratificação humana; avanço documental delegado",
  "aprovado_por": null,
  "aprovado_em": null,
  "commit_pr": null
}
---

# Contratos entre domínios

| Origem | Destino | Motivo | Contrato |
| --- | --- | --- | --- |
| DOM-004 | DOM-001 | Importar bytes selecionados | API-001; token de sessão |
| DOM-001 | DOM-004 | Confirmar documento e diagnóstico | API-008; documento imutável/revisão |
| DOM-002 | DOM-001 | Consumir blocos prontos | DocumentoNormalizado v1; API-002 |
| DOM-003 | DOM-002 | Solicitar layout e localizar âncora | API-003/004 |
| DOM-003 | DOM-004 | Persistir posição e notas | API-008; namespace de leitura |
| DOM-004 | DOM-003 | Excluir/restaurar dados vinculados | API-006/007; política de revisão |

As relações de solicitação/resposta podem ser bidirecionais; o grafo de execução não admite reentrada síncrona circular. Acervo orquestra importação por transação: não chama ingestão de dentro de callback de confirmação. Composição é pura sobre documento pronto; leitura não escreve documento. Apenas acervo faz I/O físico, a pedido dos donos lógicos. Cada camada expõe portas sem importar a UI.
