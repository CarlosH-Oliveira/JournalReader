---
{
  "id": "DOM-MAPA",
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

# Fronteiras de negócio

| ID | Domínio | Propósito | Dado sob propriedade lógica | Features |
| --- | --- | --- | --- | --- |
| DOM-001 | Ingestão | validar e normalizar arquivos | Documento normalizado e diagnósticos | FEAT-001, FEAT-002 |
| DOM-002 | Composição editorial | distribuir texto em quatro colunas | Perfil visual e mapa de layout | FEAT-003, FEAT-004 |
| DOM-003 | Experiência de leitura | navegar, buscar e anotar | Posição, marcadores e anotações | FEAT-005, FEAT-006, FEAT-007 |
| DOM-004 | Acervo e continuidade | catalogar, persistir e recuperar | Catálogo, arquivos e backup | FEAT-008, FEAT-009 |

Alternativa A: três domínios, fundindo composição e leitura. Menor fronteira inicial, mas regras de paginação e notas se misturam. Alternativa B escolhida provisoriamente: quatro domínios; composição calcula layout, leitura decide ação do leitor. Coesão maior, contrato de âncora explícito. Não são microsserviços.

Acervo é autoridade do catálogo e dos bytes persistidos; ingestão é autoridade da estrutura semântica extraída. Localização física não transfere a propriedade lógica. Leitura é dona de notas/posição, composição somente consome âncoras. Sem contas, permissões por equipe ou domínio artificial de autenticação.
