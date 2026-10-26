---
{
  "id": "FLOW-007",
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

# FLOW-007 — Exportar e restaurar backup

Ator: leitor local. Objetivo: exportar e restaurar backup. Domínios: donos dos núcleos NUC-009, NUC-008, conforme etapa 4. Tela inicial/final: VIEW-004 → VIEW-004. Núcleos: NUC-009, NUC-008 v1.0. Casos: UC-009. Aceites: AC-009.

Pré-condição: sessão local aberta, parâmetros/tokens válidos, revisão existente quando a ação pede uma obra. Entrada: seleção explícita, documento/âncora ou snapshot, conforme UC. Sequência com saídas e contratos: Escolher exportar → snapshot consistente → manifesto/hashes → gravar destino temporário → finalizar; restaurar → validar esquema/hashes/limites em staging → mostrar impacto de substituir acervo → confirmar → bloquear escritas → trocar ponteiro de geração → reabrir acervo → MSG-004 conclui.

Estado inicial → em andamento → sucesso ou erro/cancelado. Estado de sucesso: Obras/notas/âncoras equivalentes após restauração; sucesso apenas com geração íntegra ativa. Regras: texto imutável, um dono lógico por dado, geração atual prevalece, confirmação após persistência e acesso só aos arquivos selecionados/acervo.

Exceções e recuperação: Corrupção ou schema futuro aborta; backup não confiável passa pelas mesmas validações de caminho/zip; falha preserva geração anterior; exclusão de cópias externas é manual. Cenários de atraso/acesso negado/repetição/cancelamento: Sem acesso ao destino pede nova seleção; progresso e cancelamento antes da troca; após commit cancelar é N/A, oferecer restaurar snapshot anterior; repetir commandId consulta resultado. Não há timeout que conclua sucesso por inferência. Requisição/cálculo obsoleto pode ser descartado sem alterar estado autoritativo.

Observabilidade planejada: commandId/jobId, duração, tamanho em faixas, estado e errorCode local; sem texto, notas, caminho absoluto ou consulta de busca. Feedback exibe apenas o conteúdo necessário dentro da janela do leitor. Erro pode ser copiado como diagnóstico redigido pelo próprio usuário; sem envio automático.

Contratos nas fronteiras: serviço de origem valida entrada; destino valida revisão/expectedVersion, erro retorna tipado; UI consulta o estado se perder MSG. Dependências são portas locais da etapa 3, não integrações remotas. Critérios de conclusão acima são verificados por TEST correspondente e contraprovas de falha da etapa 6. O fluxo é proposto, não demonstrado em aplicativo.

AV-5.FLOW-007: inspeção de cinco classes (sucesso/erro, atraso, acesso negado, cancelamento, repetição), com N/A localizado quando cancelamento pós-commit não é reversível; em tal caso há operação de recuperação explícita. Gate humano pendente; limiar automático documental ≥75.
