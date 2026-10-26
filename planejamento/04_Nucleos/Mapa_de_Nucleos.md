---
{
  "id": "MAP-NUC",
  "etapa": 4,
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
  "avaliacao": "AV-E4",
  "diagrama": "DIAG-004",
  "gate": "Pendente de ratificação humana; avanço documental delegado",
  "aprovado_por": null,
  "aprovado_em": null,
  "commit_pr": null
}
---

# Capacidades compostas

| ID | DOM | Tipo | Capacidade | UC | DATA | Artefatos | Dependências | Contrato | AC |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NUC-001 | DOM-001 | back-end local | Aceitar importação | UC-001, UC-002 | DATA-001, DATA-002 | API-001, API-002 | NUC-008 | Aceite entrega revisão persistida ou erro explícito | AC-001, AC-002 |
| NUC-002 | DOM-001 | rotina | Extrair em segundo plano | UC-001, UC-002 | DATA-001, DATA-002 | JOB-001, MSG-001 | NUC-001 | jobId progride até prévia/erro/cancelado; nunca confirma sozinho | AC-001, AC-002 |
| NUC-003 | DOM-001 | interatividade | Importar com prévia | UC-001, UC-002 | DATA-002 | VIEW-001, API-001, API-002, MSG-001 | NUC-001, NUC-002 | Ações de seleção, aceite e cancelamento recebem feedback do estado real | AC-001, AC-002 |
| NUC-004 | DOM-002 | back-end local | Compor e localizar | UC-003, UC-004 | DATA-003, DATA-004; lê DATA-001 | API-003, API-004, MSG-002 | NUC-001 (documento pronto) | Perfil + revisão + viewport geram mapa; versão velha descartada | AC-003, AC-004 |
| NUC-005 | DOM-003 | back-end local | Navegar e persistir leitura | UC-005, UC-006, UC-007 | DATA-005, DATA-006; lê DATA-001 | API-005, API-006, MSG-003 | NUC-004, NUC-008 | Resolve âncora e confirma gravação por commandId ou relata falha | AC-005, AC-006, AC-007 |
| NUC-006 | DOM-003 | rotina | Construir índice | UC-005 | DATA-001 (leitura), índice derivado | JOB-002, MSG-003 | NUC-001 (documento pronto) | Índice compatível com revisão torna busca disponível; falha permite reconstruir | AC-005 |
| NUC-007 | DOM-003 | interatividade | Ler e anotar | UC-003, UC-004, UC-005, UC-006, UC-007 | DATA-003–006 | VIEW-002, VIEW-003, MSG-002, MSG-003 | NUC-004, NUC-005, NUC-006 | Leitor enxerga layout e confirmação de estado; mantém foco/âncora em alterações | AC-003, AC-004, AC-005, AC-006, AC-007 |
| NUC-008 | DOM-004 | back-end local | Persistir e recuperar acervo | UC-008, UC-009; suporte UC-001/002/006/007 | DATA-007, DATA-008; repositórios dos demais donos | API-007, API-008, MSG-004 | Nenhum núcleo síncrono; portas de dados dos domínios | Transação confirma mudanças; restore troca snapshot validado e preserva anterior até sucesso | AC-008, AC-009 |
| NUC-009 | DOM-004 | interatividade | Gerir biblioteca e backup | UC-008, UC-009 | DATA-007, DATA-008 | VIEW-004, MSG-004 | NUC-008, NUC-003 (navegação para importar) | Excluir/restaurar exige confirmação do impacto; cancelamento não altera dados ativos | AC-008, AC-009 |

Componentes referenciam exclusivamente versão 1.0, em estado Proposta. “back-end” significa regra local, sem serviço remoto. Dependências de documento pronto são dados de entrada e não chamada recursiva. NUC-008 não chama NUC-001 nem NUC-005 durante commit; recebe payload tipado e valida namespace.

## Categorias não aplicáveis por domínio

DOM-001: back-end, rotina e interatividade aplicáveis; notificação independente N/A porque MSG-001 integra a mesma operação e VIEW-001, sem capacidade autônoma. DOM-002: só back-end local aplicável; rotina N/A (recomposição vinculada à interação), notificação N/A (status incorporado), interatividade própria N/A (NUC-007 compõe VIEW-002). DOM-003: back-end, rotina e interatividade aplicáveis; notificação independente N/A (MSG-003 é feedback da ação). DOM-004: back-end e interatividade aplicáveis; rotina persistente N/A (backup por comando), notificação independente N/A (MSG-004 incorporado). Não existem e-mails, push ou scheduler.

G4.NUC e G4.DOM permanecem pendentes de ratificação; autoavaliação permite continuidade documental. Nenhuma capacidade essencial está sem executor; eventos não exigem núcleo artificial de notificação.
