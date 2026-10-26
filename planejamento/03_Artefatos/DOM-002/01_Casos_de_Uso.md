---
{
  "id": "SPEC-DOM-002-UC",
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

# Casos de uso — Composição editorial

Ator padrão: leitor local; permissão: somente arquivo escolhido ou obra de seu acervo local. Eventos automáticos herdam o escopo do comando. Sem papéis remotos.

## UC-003 — Compor jornal

Feature: FEAT-003. Gatilho: ação explícita do leitor, exceto autosave de UC-006 após navegação. Pré-condição: Documento confirmado, folha virtual definida.

Fluxo: Medir blocos/fontes → distribuir sequencialmente em quatro colunas → mostrar folha. Pós-condição: Mapa de layout cobre todo o texto e permite folha seguinte. Exceções: Palavra longa quebra visualmente; repaginação abortada mantém layout anterior. Invariantes: texto canônico imutável, propriedade única e nenhuma confirmação falsa de persistência.

**AC-003** — Dado o contexto da pré-condição, quando o fluxo for acionado, então: Com corpus de parágrafos numerados, leitura de coluna 1 a 4 e folhas subsequentes recupera cada trecho exatamente uma vez e na ordem. Verificação planejada: TEST-003. Além disso, negar token de arquivo inválido deve resultar em DENIED sem leitura arbitrária.

## UC-004 — Personalizar apresentação

Feature: FEAT-004. Gatilho: ação explícita do leitor, exceto autosave de UC-006 após navegação. Pré-condição: Documento aberto com âncora atual.

Fluxo: Selecionar fonte/tamanho/tema ou modo acessível → recompor → reposicionar. Pós-condição: Perfil salvo e âncora preservada. Exceções: Fonte indisponível: fallback informado; largura pequena mantém folha virtual e oferece modo acessível. Invariantes: texto canônico imutável, propriedade única e nenhuma confirmação falsa de persistência.

**AC-004** — Dado o contexto da pré-condição, quando o fluxo for acionado, então: Mudar fonte 18→24 e modo 4→1→4 mantém o mesmo bloco/offset visível, sem gravar página física como posição. Verificação planejada: TEST-004. Além disso, negar token de arquivo inválido deve resultar em DENIED sem leitura arbitrária.

## Universo de cenários críticos avaliado

| Caso | Sucesso | Erro de entrada/estado | Permissão | Repetição |
| --- | --- | --- | --- | --- |
| UC-003 | Pós-condição e AC do caso | Exceção descrita impede conclusão falsa | Token/obra fora do escopo resulta DENIED | Mesmo commandId preserva efeito único em mutação; leitura pura repetida não altera canônico |
| UC-004 | Pós-condição e AC do caso | Exceção descrita impede conclusão falsa | Token/obra fora do escopo resulta DENIED | Mesmo commandId preserva efeito único em mutação; leitura pura repetida não altera canônico |
