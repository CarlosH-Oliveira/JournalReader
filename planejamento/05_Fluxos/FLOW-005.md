---
{
  "id": "FLOW-005",
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

# FLOW-005 — Destacar e escrever nota

Ator: leitor local. Objetivo: destacar e escrever nota. Domínios: donos dos núcleos NUC-007, NUC-005, NUC-008, NUC-004, conforme etapa 4. Tela inicial/final: VIEW-002 → VIEW-003 → VIEW-002. Núcleos: NUC-007, NUC-005, NUC-008, NUC-004 v1.0. Casos: UC-007. Aceites: AC-007.

Pré-condição: sessão local aberta, parâmetros/tokens válidos, revisão existente quando a ação pede uma obra. Entrada: seleção explícita, documento/âncora ou snapshot, conforme UC. Sequência com saídas e contratos: Selecionar intervalo DOM → converter em âncoras canônicas → editar nota → API-006 valida e grava via API-008 → MSG-003 confirma → painel lista → ir ao trecho por API-004.

Estado inicial → em andamento → sucesso ou erro/cancelado. Estado de sucesso: Destaque acompanha mesmo intervalo após repaginar; nota salva somente com confirmação. Regras: texto imutável, um dono lógico por dado, geração atual prevalece, confirmação após persistência e acesso só aos arquivos selecionados/acervo.

Exceções e recuperação: Seleção inválida não grava; nota acima do limite pede reduzir; erro de disco preserva rascunho; revisão antiga mostra nota órfã. Cenários de atraso/acesso negado/repetição/cancelamento: Escrita em atraso mostra pendente; obra excluída impede salvar; repetir commandId devolve mesma nota; cancelar antes de salvar descarta somente com aviso se rascunho. Não há timeout que conclua sucesso por inferência. Requisição/cálculo obsoleto pode ser descartado sem alterar estado autoritativo.

Observabilidade planejada: commandId/jobId, duração, tamanho em faixas, estado e errorCode local; sem texto, notas, caminho absoluto ou consulta de busca. Feedback exibe apenas o conteúdo necessário dentro da janela do leitor. Erro pode ser copiado como diagnóstico redigido pelo próprio usuário; sem envio automático.

Contratos nas fronteiras: serviço de origem valida entrada; destino valida revisão/expectedVersion, erro retorna tipado; UI consulta o estado se perder MSG. Dependências são portas locais da etapa 3, não integrações remotas. Critérios de conclusão acima são verificados por TEST correspondente e contraprovas de falha da etapa 6. O fluxo é proposto, não demonstrado em aplicativo.

AV-5.FLOW-005: inspeção de cinco classes (sucesso/erro, atraso, acesso negado, cancelamento, repetição), com N/A localizado quando cancelamento pós-commit não é reversível; em tal caso há operação de recuperação explícita. Gate humano pendente; limiar automático documental ≥75.
