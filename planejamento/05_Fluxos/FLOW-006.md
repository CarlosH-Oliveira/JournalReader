---
{
  "id": "FLOW-006",
  "etapa": 5,
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
  "avaliacao": "AV-E5",
  "diagrama": "DIAG-005",
  "gate": "Pendente de ratificação humana; avanço documental delegado",
  "aprovado_por": null,
  "aprovado_em": null,
  "commit_pr": null
}
---

# FLOW-006 — Excluir obra do acervo

Ator: leitor local. Objetivo: excluir obra do acervo. Domínios: donos dos núcleos NUC-009, NUC-008, NUC-007, conforme etapa 4. Tela inicial/final: VIEW-004 → VIEW-004. Núcleos: NUC-009, NUC-008, NUC-007 v1.0. Casos: UC-008. Aceites: AC-008.

Pré-condição: sessão local aberta, parâmetros/tokens válidos, revisão existente quando a ação pede uma obra. Entrada: seleção explícita, documento/âncora ou snapshot, conforme UC. Sequência com saídas e contratos: Selecionar obra → mostrar notas e arquivos internos afetados → confirmar → API-007 marca excluindo, bloqueia novas escritas → API-008 transaciona remoção dos vínculos → apagar blobs sem referências → MSG-004 informa conclusão.

Estado inicial → em andamento → sucesso ou erro/cancelado. Estado de sucesso: Obra desaparece após exclusão lógica; resíduos pendentes têm estado e nova tentativa de limpeza. Regras: texto imutável, um dono lógico por dado, geração atual prevalece, confirmação após persistência e acesso só aos arquivos selecionados/acervo.

Exceções e recuperação: Falha antes de commit faz rollback; depois de commit mantém exclusão lógica e pendência visível de limpeza de blobs; original externo nunca tocado. Cenários de atraso/acesso negado/repetição/cancelamento: Operação lenta mostra andamento; ID fora do acervo é negado; repetir exclusão já finalizada retorna concluído; cancelar antes do commit preserva obra. Não há timeout que conclua sucesso por inferência. Requisição/cálculo obsoleto pode ser descartado sem alterar estado autoritativo.

Observabilidade planejada: commandId/jobId, duração, tamanho em faixas, estado e errorCode local; sem texto, notas, caminho absoluto ou consulta de busca. Feedback exibe apenas o conteúdo necessário dentro da janela do leitor. Erro pode ser copiado como diagnóstico redigido pelo próprio usuário; sem envio automático.

Contratos nas fronteiras: serviço de origem valida entrada; destino valida revisão/expectedVersion, erro retorna tipado; UI consulta o estado se perder MSG. Dependências são portas locais da etapa 3, não integrações remotas. Critérios de conclusão acima são verificados por TEST correspondente e contraprovas de falha da etapa 6. O fluxo é proposto, não demonstrado em aplicativo.

AV-5.FLOW-006: inspeção de cinco classes (sucesso/erro, atraso, acesso negado, cancelamento, repetição), com N/A localizado quando cancelamento pós-commit não é reversível; em tal caso há operação de recuperação explícita. Gate humano pendente; limiar automático documental ≥75.
