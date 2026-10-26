---
{
  "id": "FLOW-002",
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

# FLOW-002 — Personalizar e reorganizar

Ator: leitor local. Objetivo: personalizar e reorganizar. Domínios: donos dos núcleos NUC-007, NUC-004, NUC-005, NUC-008, conforme etapa 4. Tela inicial/final: VIEW-002 → VIEW-002. Núcleos: NUC-007, NUC-004, NUC-005, NUC-008 v1.0. Casos: UC-003, UC-004, UC-006. Aceites: AC-003, AC-004, AC-006.

Pré-condição: sessão local aberta, parâmetros/tokens válidos, revisão existente quando a ação pede uma obra. Entrada: seleção explícita, documento/âncora ou snapshot, conforme UC. Sequência com saídas e contratos: Capturar âncora → validar perfil → incrementar generation → API-003 recompõe → API-004 localiza → MSG-002 pronto → salvar perfil/posição e renderizar.

Estado inicial → em andamento → sucesso ou erro/cancelado. Estado de sucesso: Mesma âncora visível com novo perfil, sem duplicar texto. Regras: texto imutável, um dono lógico por dado, geração atual prevalece, confirmação após persistência e acesso só aos arquivos selecionados/acervo.

Exceções e recuperação: Fonte ausente usa fallback informado; generation obsoleta não substitui atual; falha mantém layout anterior. Cenários de atraso/acesso negado/repetição/cancelamento: Recomposição mostra ocupado; obra removida cancela e volta ao acervo; mudança rápida só aplica última geração; desfazer perfil é recuperação. Não há timeout que conclua sucesso por inferência. Requisição/cálculo obsoleto pode ser descartado sem alterar estado autoritativo.

Observabilidade planejada: commandId/jobId, duração, tamanho em faixas, estado e errorCode local; sem texto, notas, caminho absoluto ou consulta de busca. Feedback exibe apenas o conteúdo necessário dentro da janela do leitor. Erro pode ser copiado como diagnóstico redigido pelo próprio usuário; sem envio automático.

Contratos nas fronteiras: serviço de origem valida entrada; destino valida revisão/expectedVersion, erro retorna tipado; UI consulta o estado se perder MSG. Dependências são portas locais da etapa 3, não integrações remotas. Critérios de conclusão acima são verificados por TEST correspondente e contraprovas de falha da etapa 6. O fluxo é proposto, não demonstrado em aplicativo.

AV-5.FLOW-002: inspeção de cinco classes (sucesso/erro, atraso, acesso negado, cancelamento, repetição), com N/A localizado quando cancelamento pós-commit não é reversível; em tal caso há operação de recuperação explícita. Gate humano pendente; limiar automático documental ≥75.
