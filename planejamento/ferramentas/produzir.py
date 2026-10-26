from pathlib import Path
import json, shutil, re, hashlib, zipfile, textwrap, sys, html
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent.parent
DATE='2026-10-26'
STAGES=['01_Concepcao','02_Dominios','03_Artefatos','04_Nucleos','05_Fluxos','06_Arquitetura']
DOMS=[('DOM-001','Ingestão','validar e normalizar arquivos','Documento normalizado e diagnósticos','FEAT-001, FEAT-002'),('DOM-002','Composição editorial','distribuir texto em quatro colunas','Perfil visual e mapa de layout','FEAT-003, FEAT-004'),('DOM-003','Experiência de leitura','navegar, buscar e anotar','Posição, marcadores e anotações','FEAT-005, FEAT-006, FEAT-007'),('DOM-004','Acervo e continuidade','catalogar, persistir e recuperar','Catálogo, arquivos e backup','FEAT-008, FEAT-009')]
FEATURES=[('FEAT-001','Importar TXT, PDF textual e EPUB refluível','agora','DOM-001'),('FEAT-002','Diagnóstico e prévia da extração','agora','DOM-001'),('FEAT-003','Jornal paginado com quatro colunas','agora','DOM-002'),('FEAT-004','Fonte, espaçamento, tema e modo acessível','agora','DOM-002'),('FEAT-005','Sumário, busca e navegação por teclado','agora','DOM-003'),('FEAT-006','Retomar posição e criar marcadores','agora','DOM-003'),('FEAT-007','Destaques e notas locais','agora','DOM-003'),('FEAT-008','Biblioteca local e exclusão completa','agora','DOM-004'),('FEAT-009','Exportar/importar backup pessoal','agora','DOM-004'),('FEAT-010','Leitura em voz alta e dicionário','depois','DOM-003'),('FEAT-011','OCR de PDF digitalizado','depois','DOM-001'),('FEAT-012','Sincronização e aplicativos móveis','depois','DOM-004'),('FEAT-013','Reescrita, resumo IA e seleção de notícias','fora','—'),('FEAT-014','Exportar jornal diagramado como PDF','depois','DOM-002')]
def write(rel,body,id='DOC-GERAL',stage=0,dom=None,related=None,version='1.0'):
 p=ROOT/rel;p.parent.mkdir(parents=True,exist_ok=True)
 meta={'id':id,'etapa':stage,'dominio':dom,'versao':version,'estado':'Proposta','fontes':['Normativa v2.0 de 23/10/2026','Solicitação do usuário de 26/10/2026'],'ids_relacionados':related or [],'responsavel':'IA autora','revisor':'Autoavaliação; independência não disponível','avaliacao':f'AV-E{stage}' if stage else 'Ver Avaliacoes/Painel.md','diagrama':f'DIAG-00{stage}' if stage else None,'gate':'Pendente de ratificação humana; avanço documental delegado','aprovado_por':None,'aprovado_em':None,'commit_pr':None}
 p.write_text('---\n'+json.dumps(meta,ensure_ascii=False,indent=2)+'\n---\n\n'+body.strip()+'\n',encoding='utf-8')
