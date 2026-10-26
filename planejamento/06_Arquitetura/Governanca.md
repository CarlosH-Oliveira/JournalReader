---
{
  "id": "GOV-001",
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

# Governança técnica proposta

Documentos e decisões estão em Proposta. G6 exige ratificação técnica das versões exatas e designação dos papéis. A autorização de produção automática do plano não publica aplicativo nem aceita riscos operacionais. CHG-001 rege passagem documental com 75 e revisão limitada; LIM-001 deve ser resolvida por revisão independente antes de implementação relevante.

Sem conta/servidor, autenticação de produto é N/A. Usuário local do SO é a fronteira; outros usuários do mesmo perfil podem acessar o acervo. Texto/nota pode conter informação sensível; nenhum conteúdo, título, consulta ou caminho absoluto vai para telemetria. Sem coleta automática e sem promessa jurídica de conformidade. Backups em claro exigem aviso e destino escolhido.

Logs locais: IDs técnicos sem conteúdo, duração/errorCode e versão; rotação de sete dias, exclusão pelo usuário. Diagnóstico exportado só por ação explícita e prévia. Relatório não inclui texto/nota/caminho original. Dados canônicos ficam até exclusão; resíduos temporários são limpos no início; backups externos não são apagados pelo aplicativo.

Agentes futuros trabalham em sandbox, com corpus sintético ou autorizado e permissões mínimas. Sem acessar diretórios arbitrários, enviar documentos, registrar credenciais ou instalar serviços externos. Changes que afetem formatos, âncoras, schema ou segurança reabrem origem e descendentes: documento → núcleo → fluxo → ADR/testes. Nunca aprovar a própria mudança como revisão independente.

Plano de migração: schemaVersion monotônico; backup pré-migração, transação e validação de contagens/âncoras. Falha restaura snapshot anterior. Downgrade não abre schema futuro; oferecer restauração compatível. Nenhuma migração executada nesta entrega. Responsável técnico deve provar rollback com falha injetada antes da etapa 7.

Exclusão/restauração futuras exigem confirmação na interface; a presente produção não manipula acervo real. Publicação, assinatura de instalador e atualização exigem autorização própria. Revisão técnica e humana mantém gates G1A/G1B/G2/G3/G4/G5/G6 pendentes até ratificação.
