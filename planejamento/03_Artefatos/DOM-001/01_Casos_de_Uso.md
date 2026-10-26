---
{
  "id": "SPEC-DOM-001-UC",
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

# Casos de uso — Ingestão

Ator padrão: leitor local; permissão: somente arquivo escolhido ou obra de seu acervo local. Eventos automáticos herdam o escopo do comando. Sem papéis remotos.

## UC-001 — Importar arquivo

Feature: FEAT-001. Gatilho: ação explícita do leitor, exceto autosave de UC-006 após navegação. Pré-condição: Arquivo local selecionado e dentro dos limites.

Fluxo: Validar assinatura/tamanho → detectar tipo → extrair blocos → gerar prévia. Pós-condição: Documento pronto somente depois de confirmação. Exceções: Arquivo protegido, vazio ou inválido: recusar sem criar obra pronta. Invariantes: texto canônico imutável, propriedade única e nenhuma confirmação falsa de persistência.

**AC-001** — Dado o contexto da pré-condição, quando o fluxo for acionado, então: Um TXT UTF-8 conhecido produz os mesmos caracteres e parágrafos lógicos, removendo somente BOM e normalizando finais de linha; tipo não suportado gera erro identificável. Verificação planejada: TEST-001. Além disso, negar token de arquivo inválido deve resultar em DENIED sem leitura arbitrária.

## UC-002 — Revisar extração

Feature: FEAT-002. Gatilho: ação explícita do leitor, exceto autosave de UC-006 após navegação. Pré-condição: Extração concluída em estado de prévia.

Fluxo: Mostrar fonte, blocos, ordem estimada e alertas → aceitar ou cancelar. Pós-condição: Aceite grava revisão imutável; cancelar remove temporários. Exceções: PDF sem texto: informar OCR indisponível; ordem suspeita exige aceite explícito. Invariantes: texto canônico imutável, propriedade única e nenhuma confirmação falsa de persistência.

**AC-002** — Dado o contexto da pré-condição, quando o fluxo for acionado, então: PDF de duas colunas conhecido mostra alerta e prévia; cancelar não insere obra no catálogo; sem texto impede confirmar. Verificação planejada: TEST-002. Além disso, negar token de arquivo inválido deve resultar em DENIED sem leitura arbitrária.

## Universo de cenários críticos avaliado

| Caso | Sucesso | Erro de entrada/estado | Permissão | Repetição |
| --- | --- | --- | --- | --- |
| UC-001 | Pós-condição e AC do caso | Exceção descrita impede conclusão falsa | Token/obra fora do escopo resulta DENIED | Mesmo commandId preserva efeito único em mutação; leitura pura repetida não altera canônico |
| UC-002 | Pós-condição e AC do caso | Exceção descrita impede conclusão falsa | Token/obra fora do escopo resulta DENIED | Mesmo commandId preserva efeito único em mutação; leitura pura repetida não altera canônico |
