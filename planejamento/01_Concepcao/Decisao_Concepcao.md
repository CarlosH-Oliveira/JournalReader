---
{
  "id": "DEC-001",
  "etapa": 1,
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
  "avaliacao": "AV-E1",
  "diagrama": "DIAG-001",
  "gate": "Pendente de ratificação humana; avanço documental delegado",
  "aprovado_por": null,
  "aprovado_em": null,
  "commit_pr": null
}
---

# Escolha provisória de concepção

G1A: MOD-001 v1.0 recomendado e adotado para elaboração automática; ratificação pendente. G1B: SET-003 v1.0; FEAT-001–009 agora, FEAT-010–012 e 014 depois, FEAT-013 fora. G1A não aprova features implicitamente: as escolhas estão registradas em linhas distintas.

Para FEAT-003, “jornal” significa uma única sequência de texto paginada em quatro colunas da esquerda para a direita. Não são quatro matérias independentes. Coluna de altura finita; ordem coluna 1 de cima a baixo, depois 2, 3, 4 e folha seguinte. Títulos e notas de rodapé entram na sequência, sem alteração editorial.

Sucesso inicial: quatro colunas contêm todos os blocos textuais aceitos, na ordem aprovada na prévia; busca alcança o trecho; reabrir retorna à mesma âncora lógica. Metas verificadas com corpus de referência definido no plano da etapa 6. Apenas autorizar leitura após aceitar a prévia quando houver alerta de PDF.

## Critérios iniciais por feature crítica

| Feature | Critério observável inicial |
| --- | --- |
| FEAT-001 | Um TXT UTF-8 conhecido produz os mesmos caracteres e parágrafos lógicos, removendo somente BOM e normalizando finais de linha; tipo não suportado gera erro identificável |
| FEAT-002 | PDF de duas colunas conhecido mostra alerta e prévia; cancelar não insere obra no catálogo; sem texto impede confirmar |
| FEAT-003 | Com corpus de parágrafos numerados, leitura de coluna 1 a 4 e folhas subsequentes recupera cada trecho exatamente uma vez e na ordem |
| FEAT-004 | Mudar fonte 18→24 e modo 4→1→4 mantém o mesmo bloco/offset visível, sem gravar página física como posição |
| FEAT-005 | Busca por frase com acento retorna offset correto; termo ausente mostra zero resultados; navegação integral funciona por teclado |
| FEAT-006 | Reabrir após salvamento confirmado retorna ao mesmo bloco/offset; repetir criar marcador com mesmo commandId não duplica |
| FEAT-007 | Após mudar zoom, destaque cobre o mesmo intervalo; falha de gravação mantém rascunho visível e oferece repetir |
| FEAT-008 | Confirmar exclusão remove catálogo, texto, índice e notas vinculadas; arquivos originais fora do acervo nunca são apagados |
| FEAT-009 | Restaurar backup conhecido em acervo isolado preserva obras/notas/âncoras; hash alterado aborta sem escrever no acervo ativo |
