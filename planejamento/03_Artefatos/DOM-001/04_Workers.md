---
{
  "id": "SPEC-DOM-001-JOB",
  "etapa": 3,
  "dominio": "DOM-001",
  "versao": "1.0",
  "estado": "Proposta",
  "fontes": [
    "Normativa v2.0 de 23/10/2026",
    "Solicitação do usuário de 26/10/2026"
  ],
  "ids_relacionados": [],
  "responsavel": "IA autora",
  "revisor": "Autoavaliação; independência não disponível",
  "avaliacao": "AV-E3",
  "diagrama": "DIAG-003",
  "gate": "Pendente de ratificação humana; avanço documental delegado",
  "aprovado_por": null,
  "aprovado_em": null,
  "commit_pr": null
}
---

# Workers e rotinas

| ID | DOM | UC | Objetivo | Gatilho | Dados/resultado | Concorrência, falha e limites |
| --- | --- | --- | --- | --- | --- | --- |
| JOB-001 | DOM-001 | UC-001, UC-002 | Extrair arquivo | API-001 após seleção | DATA-002; gera DATA-001 | Um job pesado por vez; progresso por blocos; sem retry automático de arquivo inválido; falha transitória permite uma tentativa manual com novo attemptId e mesmo commandId lógico; cancelamento a cada bloco; limite 60s sem progresso; nenhum commit parcial |


Jobs aplicáveis executam fora da UI, sem permissão de rede. Falha e término são observáveis por MSG-001 ou MSG-003; fechamento encerra o processo, e o próximo início descarta staging não confirmado. Não há alegação de job já implementado.
