---
{
  "id": "FLOW-004",
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

# FLOW-004 — Retomar e marcar posição

Ator: leitor local. Objetivo: retomar e marcar posição. Domínios: donos dos núcleos NUC-009, NUC-007, NUC-005, NUC-004, NUC-008, conforme etapa 4. Tela inicial/final: VIEW-004 → VIEW-002. Núcleos: NUC-009, NUC-007, NUC-005, NUC-004, NUC-008 v1.0. Casos: UC-006. Aceites: AC-006.

Pré-condição: sessão local aberta, parâmetros/tokens válidos, revisão existente quando a ação pede uma obra. Entrada: seleção explícita, documento/âncora ou snapshot, conforme UC. Sequência com saídas e contratos: Abrir obra → ler EstadoLeitura → validar revisão/âncora → API-004 resolve → exibir; ao navegar API-006 salva com debounce → API-008 commit → MSG-003 confirma; marcador por comando explícito.

Estado inicial → em andamento → sucesso ou erro/cancelado. Estado de sucesso: Reabertura após confirmação retorna à mesma localização; perda antes de commit é explicitada. Regras: texto imutável, um dono lógico por dado, geração atual prevalece, confirmação após persistência e acesso só aos arquivos selecionados/acervo.

Exceções e recuperação: Âncora incompatível mostra órfã e oferece início sem apagar referência; disco cheio exibe não salvo. Cenários de atraso/acesso negado/repetição/cancelamento: Escrita lenta mantém indicador pendente; obra removida encerra sessão; repetir commandId não duplica; ao fechar com pendência perguntar tentar/fechar sem salvar/cancelar. Não há timeout que conclua sucesso por inferência. Requisição/cálculo obsoleto pode ser descartado sem alterar estado autoritativo.

Observabilidade planejada: commandId/jobId, duração, tamanho em faixas, estado e errorCode local; sem texto, notas, caminho absoluto ou consulta de busca. Feedback exibe apenas o conteúdo necessário dentro da janela do leitor. Erro pode ser copiado como diagnóstico redigido pelo próprio usuário; sem envio automático.

Contratos nas fronteiras: serviço de origem valida entrada; destino valida revisão/expectedVersion, erro retorna tipado; UI consulta o estado se perder MSG. Dependências são portas locais da etapa 3, não integrações remotas. Critérios de conclusão acima são verificados por TEST correspondente e contraprovas de falha da etapa 6. O fluxo é proposto, não demonstrado em aplicativo.

AV-5.FLOW-004: inspeção de cinco classes (sucesso/erro, atraso, acesso negado, cancelamento, repetição), com N/A localizado quando cancelamento pós-commit não é reversível; em tal caso há operação de recuperação explícita. Gate humano pendente; limiar automático documental ≥75.
