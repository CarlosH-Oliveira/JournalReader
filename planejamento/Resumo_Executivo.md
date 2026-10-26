---
{
  "id": "DOC-GERAL",
  "etapa": 0,
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
  "avaliacao": "Ver Avaliacoes/Painel.md",
  "diagrama": null,
  "gate": "Pendente de ratificação humana; avanço documental delegado",
  "aprovado_por": null,
  "aprovado_em": null,
  "commit_pr": null
}
---

# Um leitor com aparência de jornal

**Proposta escolhida provisoriamente:** aplicativo desktop local, sem conta, que importa TXT, PDF com camada textual e EPUB refluível sem DRM. O documento é convertido em blocos semânticos; a exibição pagina esses blocos em quatro colunas sequenciais. O texto não é resumido, reescrito nem convertido em notícias.

**Qualidade de vida no escopo:** biblioteca, retomada, sumário quando disponível, busca, marcadores, destaques, notas, tema claro/escuro/sépia, ajustes tipográficos, teclado e backup pessoal. Em telas estreitas, quatro colunas permanecem em uma folha virtual com navegação horizontal explícita; modo acessível de uma coluna é uma escolha adicional, preservando a âncora.

**Limites importantes:** PDF não permite prometer ordem perfeita; a prévia deve expor problemas. PDF digitalizado, documentos protegidos e EPUB de layout fixo são diagnosticados e recusados nesta versão. OCR, voz, dicionário, nuvem, mobile e exportação do jornal para PDF ficam para depois. Backup JSON/ZIP é distinto de exportação editorial.

**Arquitetura proposta:** monólito modular desktop, interface TypeScript, runtime Electron isolado, importação em processo utilitário, persistência SQLite e blobs locais, sem API remota ou broker. Versões e dependências devem ser fixadas somente após prova técnica e auditoria de licença.

**Principais provas ainda necessárias:** ordem da extração PDF, paginação real em quatro colunas, estabilidade de âncoras com Unicode e zoom, acessibilidade, limites de memória e restauração após falha. O planejamento descreve como verificar; não comprova funcionamento.
