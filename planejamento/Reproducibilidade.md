---
{
  "id": "REPRO-001",
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

# Fontes editáveis e reprodução

Os documentos Markdown e SVG são editáveis. As seis imagens PNG são sínteses reproduzíveis por `ferramentas/avaliar.py`; os mapas Mermaid detalhados não foram renderizados neste ambiente.

As ferramentas opcionais precisam de Python 3.11+ e Pillow. Não são código do aplicativo. Em cópia de trabalho deste pacote, executar pela ordem: `python ferramentas/produzir.py 0`, `python ferramentas/produzir.py 1`, `python ferramentas/avaliar.py 1`, `python ferramentas/produzir.py 2`, `python ferramentas/avaliar.py 2`, `python ferramentas/produzir.py 3`, `python ferramentas/avaliar.py 3`, `python ferramentas/completar.py 4`, `python ferramentas/completar.py 5`, `python ferramentas/completar.py 6`, `python ferramentas/diagramas_e_auditoria.py`. São geradores documentais determinísticos de conteúdo; a autoavaliação codificada não equivale a avaliação independente de qualidade.

Não regenerar sobre documentos humanos já aprovados: usar cópia de trabalho e revisar diffs. A sequência reavalia o mínimo anterior antes de produzir a próxima etapa; N/A não recebe nota. As ferramentas reproduzem os catálogos e imagens, enquanto o painel final desta entrega registra os denominadores corrigidos. `verificar.py` inspeciona integridade estrutural sem escrever dados do usuário.

A normative fonte é cópia exata do anexo fornecido neste projeto. Nenhum conteúdo de outros projetos ou bibliotecas pessoais foi consultado.
