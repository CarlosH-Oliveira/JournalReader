---
{
  "id": "IDEA-001",
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

# IDEA-001 — origem e interpretação

## Solicitação literal

“Execute de forma automática a produção de um planejamento de software (até a etapa 6 da normativa anexada neste projeto) para um aplicativo cujo objetivo é Transformar formatos diversos de texto, como txt, pdf e epub, em jornais estilizados de 4 colunas de texto ( apenas uma formatação de texto adaptada ). A ideia é que a aplicação também tenha diversas funcionalidades de qualidade de vida para leitura, como outros leitores de epub existentes. Itere por conta própria sobre as 6 etapas e só avance para a próxima etapa quando a avaliação de métricas da etapa anterior bater no mínimo 75 pontos de 100. Ao final do processo, gere um arquivo .zip com o planejamento e uma imagem por etapa sumarizando o conteúdo”

## Interpretação separada

Público hipotético: leitores de livros e textos longos em computador. Necessidade: ler conteúdo próprio em apresentação editorial compacta, mantendo continuidade e controle visual. Problema ainda não validado com usuários. Idioma inicial da interface: pt-BR; textos Unicode em escrita horizontal da esquerda para a direita. Não prometer suporte editorial completo a escrita vertical/RTL.

OBJ-001: importar sem adulterar texto; aferir comparação entre blocos extraídos e corpus de referência. OBJ-002: apresentar quatro colunas em ordem contínua sem saltos/duplicações; aferir contagem e percurso dos blocos. OBJ-003: retomar, buscar e anotar com estabilidade; aferir âncora antes/depois de reabrir e alterar fonte. OBJ-004: manter conteúdo local; aferir tráfego zero ao abrir documento e escopo dos arquivos acessados.

Hipóteses H-001: desktop é melhor ponto inicial; validar com cinco leitores antes da etapa 7. H-002: quatro colunas melhoram conforto; comparar tarefa de 15 minutos em uma e quatro colunas, sem afirmar ganho prévio. H-003: corpus predominantemente textual; validar amostra antes de ampliar formatos. Falha das hipóteses reabre G1A/G1B, sem descartar todo o plano.

Não objetivos: editar conteúdo, sumarizar com IA, montar manchetes ou múltiplas matérias, servir notícias, operar loja, remover DRM ou publicar documentos.
