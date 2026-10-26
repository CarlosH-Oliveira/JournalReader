---
{
  "id": "FLOW-001",
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

# FLOW-001 — Importar e abrir

Ator: leitor local. Objetivo: importar e abrir. Domínios: donos dos núcleos NUC-009, NUC-003, NUC-001, NUC-002, NUC-008, NUC-004, NUC-007, conforme etapa 4. Tela inicial/final: VIEW-004 → VIEW-001 → VIEW-002. Núcleos: NUC-009, NUC-003, NUC-001, NUC-002, NUC-008, NUC-004, NUC-007 v1.0. Casos: UC-001, UC-002, UC-003. Aceites: AC-001, AC-002, AC-003.

Pré-condição: sessão local aberta, parâmetros/tokens válidos, revisão existente quando a ação pede uma obra. Entrada: seleção explícita, documento/âncora ou snapshot, conforme UC. Sequência com saídas e contratos: Selecionar arquivo → API-001 gera jobId → JOB-001 valida/extrai → MSG-001 atualiza prévia → confirmar API-002 → API-008 grava revisão/obra → API-003 gera layout → leitor exibe quatro colunas.

Estado inicial → em andamento → sucesso ou erro/cancelado. Estado de sucesso: Obra pronta só depois de commit e layout; importação recusada permanece legível no erro. Regras: texto imutável, um dono lógico por dado, geração atual prevalece, confirmação após persistência e acesso só aos arquivos selecionados/acervo.

Exceções e recuperação: Formato inválido/protegido ou sem texto impede pronto; PDF suspeito exige aceite da ordem; sem espaço não abre obra incompleta. Cenários de atraso/acesso negado/repetição/cancelamento: Atraso mostra progresso e botão cancelar; token negado retorna à seleção; repetir commandId recupera job existente; cancelar limpa temporários. Não há timeout que conclua sucesso por inferência. Requisição/cálculo obsoleto pode ser descartado sem alterar estado autoritativo.

Observabilidade planejada: commandId/jobId, duração, tamanho em faixas, estado e errorCode local; sem texto, notas, caminho absoluto ou consulta de busca. Feedback exibe apenas o conteúdo necessário dentro da janela do leitor. Erro pode ser copiado como diagnóstico redigido pelo próprio usuário; sem envio automático.

Contratos nas fronteiras: serviço de origem valida entrada; destino valida revisão/expectedVersion, erro retorna tipado; UI consulta o estado se perder MSG. Dependências são portas locais da etapa 3, não integrações remotas. Critérios de conclusão acima são verificados por TEST correspondente e contraprovas de falha da etapa 6. O fluxo é proposto, não demonstrado em aplicativo.

AV-5.FLOW-001: inspeção de cinco classes (sucesso/erro, atraso, acesso negado, cancelamento, repetição), com N/A localizado quando cancelamento pós-commit não é reversível; em tal caso há operação de recuperação explícita. Gate humano pendente; limiar automático documental ≥75.