def table(headers,rows):return '| '+' | '.join(headers)+' |\n| '+' | '.join(['---']*len(headers))+' |\n'+''.join('| '+' | '.join(map(str,r))+' |\n' for r in rows)
def intro():
 assert (ROOT/'Normativa_Fonte.md').is_file(), 'Normativa fonte ausente'
 write('README.md','''# Leitor de Jornal — planejamento até a etapa 6

Versão 1.0 • 26/10/2026 • proposta documental, sem implementação.

Transformar textos próprios em uma experiência editorial de quatro colunas, preservando o conteúdo e acrescentando conforto de leitura. Comece por `Resumo_Executivo.md`, leia as seis pastas em ordem e consulte `Avaliacoes/Painel.md` e `Rastreabilidade.md`.

Cada etapa possui Markdown canônico e uma imagem PNG em `imagens/`; o SVG correspondente é editável. Os diagramas detalhados das subetapas estão em `diagramas/` em Mermaid. O script `reproduzir.py` reproduz os artefatos; `verificar.py` verifica integridade, sem substituir revisão semântica humana.

## Como interpretar o resultado

A instrução do usuário autoriza seleção provisória de opções e avanço automático documental com IQE ≥75. CHG-001 registra a adaptação do limiar normativo de 80 e dos gates humanos de passagem. Nenhuma autorização para desenvolver, publicar, acessar arquivos do usuário ou tratar conteúdo real foi presumida. Estados continuam Proposta; aprovação por humano = null.

A autoavaliação usa a fórmula normativa e notas máximas 3/4 por dimensão: IQE máximo 75. Não há revisão independente de sessão/contexto; isso limita a confiança. O pacote satisfaz o limiar solicitado para elaboração, mas não declara conformidade estrita com os gates originais, prontidão de implementação ou validação de usabilidade/mercado. Maturidade efetiva M3.

Todos os resultados de desempenho e acessibilidade são metas de teste futuro. Nenhum parser, protótipo do aplicativo ou teste funcional foi executado. As verificações realizadas aqui se referem exclusivamente aos documentos, IDs, imagens e ZIP.
''')
 write('Governanca_Adaptacao.md','''# CHG-001 — execução documental automática

Origem: pedido explícito de produção automática das etapas 1–6 e avanço somente com nota mínima 75/100. A normativa anexada está identificada como proposta pendente de aprovação humana. Adotá-la como estrutura de planejamento não equivale a aprová-la integralmente.

Antes → depois: limiar documental 80 → 75; escolha humana em cada passagem → escolha provisória pela IA dentro da finalidade descrita. Os gates originais permanecem pendentes de ratificação de versões exatas. Não registrar aprovação humana de decisões ainda não vistas.

Notas C/K/R/E/G de 0 a 4, pesos 25/25/20/20/10. IQE = 25C/4 + 25K/4 + 20R/4 + 20E/4 + 10G/4. Sem revisão independente, máximo 3 por dimensão. Uma unidade abaixo de 75 ou com requisito crítico sem dono/contraditório bloqueia a elaboração da próxima etapa até correção. N/A é exclusão fundamentada, jamais 0/0=100%.

Revisão: inspeção integral dos itens críticos pela mesma IA e verificação estrutural por script. Script não é IA revisora independente. Falta de independência é limitação de governança aberta (LIM-001); nenhuma nota 4 atribuída. Os riscos altos de produto são cenários futuros com controles, e não defeitos críticos abertos de software entregue.

Escopo ratificável: MOD-001, SET-003, FEAT-001–009, DOM-001–004 e artefatos v1.0 das etapas 1–6. Futuro responsável de produto/técnico ainda não designado. Agentes futuros não podem publicar, instalar integrações, enviar conteúdo ou apagar dados fora de sandbox sem autorização pertinente. Sem etapa 7, tickets ou código do aplicativo.
''',id='CHG-001')
 write('Resumo_Executivo.md','''# Um leitor com aparência de jornal

**Proposta escolhida provisoriamente:** aplicativo desktop local, sem conta, que importa TXT, PDF com camada textual e EPUB refluível sem DRM. O documento é convertido em blocos semânticos; a exibição pagina esses blocos em quatro colunas sequenciais. O texto não é resumido, reescrito nem convertido em notícias.

**Qualidade de vida no escopo:** biblioteca, retomada, sumário quando disponível, busca, marcadores, destaques, notas, tema claro/escuro/sépia, ajustes tipográficos, teclado e backup pessoal. Em telas estreitas, quatro colunas permanecem em uma folha virtual com navegação horizontal explícita; modo acessível de uma coluna é uma escolha adicional, preservando a âncora.

**Limites importantes:** PDF não permite prometer ordem perfeita; a prévia deve expor problemas. PDF digitalizado, documentos protegidos e EPUB de layout fixo são diagnosticados e recusados nesta versão. OCR, voz, dicionário, nuvem, mobile e exportação do jornal para PDF ficam para depois. Backup JSON/ZIP é distinto de exportação editorial.

**Arquitetura proposta:** monólito modular desktop, interface TypeScript, runtime Electron isolado, importação em processo utilitário, persistência SQLite e blobs locais, sem API remota ou broker. Versões e dependências devem ser fixadas somente após prova técnica e auditoria de licença.

**Principais provas ainda necessárias:** ordem da extração PDF, paginação real em quatro colunas, estabilidade de âncoras com Unicode e zoom, acessibilidade, limites de memória e restauração após falha. O planejamento descreve como verificar; não comprova funcionamento.
''')

