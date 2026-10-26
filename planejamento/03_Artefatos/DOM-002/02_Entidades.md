---
{
  "id": "SPEC-DOM-002-DATA",
  "etapa": 3,
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
  "avaliacao": "AV-E3",
  "diagrama": "DIAG-003",
  "gate": "Pendente de ratificação humana; avanço documental delegado",
  "aprovado_por": null,
  "aprovado_em": null,
  "commit_pr": null
}
---

# Entidades e estados

| ID | DOM | Entidade | Atributos e tipos | Relações | Invariantes/ciclo | Operações |
| --- | --- | --- | --- | --- | --- | --- |
| DATA-003 | DOM-002 | PerfilVisual | profileId UUID, font enum, fontPx int, lineHeight number, theme enum, accessibleMode bool | Um perfil global com sobreposição opcional por obra | 18px padrão; 14–32px; entrelinha 1.3–1.8; mudar perfil incrementa layoutGeneration | Composição cria/altera; leitura consome; acervo persiste |
| DATA-004 | DOM-002 | MapaLayout | docId UUID, revision hash, generation int, viewport rect, pages LayoutPage[], anchorMap ranges | Uma revisão/perfil/viewport gera um mapa; referências a DATA-001, sem cópia autoritativa | Efêmero; calculando → pronto ou falhou; geração antiga nunca substitui atual | Composição cria e descarta; leitura lê; não persistido |

Classificação: texto, títulos, notas e histórico podem conter conteúdo pessoal/sensível fornecido pelo usuário. Necessidade: leitura local e continuidade. Acesso: somente sessão local, sem telemetria de conteúdo. Retenção: até exclusão explícita da obra; temporários de importação são eliminados ao concluir/cancelar e resíduos no próximo início. Backups externos são responsabilidade de retenção do usuário e contêm conteúdo em claro; informar antes de exportar.

Índices e layouts são derivados reconstruíveis. Excluir obra remove dados ativos e temporários; não prometer apagamento forense de SSD, backups do SO ou cópias externas. Arquivo original selecionado permanece intocado. Nova extração cria outra revisão e não migra notas silenciosamente; âncoras incompatíveis são sinalizadas.
