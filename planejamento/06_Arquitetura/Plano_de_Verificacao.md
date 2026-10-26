---
{
  "id": "TEST-PLANO",
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

# Verificações futuras do produto

| ID | Origem | Escopo | Oráculo/aceite | Estado |
| --- | --- | --- | --- | --- |
| TEST-001 | AC-001 | Importar arquivo | Um TXT UTF-8 conhecido produz os mesmos caracteres e parágrafos lógicos, removendo somente BOM e normalizando finais de linha; tipo não suportado gera erro identificável | Planejado; não executado |
| TEST-002 | AC-002 | Revisar extração | PDF de duas colunas conhecido mostra alerta e prévia; cancelar não insere obra no catálogo; sem texto impede confirmar | Planejado; não executado |
| TEST-003 | AC-003 | Compor jornal | Com corpus de parágrafos numerados, leitura de coluna 1 a 4 e folhas subsequentes recupera cada trecho exatamente uma vez e na ordem | Planejado; não executado |
| TEST-004 | AC-004 | Personalizar apresentação | Mudar fonte 18→24 e modo 4→1→4 mantém o mesmo bloco/offset visível, sem gravar página física como posição | Planejado; não executado |
| TEST-005 | AC-005 | Buscar e navegar | Busca por frase com acento retorna offset correto; termo ausente mostra zero resultados; navegação integral funciona por teclado | Planejado; não executado |
| TEST-006 | AC-006 | Retomar e marcar | Reabrir após salvamento confirmado retorna ao mesmo bloco/offset; repetir criar marcador com mesmo commandId não duplica | Planejado; não executado |
| TEST-007 | AC-007 | Destacar e anotar | Após mudar zoom, destaque cobre o mesmo intervalo; falha de gravação mantém rascunho visível e oferece repetir | Planejado; não executado |
| TEST-008 | AC-008 | Gerir biblioteca e excluir | Confirmar exclusão remove catálogo, texto, índice e notas vinculadas; arquivos originais fora do acervo nunca são apagados | Planejado; não executado |
| TEST-009 | AC-009 | Salvar e restaurar backup | Restaurar backup conhecido em acervo isolado preserva obras/notas/âncoras; hash alterado aborta sem escrever no acervo ativo | Planejado; não executado |
| TEST-010 | RISK-001, RISK-005 | Segurança/adversarial | EPUB com scripts/DTD/traversal/bomba e IPC adulterado: nada executa, nada sai do staging, zero rede, nenhum texto sentinela em logs | Planejado |
| TEST-011 | RISK-004, ADR-004 | Falha e rollback | Injetar falha em staging, blob final, commit, ponteiro e início: sempre abre geração anterior ou nova íntegra; sem referência quebrada | Planejado |
| TEST-012 | OBJ-004, RISK-005 | Privacidade | Abrir arquivo com texto sentinela e monitorar rede/logs; nenhum byte do conteúdo em rede/log; backup avisa em claro | Planejado |
| TEST-013 | RISK-006 | Desempenho e limites | Corpus limite/corpus excedente: recusa controlada, cancelar ≤2s; limite de memória alvo 1GiB para 1 milhão de caracteres; sem crash do acervo | Planejado |
| TEST-014 | FEAT-004/005, RISK-007 | Acessibilidade e conforto | Teclado integral, leitor de tela, foco, contraste 4,5:1; zoom 200% modo acessível sem rolagem horizontal; estudo com 5 leitores sem alegar eficácia | Planejado |
| TEST-015 | ADR-001/002/006, RISK-008 | Dependências | Registrar versões, licenças, hashes e vulnerabilidades de Electron, PDF.js, ZIP/XML e SQLite; impedir distribuição com risco alto sem tratamento | Planejado |

## Corpus planejado e critérios de fidelidade

Preparar 24 arquivos sintéticos/abertos com referência legível: 4 TXT (UTF-8, BOM, UTF-16, codificação ambígua), 6 PDFs textuais (simples, duas colunas, ligaduras, hifenização, tabela, notas), 4 EPUB refluíveis (sumário, notas, imagem/alt, capítulos não lineares), 4 recusas (PDF imagem/protegido, EPUB fixo/DRM), 6 adversariais/limites (ZIP traversal, bomb, XML externo, script, arquivo excedente, truncado). Manifesto fixa hash, licença/permissão e saída esperada por arquivo. Ainda não criado nem executado.

Para TXT e EPUB textual suportado: igualdade do texto normalizado conforme regras explícitas, sem reescrita. Para PDF: referência manual de sequência de blocos por página; falha relevante de ordem ou conteúdo exige diagnóstico/rejeição da entrada, não nota de fidelidade fictícia. Para layout: sequência de intervalos concatenada deve reconstruir o documento uma vez; contagens não bastam sem ordem e Unicode.

Metas de desempenho hipotéticas em máquina piloto 4 núcleos, 8GiB RAM, SSD: obra de 1 milhão de caracteres abre layout inicial em até 3s após normalização; importação até 30s para corpus comum; feedback de ação em até 250ms; cancelamento até 2s; avanço de folha p95 até 100ms em 100 ações após aquecimento. Medir 10 execuções frias por classe e registrar distribuição, ambiente e versões. Nenhuma meta é benchmark já obtido.

Camadas previstas: unitários de normalização/âncoras/invariantes; integração de parser–documento–persistência; contratos IPC; E2E das sete jornadas com falha; inspeção manual de extração/acessibilidade e prova de segurança. Defeito injetado deve fazer a verificação falhar para provar sensibilidade.

EV-001–015 reservados a evidências futuras dos TEST correspondentes; não há evidências de produto nesta entrega. Registrar comando, ambiente, versão, corpus, resultado esperado/obtido, captura redigida quando necessário e limites. A aceitação requer revisão independente e gate humano; 75 documental não substitui o teste funcional.