def stage1():
 d=STAGES[0]
 write(f'{d}/Ideia_e_Contexto.md','''# IDEA-001 — origem e interpretação

## Solicitação literal

“Execute de forma automática a produção de um planejamento de software (até a etapa 6 da normativa anexada neste projeto) para um aplicativo cujo objetivo é Transformar formatos diversos de texto, como txt, pdf e epub, em jornais estilizados de 4 colunas de texto ( apenas uma formatação de texto adaptada ). A ideia é que a aplicação também tenha diversas funcionalidades de qualidade de vida para leitura, como outros leitores de epub existentes. Itere por conta própria sobre as 6 etapas e só avance para a próxima etapa quando a avaliação de métricas da etapa anterior bater no mínimo 75 pontos de 100. Ao final do processo, gere um arquivo .zip com o planejamento e uma imagem por etapa sumarizando o conteúdo”

## Interpretação separada

Público hipotético: leitores de livros e textos longos em computador. Necessidade: ler conteúdo próprio em apresentação editorial compacta, mantendo continuidade e controle visual. Problema ainda não validado com usuários. Idioma inicial da interface: pt-BR; textos Unicode em escrita horizontal da esquerda para a direita. Não prometer suporte editorial completo a escrita vertical/RTL.

OBJ-001: importar sem adulterar texto; aferir comparação entre blocos extraídos e corpus de referência. OBJ-002: apresentar quatro colunas em ordem contínua sem saltos/duplicações; aferir contagem e percurso dos blocos. OBJ-003: retomar, buscar e anotar com estabilidade; aferir âncora antes/depois de reabrir e alterar fonte. OBJ-004: manter conteúdo local; aferir tráfego zero ao abrir documento e escopo dos arquivos acessados.

Hipóteses H-001: desktop é melhor ponto inicial; validar com cinco leitores antes da etapa 7. H-002: quatro colunas melhoram conforto; comparar tarefa de 15 minutos em uma e quatro colunas, sem afirmar ganho prévio. H-003: corpus predominantemente textual; validar amostra antes de ampliar formatos. Falha das hipóteses reabre G1A/G1B, sem descartar todo o plano.

Não objetivos: editar conteúdo, sumarizar com IA, montar manchetes ou múltiplas matérias, servir notícias, operar loja, remover DRM ou publicar documentos.
''',id='IDEA-001',stage=1)
 models=[('MOD-001','Leitor desktop local','Alta; texto próprio, offline','Leitores de textos longos','Privacidade, continuidade','Distribuição desktop; PDF imperfeito','Média','Extração/paginação','Armazenamento local','Quatro colunas adaptadas','Conforto não demonstrado'),('MOD-002','Conversor web de arquivos','Média; orientado a saída pontual','Usuário ocasional','Acesso simples e exportação','Continuidade fraca; upload se remoto','Média/alta','Privacidade, hospedagem','Servidor se conversão remota','Conversão rápida','Não validado'),('MOD-003','Modelo livre híbrido local web','Alta potencial','Leitor em navegador','Sem instalador','Quotas e persistência a validar','Alta','Compatibilidade e perda de dados','APIs de armazenamento','Interface portátil','Viabilidade offline não demonstrada')]
 write(f'{d}/Modelos_de_Produto.md','# Opções comparadas\n\n'+table(['ID','Modelo','Aderência','Público','Ganhos','Limites','Complexidade','Riscos','Dependências','Diferencial','Lacunas'],models)+'\nRecomendação provisória: MOD-001. Modelo livre disponível como MOD-003; combinação futura exige nova decisão. Comparações são análise desta proposta, não fatos de mercado. MOD-001 não implica copiar código, identidade visual ou todas as funcionalidades dos referenciais.',id='MOD-001',stage=1)
 write(f'{d}/Referencias_de_Mercado.md','''# Referências verificadas em 26/10/2026

| ID | Fonte oficial | Capacidade observada | Limite da analogia | Confiança |
| --- | --- | --- | --- | --- |
| REF-001 | https://manual.calibre-ebook.com/viewer.html | Navegação, busca, destaques e personalização do leitor | Não prova extração PDF nem experiência exata em quatro colunas deste produto | Alta sobre documentação; não testado |
| REF-002 | https://www.edrlab.org/software/thorium-reader/ | EPUB/PDF, ajustes de fonte/colunas, marcadores e posição | Aceitar formatos no leitor não prova conversão fiel para jornal | Alta sobre documentação; não testado |
| REF-003 | https://www.w3.org/TR/epub-33/ | Spine estabelece ordem primária de leitura EPUB | Padrão não garante fidelidade de qualquer parser | Alta sobre especificação |

Acesso externo realizado por pesquisa e leitura de páginas oficiais, sem instalação dos produtos. Datas de consulta não são datas de teste. Sem alegação de preço, fatia de mercado ou validação. Features são requisitos propostos pela IA, derivados da ideia e analogias; não há licença implícita para reutilizar implementação.
''',id='REF-001',stage=1)
 write(f'{d}/Conjuntos_de_Features.md','''# Alternativas de escopo

| Dimensão | SET-001 Essencial | SET-002 Ampliado | SET-003 Equilibrado proposto |
| --- | --- | --- | --- |
| Incluídas | FEAT-001–006,008 | FEAT-001–012,014 | FEAT-001–009 |
| Excluídas agora | 007,009–014 | 013 | 010–014 |
| Jornada | Importar → ler → retomar | Importar/OCR → ouvir/sincronizar/exportar | Importar → prévia → ler/anotar → backup |
| Benefício | Foco no mecanismo editorial | Amplitude de leitor avançado | Leitura sustentável sem infraestrutura remota |
| Custo relativo | Menor | Muito maior | Intermediário |
| Risco | Perda de notas/backup inexistentes | Contas, rede, OCR, voz e qualidade de exportação | Âncoras e recuperação local |
| Dependências | Parser/layout/persistência | OCR, voz, nuvem, autenticação, exportador | Parser/layout/persistência/backup |
| Acessibilidade/segurança | Teclado e modo acessível; isolamento | Também consentimentos e autenticação | Teclado, modo acessível, isolamento e arquivo de backup explícito |
| Comprovação | Corpus e retomada | Corpus + rede + voz + OCR | Corpus + âncoras + restauração |

Custo de não incluir capacidades críticas no SET-001: sem notas, leitura de estudo incompleta; sem backup, trocar computador perde dados. SET-002 é especificável mas excessivo para validar a proposta central. SET-003 combina a contenção do essencial com notas e backup, sem prometer nuvem. Todos os conjuntos têm qualidade documental avaliada separadamente de conveniência.
''',id='SET-003',stage=1)
 rows=[]
 benefits=['Preservar acesso ao conteúdo próprio','Evitar confiar em extração defeituosa','Entregar a aparência pedida','Ajustar conforto e acesso','Encontrar trechos e mover-se','Manter continuidade','Apoiar leitura ativa','Organizar e controlar retenção','Reduzir perda e portabilidade','Leitura auditiva/consulta','Atender material digitalizado','Continuar entre dispositivos','Fora da finalidade de formatação','Levar aparência para impressão']
 for f,b in zip(FEATURES,benefits): rows.append((*f,b,'IDEA-001 / MOD-001'+(' / REF-001, REF-002' if f[0] in ['FEAT-004','FEAT-005','FEAT-006','FEAT-007','FEAT-010'] else '')))
 write(f'{d}/Features_Propostas.md','# Features, valor e prioridade\n\n'+table(['ID','Comportamento','Prioridade','Dono proposto','Benefício','Origem'],rows)+'\nFeatures agora têm critérios demonstráveis em UC/AC na etapa 3. Exclusões são propostas ratificáveis, não rejeições humanas definitivas. SET-003 v1.0 é base provisória das próximas etapas; nada está no estado Aprovado.',id='FEAT-CATALOGO',stage=1)
 write(f'{d}/Decisao_Concepcao.md','''# Escolha provisória de concepção

G1A: MOD-001 v1.0 recomendado e adotado para elaboração automática; ratificação pendente. G1B: SET-003 v1.0; FEAT-001–009 agora, FEAT-010–012 e 014 depois, FEAT-013 fora. G1A não aprova features implicitamente: as escolhas estão registradas em linhas distintas.

Para FEAT-003, “jornal” significa uma única sequência de texto paginada em quatro colunas da esquerda para a direita. Não são quatro matérias independentes. Coluna de altura finita; ordem coluna 1 de cima a baixo, depois 2, 3, 4 e folha seguinte. Títulos e notas de rodapé entram na sequência, sem alteração editorial.

Sucesso inicial: quatro colunas contêm todos os blocos textuais aceitos, na ordem aprovada na prévia; busca alcança o trecho; reabrir retorna à mesma âncora lógica. Metas verificadas com corpus de referência definido no plano da etapa 6. Apenas autorizar leitura após aceitar a prévia quando houver alerta de PDF.
''',id='DEC-001',stage=1)


