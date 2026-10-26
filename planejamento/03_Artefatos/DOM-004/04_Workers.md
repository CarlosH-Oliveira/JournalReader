---
{
  "id": "SPEC-DOM-004-JOB",
  "etapa": 3,
  "dominio": "DOM-004",
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

N/A: nenhum job autônomo neste domínio. Composição é cálculo local assíncrono cancelável por geração, ligado à interação UC-003/004; não exige rotina persistente. Acervo executa backup por comando explícito com progresso, sem scheduler. Consumidores recebem retorno/MSG do comando. Não há processamento periódico oculto.

Jobs aplicáveis executam fora da UI, sem permissão de rede. Falha e término são observáveis por MSG-001 ou MSG-003; fechamento encerra o processo, e o próximo início descarta staging não confirmado. Não há alegação de job já implementado.
