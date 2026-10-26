---
{
  "id": "DOM-002",
  "etapa": 2,
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
  "avaliacao": "AV-E2",
  "diagrama": "DIAG-002",
  "gate": "Pendente de ratificação humana; avanço documental delegado",
  "aprovado_por": null,
  "aprovado_em": null,
  "commit_pr": null
}
---

# DOM-002 — Composição editorial

Objetivo: distribuir texto em quatro colunas. Dono lógico: módulo Composição editorial, responsável humano ainda a designar. Dados: Perfil visual e mapa de layout. Atores: leitor local e eventos internos autorizados da sessão. Features: FEAT-003, FEAT-004.

Vocabulário comum: obra = item catalogado; revisão = extração imutável; bloco = trecho semântico identificado; folha = grupo visual de quatro colunas; âncora = posição lógica independente de folha.

Fronteira: o domínio responde somente por sua capacidade e contratos de Dependencias.md. Não assume propriedade dos dados dos outros domínios; acervo guarda bytes mas não redefine notas, posições ou estrutura semântica. Sem este domínio perde-se a capacidade “distribuir texto em quatro colunas”. Regras e dados específicos estão nas seis subetapas da etapa 3.