def stage2():
 d=STAGES[1]
 write(f'{d}/Mapa_de_Dominios.md','# Fronteiras de negócio\n\n'+table(['ID','Domínio','Propósito','Dado sob propriedade lógica','Features'],DOMS)+'''
Alternativa A: três domínios, fundindo composição e leitura. Menor fronteira inicial, mas regras de paginação e notas se misturam. Alternativa B escolhida provisoriamente: quatro domínios; composição calcula layout, leitura decide ação do leitor. Coesão maior, contrato de âncora explícito. Não são microsserviços.

Acervo é autoridade do catálogo e dos bytes persistidos; ingestão é autoridade da estrutura semântica extraída. Localização física não transfere a propriedade lógica. Leitura é dona de notas/posição, composição somente consome âncoras. Sem contas, permissões por equipe ou domínio artificial de autenticação.
''',id='DOM-MAPA',stage=2)
 write(f'{d}/Matriz_Features_Dominios.md','# Cobertura FEAT × DOM\n\n'+table(['Feature','Primário','Consumidores'],[(f[0],f[3],{'DOM-001':'DOM-002, DOM-003, DOM-004','DOM-002':'DOM-003','DOM-003':'DOM-002, DOM-004','DOM-004':'DOM-001, DOM-003'}[f[3]]) for f in FEATURES[:9]]),id='MAP-FEAT-DOM',stage=2)
 deps=[('DOM-004','DOM-001','Importar bytes selecionados','API-001; token de sessão'),('DOM-001','DOM-004','Confirmar documento e diagnóstico','API-008; documento imutável/revisão'),('DOM-002','DOM-001','Consumir blocos prontos','DocumentoNormalizado v1; API-002'),('DOM-003','DOM-002','Solicitar layout e localizar âncora','API-003/004'),('DOM-003','DOM-004','Persistir posição e notas','API-008; namespace de leitura'),('DOM-004','DOM-003','Excluir/restaurar dados vinculados','API-006/007; política de revisão')]
 write(f'{d}/Dependencias.md','# Contratos entre domínios\n\n'+table(['Origem','Destino','Motivo','Contrato'],deps)+'''\nAs relações de solicitação/resposta podem ser bidirecionais; o grafo de execução não admite reentrada síncrona circular. Acervo orquestra importação por transação: não chama ingestão de dentro de callback de confirmação. Composição é pura sobre documento pronto; leitura não escreve documento. Apenas acervo faz I/O físico, a pedido dos donos lógicos. Cada camada expõe portas sem importar a UI.
''',id='DEP-001',stage=2)
 for did,name,purpose,data,feat in DOMS:
  write(f'{d}/{did}/Identidade.md',f'''# {did} — {name}

Objetivo: {purpose}. Dono lógico: módulo {name}, responsável humano ainda a designar. Dados: {data}. Atores: leitor local e eventos internos autorizados da sessão. Features: {feat}.

Vocabulário comum: obra = item catalogado; revisão = extração imutável; bloco = trecho semântico identificado; folha = grupo visual de quatro colunas; âncora = posição lógica independente de folha.

Fronteira: o domínio responde somente por sua capacidade e contratos de Dependencias.md. Não assume propriedade dos dados dos outros domínios; acervo guarda bytes mas não redefine notas, posições ou estrutura semântica. Sem este domínio perde-se a capacidade “{purpose}”. Regras e dados específicos estão nas seis subetapas da etapa 3.
''',id=did,stage=2,dom=did)

