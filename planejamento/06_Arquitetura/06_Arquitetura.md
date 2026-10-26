---
{
  "id": "ARCH-001",
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

# Arquitetura proposta

Seis componentes lógicos, justificados por fluxos: (1) shell desktop/UI e bridge, FLOW-001–007; (2) módulo ingestão e adaptadores, FLOW-001; (3) módulo composição, FLOW-001/002; (4) módulo leitura/índice, FLOW-003–005; (5) módulo acervo/repositórios, FLOW-001/004–007; (6) processo utilitário de tarefas, FLOW-001/003. SQLite e filesystem são recursos de persistência do componente 5, não domínios novos.

Camada privilegiada faz seleção de arquivo, tokens e escrita. UI em renderizador isolado contém conteúdo sanitizado, nunca o HTML arbitrário do EPUB. O processo de importação recebe bytes/recursos limitados, sem acesso amplo ao disco ou rede. Nenhuma API remota, autenticação, broker, nuvem ou servidor. Proteção de sessão herda a conta do sistema operacional; não se promete segurança em computador compartilhado desbloqueado.

Stack candidata: Electron/TypeScript/HTML/CSS, SQLite, PDF.js e bibliotecas ZIP/XML escolhidas após prova técnica e auditoria. Não definir versões inventadas ou “última versão” no plano; registrar versões exatas e licenças antes da etapa 7. Sem necessidade de framework React neste estágio.

Caminho: arquivo selecionado → token → validação/adaptador → DocumentoNormalizado → prévia/aceite → persistência → composição de quatro colunas → ação de leitura → âncora/nota → persistência. Índice e layout são descartáveis; texto/revisões/notas são canônicos.

Estrutura proposta, sem código implementado: `src/domains/{ingestao,composicao,leitura,acervo}`; `src/desktop/{main,preload}`; `src/ui`; `src/tasks`; contratos compartilhados sem regra de negócio. A etapa 7 poderá materializar essa estrutura.

Distribuição futura: desktop, plataforma piloto a confirmar; hipótese inicial Windows 11 x64, demais SOs após validar caminhos/fontes/sandbox. Empacotamento/assinatura, atualização e deploy ficam pendentes de autorização técnica. Não há publicação neste planejamento. Adoção do runtime depende de aprovação de ADR-001/006 e das provas da matriz de verificação.
