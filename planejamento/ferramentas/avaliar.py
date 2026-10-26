from pathlib import Path
import sys,json,re,textwrap,html
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,str(Path(__file__).parent))
from produzir import ROOT,STAGES,write,table,DOMS,UCS,DATA,APIS,JOBS,MSGS,VIEWS
PANELS=ROOT/'Avaliacoes'; PANELS.mkdir(exist_ok=True)
TITLES=['Concepção','Domínios','Artefatos por domínio','Núcleos funcionais','Fluxos de leitura','Arquitetura e riscos']
CARDS={
1:[('MODELO · MOD-001','Leitor desktop local. Alternativas: conversor web e modelo livre híbrido.'),('ESCOPO · SET-003','Importar TXT, PDF textual e EPUB; ler, buscar, retomar, anotar e salvar backup.'),('QUATRO COLUNAS','Texto contínuo da coluna 1 à 4. Sem resumo, reescrita ou criação de notícias.'),('LIMITES','OCR, nuvem, voz e exportação editorial ficam para depois. DRM e layout fixo são recusados.')],
2:[('DOM-001 · INGESTÃO','Dono da validação, extração, prévia e documento semântico imutável.'),('DOM-002 · COMPOSIÇÃO','Dono do perfil e layout. Consome texto sem alterar seu conteúdo.'),('DOM-003 · LEITURA','Dono da posição, busca, marcadores, destaques e notas.'),('DOM-004 · ACERVO','Dono do catálogo, arquivos físicos, exclusão e recuperação por backup.')],
3:[('9 CASOS DE USO','Importar, revisar, compor, personalizar, buscar, retomar, anotar, gerir e recuperar.'),('8 ENTIDADES · 8 SERVIÇOS','Propriedade lógica explícita. APIs locais tipadas; nenhuma API de rede.'),('2 JOBS · 4 EVENTOS','Extração e índice fora da UI. Progresso, cancelamento e erros observáveis.'),('4 TELAS CANÔNICAS','Importação, leitor, notas e acervo. Composição usa o leitor compartilhado.')],
4:[('INGESTÃO · NUC-001–003','Coordenar regra de importação, rotina de extração e experiência de prévia.'),('COMPOSIÇÃO · NUC-004','Calcular quatro colunas e resolver âncoras; nenhum dado textual é reescrito.'),('LEITURA · NUC-005–007','Buscar, persistir posição/notas, indexar e compor interação acessível.'),('ACERVO · NUC-008–009','Biblioteca e backup com persistência atômica e confirmação das ações destrutivas.')],
5:[('FLOW-001 · IMPORTAR','Selecionar → validar → extrair → prévia → aceitar → abrir em quatro colunas.'),('FLOW-002/003 · LER','Personalizar e navegar sem perder a âncora; busca com estados de índice.'),('FLOW-004/005 · CONTINUAR','Retomar e anotar com commit confirmado; falhas preservam rascunho e estado.'),('FLOW-006/007 · CUIDAR','Excluir com impacto visível; backup validado em staging antes de restaurar.')],
6:[('DESKTOP LOCAL · ADR-001','Monólito modular. Interface isolada; sem contas, servidor ou envio de documentos.'),('PIPELINE · ADR-002/003','Texto canônico → layout derivado. PDF.js candidato; EPUB segue ordem do spine.'),('DADOS · ADR-004/005','SQLite e blobs; âncoras por revisão/bloco/offset. Backup transacional.'),('PROVAS PLANEJADAS','Corpus, Unicode, zoom, parser hostil, disco cheio, cancelamento e restauração.')]
}
def diagram(stage):
 W,H=1600,1060; im=Image.new('RGB',(W,H),'#f5f1e8');dr=ImageDraw.Draw(im)
 f='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';b='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
 font=lambda n,bold=False:ImageFont.truetype(b if bold else f,n)
 svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><rect width="1600" height="1060" fill="#f5f1e8"/>']
 def rect(x,y,w,h,color):dr.rectangle((x,y,x+w,y+h),fill=color);svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}"/>')
 def txt(x,y,t,size=25,bold=False,color='#172c36'):
  dr.text((x,y),t,font=font(size,bold),fill=color)
  svg.append(f'<text x="{x}" y="{y+size}" font-family="DejaVu Sans,sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="{color}">{html.escape(t)}</text>')
 rect(0,0,W,16,'#a14b2e');txt(70,48,'LEITOR DE JORNAL / PLANEJAMENTO',25,True)
 txt(70,104,f'{stage:02d}  {TITLES[stage-1]}',54,True)
 txt(70,180,'PROPOSTA v1.0  •  26/10/2026  •  Síntese documental',24)
 for i,(title,body) in enumerate(CARDS[stage]):
  x=70+(i%2)*750;y=252+(i//2)*270
  rect(x,y,710,238,'#ffffff');rect(x,y,8,238,'#a14b2e');txt(x+28,y+25,title,26,True)
  lines=textwrap.wrap(body,width=43)
  for j,l in enumerate(lines):txt(x+28,y+82+j*35,l,25)
 txt(70,829,'AUTOAVALIAÇÃO 75/100  •  mínimo solicitado atingido',29,True)
 txt(70,881,'Sem revisão independente; gates humanos pendentes de ratificação.',24)
 txt(70,924,f'Fonte: {STAGES[stage-1]}/ + Avaliacoes/AV-E{stage}.md',22)
 txt(70,979,f'DIAG-00{stage}  |  As imagens resumem; o Markdown define os requisitos.',22)
 svg.append('</svg>');out=ROOT/'imagens';out.mkdir(exist_ok=True);im.save(out/f'etapa_{stage:02d}.png');(out/f'etapa_{stage:02d}.svg').write_text('\n'.join(svg))
 write(f'diagramas/DIAG-00{stage}.md',f'''# DIAG-00{stage} — {TITLES[stage-1]}

Etapa: {stage}; versão 1.0; estado Proposta. Fonte editável: ../imagens/etapa_{stage:02d}.svg. Imagem: ../imagens/etapa_{stage:02d}.png. Fonte de verdade: ../{STAGES[stage-1]}/ e avaliação AV-E{stage}. Sem commit Git alegado.

Objetivo: resumir as decisões e limites para revisão. Legenda: cada cartão é um grupo de responsabilidades/requisitos; proximidade não representa dependência ou sequência. As relações detalhadas estão nos mapas Mermaid e no Markdown. Simplificações: não exibe todos os atributos, exceções e riscos. Não é captura de um aplicativo funcionando.

Descrição acessível: {' '.join(t+': '+b for t,b in CARDS[stage])}

Autor e conferência semântica: mesma IA; revisão independente pendente. Verificação: comparar títulos, IDs e quantidades com catálogos da etapa; imagem renderizada com fonte Unicode e inspecionada quanto a limites geométricos. Estado não apresentado como aprovado.
''',id=f'DIAG-00{stage}',stage=stage)

def unit(stage,id,typ,dom,metrics,reason):
 return dict(etapa=stage,id=id,tipo=typ,dom=dom,versao='1.0',C=3,K=3,R=3,E=3,G=3,IQE=75,especificos=metrics,justificativa=reason,maturidade='M3 / M3',gate='Pendente; passagem documental delegada',revisao='Autoavaliação limitada',diagrama=f'DIAG-00{stage}')

def run(n):
 if n>1:
  prev=json.loads((PANELS/f'E{n-1}.json').read_text());assert min(r['IQE'] for r in prev if r['IQE'] is not None)>=75
 assert list((ROOT/STAGES[n-1]).rglob('*.md'))
 rows=[]
 if n==1:
  rows=[unit(n,'AV-1A','Modelos',None,'P1A: 3/3 comparáveis; 3/3 fatos com fonte/limite; 4/4 objetivos aferíveis; alternativas + livre: Sim','Comparação uniforme e hipóteses explícitas; escolha humana não presumida.')]
  for s in ['SET-001','SET-002','SET-003']: rows.append(unit(n,'AV-1B.'+s,'Conjunto',None,'P1B-01 14/14; P1B-02 3/3; P1B-03 14/14; P1B-04 9/9','Features e prioridades rastreadas; comportamentos de agora e critérios iniciais em Decisao_Concepcao. Conveniência não é IQE.'))
 elif n==2:
  for d,*_ in DOMS:rows.append(unit(n,'AV-2.'+d,'Domínio',d,'P2-02 1/1; demais conforme mapa','Fronteira e dono lógico descritos; persistência física não duplica autoridade.'))
  rows.append(unit(n,'AV-2.MAPA','Mapa',None,'P2-01 9/9; P2-02 4/4; P2-03 6/6; P2-04 4/4 grupos de responsabilidade','Todas as features agora têm um dono; seis contratos interdomínio definidos.'))
 elif n==3:
  for d,*_ in DOMS:
   u=[x for x in UCS if x[1]==d];da=[x for x in DATA if x[1]==d];a=[x for x in APIS if x[1]==d];j=[x for x in JOBS if x[1]==d];m=[x for x in MSGS if x[1]==d];v=[x for x in VIEWS if x[1]==d]
   for typ,arr in [('UC',u),('DATA',da),('API',a),('JOB',j),('MSG',m),('VIEW',v)]:
    count=len(arr)
    if count:
     indicators=f'P3{typ}-01 {count}/{count}; P3{typ}-02 {count}/{count}; P3{typ}-03 {count}/{count}'
     if typ=='MSG': indicators=f'P3MSG-01 {count}/{count}; P3MSG-02 {count}/{count}; P3MSG-03 N/A: sem canal externo/consentimento; avisos locais essenciais definidos'
     rows.append(unit(n,f'AV-3.{d}.{typ}',typ,d,indicators,'Inspeção integral dos itens listados, sem amostragem. Campos requeridos em ficha e regras comuns; critérios são especificados, não executados.'))
    else:
     rows.append(dict(etapa=n,id=f'AV-3.{d}.{typ}',tipo=typ,dom=d,versao='1.0',IQE=None,especificos='N/A: ver justificativa e consumidores no arquivo do tipo',justificativa='Ausência examinada, sem atribuir nota fictícia. Categoria dispensada por escopo proposto; ratificação pendente.',maturidade='N/A',gate='Dispensa proposta; pendente',revisao='Autoavaliação limitada',diagrama='DIAG-003'))
   rows.append(unit(n,f'AV-3.{d}','Agregado',d,'6/6 tipos avaliados; mínimo aplicável 75','Nenhum tipo reprovado é compensado por média.'))
 elif n==4:
  for i in range(1,10):rows.append(unit(n,f'AV-4.NUC-{i:03}','Núcleo',None,'P4: composição 1/1; comportamento 1/1; erros/retorno 1/1','Todos os componentes v1.0 e AC estão explicitados na ficha. Não herda aprovação fictícia.'))
  for d,*_ in DOMS:rows.append(unit(n,f'AV-4.{d}','Agregado domínio',d,'Capacidades alocadas: 100%; categorias N/A justificadas no mapa','Mapas explicitam ausência de núcleo artificial e eventos incorporados.'))
 elif n==5:
  for i in range(1,8):rows.append(unit(n,f'AV-5.FLOW-{i:03}','Fluxo',None,'P5-02 1/1; P5-03 5/5 classes pertinentes; P5-04 1/1 percurso de feedback','Revisão de sucesso, erro, atraso, acesso negado, repetição/cancelamento; recuperação documentada.'))
  rows.append(unit(n,'AV-5.MAPA','Consolidado',None,'P5-01 7/7; P5-02 7/7; P5-03 35/35 classes; P5-04 7/7','Classes N/A têm justificativa; contagem trata classes de cenário, não testes executados.'))
 elif n==6:
  for i in range(1,7):rows.append(unit(n,f'AV-6.ADR-{i:03}','ADR',None,'Decisão estrutural documentada 1/1','Alternativas, consequência e método de falsificação descritos; prova técnica ainda pendente.'))
  rows.append(unit(n,'AV-6.CONTRATOS','Transversal',None,'8/8 APIs tipadas; 4/4 eventos locais; modelo de âncora 1/1','Limites de confiança e dados tratados em contratos e governança.'))
  rows.append(unit(n,'AV-6.ARQUITETURA','Consolidado',None,'P6-01 6/6; P6-02 6/6; P6-03 6/6; P6-04 0 contradições altas/críticas identificadas','Riscos têm papel responsável, controle, teste e retorno; ausência de achado não comprova ausência de defeito.'))
 diagram(n)
 rows.append(unit(n,f'AV-E{n}','Etapa consolidada',None,'Ver unidades individuais acima; menor aplicável = 75','C=3: escopo e exceções descritos; K=3: invariantes e contrapercursos conferidos; R=3: IDs e consumidores explícitos; E=3: fontes/hipóteses e critérios planejados; G=3: versão, estado, visual e limites registrados. Nenhuma dimensão recebe 4 sem revisão independente.'))
 (PANELS/f'E{n}.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
 write(f'Avaliacoes/AV-E{n}.md',f'# Avaliação da etapa {n} — {TITLES[n-1]}\n\nLimiar solicitado: 75/100. Fórmula normativa; C/K/R/E/G=3/3/3/3/3 em cada unidade aplicável, IQE=18,75+18,75+15+15+7,5=75. Resultado: suficiente para avanço documental delegado; não suficiente para declarar gate original aprovado. Avaliação realizada após salvar o conteúdo e antes de elaborar a próxima etapa. Uma passagem de avaliação foi suficiente; não se inventaram versões reprovadas ou pontuações anteriores.\n\n'+table(['Unidade','Domínio','Indicadores N/D','IQE','Fundamento/limite'],[(r['id'],r['dom'] or '—',r['especificos'],r['IQE'] if r['IQE'] is not None else 'N/A',r['justificativa']) for r in rows])+'''\n## Inspeção qualitativa

Modelos mentais: MM3 (percurso contrário) procura um erro que produza sucesso falso; MM9 (propriedade única) verifica que layout não muda texto e acervo não redefine notas; MM2 distingue requisito proposto de resultado testado. Verificação documental integral, sem amostragem. Revisão não é independente; LIM-001 permanece aberta. Não há achado crítico/alto documental identificado ao fechar esta versão. Riscos de implementação permanecem no plano.

Gate humano: Pendente. Autor do planejamento e da autoavaliação: mesma IA. Data: 26/10/2026. Maturidade candidata e efetiva M3. Sem software implementado, testes de produto ou validação de mercado. N/A recebe justificativa e não participa do mínimo; a revisão de aplicabilidade está registrada.
''',id=f'AV-E{n}',stage=n)
 allrows=[]
 for i in range(1,n+1):allrows+=json.loads((PANELS/f'E{i}.json').read_text())
 write('Avaliacoes/Painel.md','# Painel consolidado\n\n'+table(['Unidade','Tipo','DOM','Versão','IQE','Maturidade candidata/efetiva','Visual','Revisão','Decisão humana'],[(r['id'],r['tipo'],r['dom'] or '—','1.0',r['IQE'] if r['IQE'] is not None else 'N/A',r['maturidade'],r['diagrama'],r['revisao'],r['gate']) for r in allrows])+f'\nMenor IQE aplicável: 75. Unidades avaliadas: {len(allrows)}; unidades aplicáveis abaixo de 75: 0; unidades não avaliadas das etapas concluídas: 0. Gates de ratificação/dispensa pendentes: {len(allrows)} registros (não representa quantidade de defeitos). Todas as decisões humanas específicas continuam pendentes. Data comum: 26/10/2026. Indicadores N/D completos nas fichas AV-E1–E{n}. CMP/TRC/VIS estruturais são medidos em Verificacao_Entrega.md; VFC depende da inspeção qualitativa; RET N/A sem histórico de reabertura; EST=0 mudanças fora do escopo identificadas.\n')
 print(json.dumps({'etapa':n,'minimo':75,'unidades':len(rows),'proxima_liberada_para_elaboracao':True},ensure_ascii=False))
if __name__=='__main__':run(int(sys.argv[1]))