# UC contracts: each item has explicit negative and observable result.
UCS=[
('UC-001','DOM-001','FEAT-001','Importar arquivo','Arquivo local selecionado e dentro dos limites','Validar assinatura/tamanho → detectar tipo → extrair blocos → gerar prévia','Documento pronto somente depois de confirmação','Arquivo protegido, vazio ou inválido: recusar sem criar obra pronta','Um TXT UTF-8 conhecido produz os mesmos caracteres e parágrafos lógicos, removendo somente BOM e normalizando finais de linha; tipo não suportado gera erro identificável'),
('UC-002','DOM-001','FEAT-002','Revisar extração','Extração concluída em estado de prévia','Mostrar fonte, blocos, ordem estimada e alertas → aceitar ou cancelar','Aceite grava revisão imutável; cancelar remove temporários','PDF sem texto: informar OCR indisponível; ordem suspeita exige aceite explícito','PDF de duas colunas conhecido mostra alerta e prévia; cancelar não insere obra no catálogo; sem texto impede confirmar'),
('UC-003','DOM-002','FEAT-003','Compor jornal','Documento confirmado, folha virtual definida','Medir blocos/fontes → distribuir sequencialmente em quatro colunas → mostrar folha','Mapa de layout cobre todo o texto e permite folha seguinte','Palavra longa quebra visualmente; repaginação abortada mantém layout anterior','Com corpus de parágrafos numerados, leitura de coluna 1 a 4 e folhas subsequentes recupera cada trecho exatamente uma vez e na ordem'),
('UC-004','DOM-002','FEAT-004','Personalizar apresentação','Documento aberto com âncora atual','Selecionar fonte/tamanho/tema ou modo acessível → recompor → reposicionar','Perfil salvo e âncora preservada','Fonte indisponível: fallback informado; largura pequena mantém folha virtual e oferece modo acessível','Mudar fonte 18→24 e modo 4→1→4 mantém o mesmo bloco/offset visível, sem gravar página física como posição'),
('UC-005','DOM-003','FEAT-005','Buscar e navegar','Documento pronto aberto','Buscar literal → listar resultados → escolher trecho; navegar sumário/folhas','Âncora do trecho torna-se posição atual','Sem ocorrência: estado vazio; arquivo sem sumário: entrada ausente com explicação; índice em carga tem progresso','Busca por frase com acento retorna offset correto; termo ausente mostra zero resultados; navegação integral funciona por teclado'),
('UC-006','DOM-003','FEAT-006','Retomar e marcar','Obra aberta; posição válida','Mover leitura → salvar âncora → fechar/reabrir; adicionar marcador','Posição confirmada e marcador persistem','Falha de disco mostra não salvo; âncora inválida não desloca silenciosamente para outro capítulo','Reabrir após salvamento confirmado retorna ao mesmo bloco/offset; repetir criar marcador com mesmo commandId não duplica'),
('UC-007','DOM-003','FEAT-007','Destacar e anotar','Seleção textual válida em revisão atual','Selecionar → escolher cor e nota → salvar → listar/editar/remover','Nota vinculada a intervalo lógico, não a coordenadas','Seleção entre colunas mantém continuidade; âncora órfã é sinalizada, nunca perdida sem aviso','Após mudar zoom, destaque cobre o mesmo intervalo; falha de gravação mantém rascunho visível e oferece repetir'),
('UC-008','DOM-004','FEAT-008','Gerir biblioteca e excluir','Acervo aberto; obra selecionada para exclusão','Listar/filtrar → abrir; para excluir mostrar impacto → confirmar → apagar vínculos e blobs','Obra removida e sem referências ativas','Cancelar preserva tudo; disco falha causa rollback; exclusão pendente de blobs é exibida e retentável','Confirmar exclusão remove catálogo, texto, índice e notas vinculadas; arquivos originais fora do acervo nunca são apagados'),
('UC-009','DOM-004','FEAT-009','Salvar e restaurar backup','Destino/origem selecionado; espaço estimado suficiente','Exportar manifesto, documentos e leitura → validar hashes; para restaurar validar e preparar → confirmar → trocar atomicamente','Snapshot íntegro exportado ou restaurado','Backup inválido/incompatível não altera acervo; restauração interrompida mantém snapshot anterior','Restaurar backup conhecido em acervo isolado preserva obras/notas/âncoras; hash alterado aborta sem escrever no acervo ativo')]
DATA=[
('DATA-001','DOM-001','DocumentoNormalizado','docId UUID, revision SHA-256, sourceHash SHA-256, format enum, language string?, blocks Block[], toc TocEntry[], warnings string[]','Obra 1:N revisões; revisão 1:N blocos; bloco contém blockId e text string UTF-16, sourceRef string?','Prévia → confirmado ou descartado; revisão confirmada imutável; NFKC não aplicado ao texto canônico','Ingestão cria; composição/leitura leem; acervo persiste e exclui sob comando do dono'),
('DATA-002','DOM-001','Importacao','jobId UUID, commandId UUID, status enum, progress int, warningCodes string[], tempRef string?, accepted bool','Uma importação candidata a uma obra; nenhuma obra pronta antes de aceite','Validando → extraindo → prévia → confirmado; erro/cancelado terminais','Ingestão cria/altera; UI de importação lê; temporários apagados em cancelamento'),
('DATA-003','DOM-002','PerfilVisual','profileId UUID, font enum, fontPx int, lineHeight number, theme enum, accessibleMode bool','Um perfil global com sobreposição opcional por obra','18px padrão; 14–32px; entrelinha 1.3–1.8; mudar perfil incrementa layoutGeneration','Composição cria/altera; leitura consome; acervo persiste'),
('DATA-004','DOM-002','MapaLayout','docId UUID, revision hash, generation int, viewport rect, pages LayoutPage[], anchorMap ranges','Uma revisão/perfil/viewport gera um mapa; referências a DATA-001, sem cópia autoritativa','Efêmero; calculando → pronto ou falhou; geração antiga nunca substitui atual','Composição cria e descarta; leitura lê; não persistido'),
('DATA-005','DOM-003','EstadoLeitura','docId UUID, revision hash, anchor Anchor, updatedAt instant, saveState enum','Obra 1:1 posição atual por instalação','Anchor = revision + blockId + offset UTF-16 no texto canônico; não cortar surrogate/grapheme; página não é identidade','Leitura cria/altera; acervo persiste; exclusão da obra elimina estado'),
('DATA-006','DOM-003','Anotacao','annotationId UUID, commandId UUID, docId UUID, revision hash, start Anchor, end Anchor?, kind enum, color enum?, note string?','Obra 1:N anotações; marcador tem end null; destaque usa intervalo [start,end)','Ativa → editada ou excluída; revisão ausente → órfã com aviso; nota até 10000 caracteres','Leitor cria/lê/altera/exclui via leitura; conteúdo privado local'),
('DATA-007','DOM-004','Obra','docId UUID, title string, format enum, sourceHash hash, blobRef path relativo, currentRevision hash, createdAt instant','Obra 1:N revisões; aponta para uma revisão atual; blob em diretório interno','Pendente → pronta → excluindo → excluída; mesmo hash oferece abrir existente ou importar como cópia explícita','Acervo cria/altera/exclui; outros domínios leem por ID'),
('DATA-008','DOM-004','Snapshot','snapshotId UUID, schemaVersion int, manifest object, entries hash[], createdAt instant','Snapshot inclui N obras e namespaces de leitura; nenhum caminho absoluto','Preparando → validado → finalizado; falha elimina staging; backup externo sob controle do usuário','Acervo cria/lê/restaura; não indexa diretórios externos')]
APIS=[
('API-001','DOM-001','UC-001, UC-002','importar(token,commandId,formatHint?) → jobId','Assinatura, tamanho e token válido da sessão; token resolve somente arquivo escolhido','UNSUPPORTED, PROTECTED, LIMIT, INVALID, NO_TEXT; sem efeito final até aceite; repetir commandId devolve mesmo jobId'),
('API-002','DOM-001','UC-002, UC-003','confirmar(jobId,acceptedWarnings,commandId) → DocumentoNormalizado','Só sessão que iniciou; estado prévia; warnings críticos aceitos','STALE_STATE, CANCELLED, ORDER_WARNING; confirmação idempotente da mesma revisão; commit via API-008'),
('API-003','DOM-002','UC-003, UC-004','compor(docId,revision,profile,viewport,generation) → MapaLayout','Revisão pronta; perfil validado; viewport >0; documento acessível ao processo local','INVALID_PROFILE, LAYOUT_FAILED, STALE_GENERATION; não altera texto; preserva último layout utilizável'),
('API-004','DOM-002','UC-005, UC-006, UC-007','localizar(anchor,generation) → page,column,rangeRect','Âncora na revisão e geração correntes','ORPHAN_ANCHOR, STALE_GENERATION; sem side effect; coordenadas são efêmeras'),
('API-005','DOM-003','UC-005','buscar(docId,query,cursor?) → resultados Anchor[],nextCursor?','Busca literal 1–256 caracteres, sem regex; normalização somente em índice com mapa para texto original','INDEX_PENDING, EMPTY_QUERY; janela de 100 resultados; sem gravar conteúdo em logs'),
('API-006','DOM-003','UC-006, UC-007','salvarLeitura(docId,revision,commandId,position?,annotationDelta?) → confirmedVersion','IDs pertencem à mesma obra; offsets válidos; nota limitada; transação via API-008','INVALID_ANCHOR, STORAGE_FULL, CONFLICT; mesmo commandId não duplica; retorno só depois de commit'),
('API-007','DOM-004','UC-008, UC-009','gerirAcervo(action,docId?,fileToken?,commandId,confirmed?) → resultado','Ações delete/restore exigem confirmação com resumo; caminho sempre resolvido por token','DENIED, CORRUPT_BACKUP, SCHEMA_NEWER, STORAGE_FULL; delete idempotente; restore substitui snapshot inteiro após validação'),
('API-008','DOM-004','UC-001, UC-002, UC-006, UC-007, UC-008, UC-009','persistir(namespace,docId,commandId,expectedVersion,payload) → committedVersion','Canal interno tipado; namespace autoriza ingestão/documento, leitura/notas e composição/perfil; UI sem SQL','VERSION_CONFLICT, IO_ERROR; commit atômico por unidade; consumidores recebem erro verdadeiro, sem sucesso otimista definitivo')]
JOBS=[('JOB-001','DOM-001','UC-001, UC-002','Extrair arquivo','API-001 após seleção','DATA-002; gera DATA-001','Um job pesado por vez; progresso por blocos; sem retry automático de arquivo inválido; falha transitória permite uma tentativa manual com novo attemptId e mesmo commandId lógico; cancelamento a cada bloco; limite 60s sem progresso; nenhum commit parcial'),('JOB-002','DOM-003','UC-005','Indexar texto','Documento confirmado ou índice ausente','Lê DATA-001; índice derivado da revisão','Um índice por docId/revision; staging e troca; descartar geração velha; até uma repetição transitória; índice removível/reconstruível; progresso e erro na busca')]
MSGS=[('MSG-001','DOM-001','UC-001, UC-002','ImportacaoEstado','Ingestão → VIEW-001 / acervo','jobId,status,progress,warningCodes; sem texto','Canal local tipado; no máximo 4Hz; estado final confiável; dedup por jobId/sequence; UI consulta status se perder evento'),('MSG-002','DOM-002','UC-003, UC-004','LayoutEstado','Composição → VIEW-002','generation,status,errorCode?','Canal local; descartar geração antiga; falha mantém layout anterior; nenhuma notificação de sistema'),('MSG-003','DOM-003','UC-005, UC-006, UC-007','LeituraEstado','Leitura → VIEW-002/003','commandId,saveState,indexState,errorCode?','Canal local; confirmado somente após commit; dedup commandId/version; consulta de estado recupera perda'),('MSG-004','DOM-004','UC-008, UC-009','AcervoEstado','Acervo → VIEW-004','commandId,action,status,errorCode?','Canal local; não emitir título/nota em aviso externo; remoção de obra invalida sessão; estado pós-falha consultável')]
VIEWS=[('VIEW-001','DOM-001','UC-001, UC-002','Importação e prévia','Selecionar arquivo; confirmar alertas; cancelar; repetir','Nome/tipo/tamanho, progresso e sequência de blocos; amostra paginada da fonte quando disponível; PDF mostra página de origem','Vazia: convite; carga: progresso e cancelar; erro: motivo e ação; sucesso: abrir; sem acesso: escolher arquivo novamente'),('VIEW-002','DOM-003','UC-003, UC-004, UC-005, UC-006','Leitor e preferências','Anterior/próxima, sumário, busca, tema, fonte, marcador, modo acessível','Folha de quatro colunas; indicador de posição lógica; estado de salvamento; controles sem sobrepor texto','Vazia: escolher obra; carga: preparar; erro: último layout e repetir; sucesso: texto; sem acesso/obra removida: voltar ao acervo'),('VIEW-003','DOM-003','UC-007','Painel de notas','Criar, editar, remover e ir ao trecho','Seleção, cor, nota e âncora; dono da composição do leitor é DOM-003','Vazia: sem notas; carga: obter; erro: rascunho preservado; sucesso: salvo; sem acesso: obra indisponível'),('VIEW-004','DOM-004','UC-008, UC-009','Acervo e backup','Importar, filtrar, abrir, excluir, exportar/restaurar','Título, formato, posição e diálogo com impacto da exclusão/restauração','Vazia: importar; carga: listar/staging; erro: sem espaço/corrupção; sucesso: snapshot confirmado; sem acesso: nova seleção de destino')]

