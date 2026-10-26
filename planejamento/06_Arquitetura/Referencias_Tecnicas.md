---
{
  "id": "REF-TECNICAS",
  "etapa": 6,
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
  "avaliacao": "AV-E6",
  "diagrama": "DIAG-006",
  "gate": "Pendente de ratificação humana; avanço documental delegado",
  "aprovado_por": null,
  "aprovado_em": null,
  "commit_pr": null
}
---

# Fontes primárias e limites — consulta 26/10/2026

| ID | Fonte | Fato limitado observado | Uso / hipótese da proposta |
| --- | --- | --- | --- |
| REF-004 | https://www.electronjs.org/docs/latest/tutorial/security/ | Documentação recomenda isolamento e cuidados com conteúdo/IPC | Configuração explícita em ADR-006; não prova segurança do produto |
| REF-005 | https://www.electronjs.org/docs/latest/tutorial/sandbox | Acesso privilegiado pode escapar por bridge/preload | Parser em outro processo também precisa privilégio mínimo |
| REF-006 | https://sqlite.org/atomiccommit.html | Transações do SQLite têm mecanismo de commit atômico | Consistência com blobs externos exige protocolo adicional |
| REF-007 | https://www.sqlite.org/lang_transaction.html | COMMIT pode falhar e transação pede tratamento | Erros e retry explícitos em API-008 |
| REF-008 | https://mozilla.github.io/pdf.js/getting_started/ | PDF.js expõe camadas de processamento e exibição | Candidato a parser, sem garantia de ordem textual |
| REF-009 | https://github.com/mozilla/pdf.js/blob/master/examples/node/getinfo.mjs | Exemplo oficial usa getTextContent | Viabilidade de extração a confirmar no corpus |
| REF-010 | https://www.w3.org/TR/css-multicol-1/ | Especifica column-count e column-fill | Paginação e mapeamento ainda são trabalho do aplicativo |
| REF-003 | https://www.w3.org/TR/epub-33/ | Spine define ordem primária | Parser deve respeitar capítulos e sinalizar recursos não suportados |

Fontes pesquisadas; não se testou combinação de runtime, bibliotecas e formatos. Decisões são inferências de engenharia explicitamente propostas. Sem versões, licenças ou desempenho inventados.