def stage3():
 d=STAGES[2]
 for did,name,_,_,_ in DOMS:
  base=f'{d}/{did}'
  uc=[r for r in UCS if r[1]==did];data=[r for r in DATA if r[1]==did];apis=[r for r in APIS if r[1]==did];jobs=[r for r in JOBS if r[1]==did];msgs=[r for r in MSGS if r[1]==did];views=[r for r in VIEWS if r[1]==did]
  body=f'# Casos de uso — {name}\n\nAtor padrão: leitor local; permissão: somente arquivo escolhido ou obra de seu acervo local. Eventos automáticos herdam o escopo do comando. Sem papéis remotos.\n'
  for uid,_,feat,title,pre,flow,post,err,ac in uc:
   n=uid[-3:]
   body+=f'\n## {uid} — {title}\n\nFeature: {feat}. Gatilho: ação explícita do leitor, exceto autosave de UC-006 após navegação. Pré-condição: {pre}.\n\nFluxo: {flow}. Pós-condição: {post}. Exceções: {err}. Invariantes: texto canônico imutável, propriedade única e nenhuma confirmação falsa de persistência.\n\n**AC-{n}** — Dado o contexto da pré-condição, quando o fluxo for acionado, então: {ac}. Verificação planejada: TEST-{n}. Além disso, negar token de arquivo inválido deve resultar em DENIED sem leitura arbitrária.\n'
  write(f'{base}/01_Casos_de_Uso.md',body,id=f'SPEC-{did}-UC',stage=3,dom=did)
  write(f'{base}/02_Entidades.md','# Entidades e estados\n\n'+table(['ID','DOM','Entidade','Atributos e tipos','Relações','Invariantes/ciclo','Operações'],data)+'''
Classificação: texto, títulos, notas e histórico podem conter conteúdo pessoal/sensível fornecido pelo usuário. Necessidade: leitura local e continuidade. Acesso: somente sessão local, sem telemetria de conteúdo. Retenção: até exclusão explícita da obra; temporários de importação são eliminados ao concluir/cancelar e resíduos no próximo início. Backups externos são responsabilidade de retenção do usuário e contêm conteúdo em claro; informar antes de exportar.

Índices e layouts são derivados reconstruíveis. Excluir obra remove dados ativos e temporários; não prometer apagamento forense de SSD, backups do SO ou cópias externas. Arquivo original selecionado permanece intocado. Nova extração cria outra revisão e não migra notas silenciosamente; âncoras incompatíveis são sinalizadas.
''',id=f'SPEC-{did}-DATA',stage=3,dom=did)
  write(f'{base}/03_Servicos.md','# Contratos locais\n\n'+table(['ID','DOM','Casos','Entrada → saída','Validação/autorização','Erros e efeitos'],apis)+'''
Todas as APIs são interfaces locais, não HTTP. Ações com efeito usam commandId UUID e registro transacional; retenção de deduplicação até exclusão da obra, para restore até substituição do snapshot seguinte. expectedVersion impede sobrescrever atualização concorrente. As entidades lidas/escritas são as do mesmo domínio, mais referências de DATA-001 e DATA-007 pelos contratos da etapa 2. I/O físico delega a API-008. Erros são enums tipados; caminhos e texto não aparecem em logs.
''',id=f'SPEC-{did}-API',stage=3,dom=did)
  write(f'{base}/04_Workers.md','# Workers e rotinas\n\n'+(table(['ID','DOM','UC','Objetivo','Gatilho','Dados/resultado','Concorrência, falha e limites'],jobs) if jobs else 'N/A: nenhum job autônomo neste domínio. Composição é cálculo local assíncrono cancelável por geração, ligado à interação UC-003/004; não exige rotina persistente. Acervo executa backup por comando explícito com progresso, sem scheduler. Consumidores recebem retorno/MSG do comando. Não há processamento periódico oculto.')+'\n\nJobs aplicáveis executam fora da UI, sem permissão de rede. Falha e término são observáveis por MSG-001 ou MSG-003; fechamento encerra o processo, e o próximo início descarta staging não confirmado. Não há alegação de job já implementado.',id=f'SPEC-{did}-JOB',stage=3,dom=did)
  write(f'{base}/05_Mensageria.md','# Eventos e feedback\n\n'+table(['ID','DOM','UC','Evento','Produtor → consumidor','Payload','Entrega e falha'],msgs)+'''
Natureza: eventos internos e feedback na interface; prioridade normal, falhas finais imediatas. Destinatário é somente a janela da sessão da obra/job. Prazo alvo de feedback: 250ms após estado do serviço. Consentimento para push/e-mail: N/A, canais externos inexistentes. Indicadores de erro essencial não podem ser silenciados por preferência. Não há broker, e-mail ou notificação do SO. EventId e sequence permitem deduplicação; estado autoritativo pode ser consultado, portanto perda de evento não perde resultado.
''',id=f'SPEC-{did}-MSG',stage=3,dom=did)
  viewtext=table(['ID','DOM dono da composição','UC','Tela','Ações','Campos','Estados'],views) if views else 'Sem tela canônica própria: DOM-002 é headless; UC-003/004 usam VIEW-002 de DOM-003. Estado visual, controles e permissões estão definidos uma vez no dono de composição. A ausência de tela própria não dispensa os casos interativos.'
  write(f'{base}/06_Telas.md','# Telas e acessibilidade\n\n'+viewtext+'''
Regras transversais: foco visível, ordem de Tab lógica, nomes acessíveis, status assíncronos anunciados sem repetir a cada bloco. Setas/PageUp/PageDown navegam somente fora de campos; Escape fecha painel e devolve foco. Diálogos de exclusão/restauração têm foco contido e confirmação explícita. Não comunicar estado só por cor; contraste alvo 4,5:1 para texto comum.

VIEW-002 é definida apenas em DOM-003; consome composição de DOM-002. Em viewport 1280×800, folha de 1184px com quatro colunas; largura menor não reduz fonte automaticamente: folha virtual horizontal com controle “próxima coluna”, ou escolha de modo acessível de uma coluna. A 200% de zoom, modo acessível oferece reflow sem rolagem horizontal e mesma âncora. Ordem de leitura assistiva usa DOM textual contínuo e não quatro cópias do conteúdo. Sem acesso: arquivo removido/token expirado retorna à seleção ou acervo, com motivo visível.
''',id=f'SPEC-{did}-VIEW',stage=3,dom=did)
  links=[]
  for row in uc:
   uid=row[0];links.append((uid,row[2],','.join(r[0] for r in data),','.join(r[0] for r in apis if uid in r[2]),','.join(r[0] for r in jobs if uid in r[2]) or 'N/A',','.join(r[0] for r in msgs if uid in r[2]),','.join(r[0] for r in VIEWS if uid in r[2]) or ('VIEW-002' if did=='DOM-002' else 'N/A'),f'AC-{uid[-3:]}'))
  write(f'{base}/Mapa_de_Artefatos.md','# Composição rastreável\n\n'+table(['UC','Feature','Dados próprios','Serviços','Workers','Mensagens','Telas próprias/consumidas','Aceite'],links)+'\nConsulte dependências interdomínio em 02_Dominios/Dependencias.md. Os vínculos auxiliares com API-008 e DATA-007 são infraestrutura de persistência compartilhada, sem mudar a propriedade lógica. Cada tipo é avaliado separadamente no painel; não se compensa reprovação por média.',id=f'MAP-{did}',stage=3,dom=did)

if __name__=='__main__':
 n=int(sys.argv[1]);
 if n==0:intro()
 elif n==1:stage1()
 elif n==2:stage2()
 elif n==3:stage3()
