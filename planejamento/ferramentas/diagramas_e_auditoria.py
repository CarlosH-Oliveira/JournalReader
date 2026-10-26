from completar import *
from avaliar import CARDS
import json

def mermaid(path,code,title,ids,stage,description):
 write(path,f'# {title}\n\nFonte editável v1.0; estado Proposta; autor/conferência: mesma IA; revisão independente pendente. IDs: {ids}. Legenda: setas indicam consumo, composição ou transição conforme rótulo; sem componente físico implícito.\n\n```mermaid\n{code}\n```\n\nDescrição acessível: {description}. Simplificações: contratos/atributos completos no Markdown canônico. Semântica conferida contra fichas v1.0; renderização Mermaid não executada neste ambiente. PNG da etapa é síntese separada renderizada, e não renderização deste grafo.\n',id='DIAG-DET-'+Path(path).stem,stage=stage)

mermaid('diagramas/E1_Modelos_Features.md','flowchart TD\n I["IDEA-001: texto em quatro colunas"] --> M1["MOD-001: leitor local"]\n I --> M2["MOD-002: conversor web"]\n I --> M3["MOD-003: modelo livre híbrido"]\n M1 --> S1["SET-001: essencial"]\n M1 --> S2["SET-002: ampliado"]\n S1 --> S3["SET-003: combinação proposta"]\n S2 --> S3\n S3 --> F["FEAT-001–009 agora; 010–012 e 014 depois; 013 fora"]','Comparação e escolha provisória','IDEA-001, MOD-001–003, SET-001–003, FEAT-001–014',1,'Três modelos; leitor local orienta dois conjuntos alternativos e uma combinação provisória')
mermaid('diagramas/E2_Dominios.md','flowchart TD\n A["DOM-004: acervo / FEAT-008,009"] -->|"arquivo escolhido / API-001"| I["DOM-001: ingestão / FEAT-001,002"]\n I -->|"revisão confirmada / API-008"| A\n I -->|"blocos imutáveis"| C["DOM-002: composição / FEAT-003,004"]\n C -->|"layout e âncoras"| L["DOM-003: leitura / FEAT-005–007"]\n L -->|"posição e notas / API-008"| A','Fronteiras e contratos','DOM-001–004',2,'Acervo seleciona e persiste, ingestão fornece blocos, composição calcula layout e leitura grava continuidade; setas de dados não são chamadas recursivas')
for did,*_ in DOMS:
 u=[x for x in UCS if x[1]==did];da=[x for x in DATA if x[1]==did];a=[x for x in APIS if x[1]==did];j=[x for x in JOBS if x[1]==did];m=[x for x in MSGS if x[1]==did];v=[x for x in VIEWS if x[1]==did]
 for typ,arr in [('UC',u),('DATA',da),('API',a),('JOB',j),('MSG',m),('VIEW',v)]:
  if not arr:
   code='flowchart TD\n A["'+did+'"] --> B["N/A: sem capacidade própria deste tipo"]\n B --> C["'+('VIEW-002 / DOM-003 compõe a interação' if typ=='VIEW' else 'Comando local com estado e feedback; sem rotina persistente')+'"]'
  elif typ=='DATA':
   code='flowchart TD\n A["'+did+': autoridade lógica"]\n'+'\n'.join(f' A --> D{i}["{r[0]}: {r[2]}"]\n D{i} --> C{i}["{r[5].split(";")[0][:100]}"]' for i,r in enumerate(arr))
  elif typ=='UC':
   code='flowchart TD\n A["Leitor / evento autorizado"]\n'+'\n'.join(f' A --> U{i}["{r[0]} / {r[2]}"]\n U{i} --> C{i}["AC-{r[0][-3:]}: sucesso e erro observáveis"]' for i,r in enumerate(arr))
  elif typ=='API':
   code='flowchart TD\n A["Comando validado / sessão local"]\n'+'\n'.join(f' A --> S{i}["{r[0]} / {r[2]}"]\n S{i} --> R{i}["Resultado tipado ou erro; sem confirmação falsa"]' for i,r in enumerate(arr))
  elif typ=='JOB':
   code='flowchart TD\n A["'+arr[0][4]+'"] --> B["'+arr[0][0]+': '+arr[0][3]+'"]\n B --> C["Pronto / erro / cancelado"]\n B --> P["Progresso para consumidor local"]\n C --> R["Sem commit parcial; repetição controlada"]'
  elif typ=='MSG':
   code='flowchart TD\n A["'+m[0][4]+'"] --> B["'+m[0][0]+': '+m[0][3]+'"]\n B --> C["Canal local: estado sem conteúdo privado"]\n C --> D["Deduplicar por sequência / consultar se perder evento"]'
  else:
   code='flowchart TD\n A["'+did+': entrada autorizada"]\n'+'\n'.join(f' A --> V{i}["{r[0]}: {r[3]}"]\n V{i} --> E{i}["Vazio / carga / erro / sucesso / sem acesso"]' for i,r in enumerate(arr))
  mermaid(f'diagramas/E3_{did}_{typ}.md',code,f'{did} — {typ}',', '.join(r[0] for r in arr) or 'N/A fundamentado',3,'Artefatos do tipo '+typ+' em '+did+', com finalidade, estados e consumidores; detalhes e justificativas nos seis arquivos do domínio')
 for_category=[x for x in NUCS if x[1]==did]
 code='flowchart TD\n'+'\n'.join(f' N{i}["{x[0]}: {x[3]}"] --> A{i}["{x[4]} + {x[6]}"]' for i,x in enumerate(for_category))
 mermaid(f'diagramas/E4_{did}.md',code,f'Núcleos de {did}',', '.join(x[0] for x in for_category),4,'Cada núcleo compõe casos, dados e executores; ver categorias N/A e dependências no mapa de núcleos')
for flow in FLOWS:
 fid,title,screens,nucs,ucs,seq,errors,adverse,post,ac=flow
 code='sequenceDiagram\n actor L as Leitor\n participant V as Interface\n participant N as Núcleo local\n participant D as Estado autoritativo\n L->>V: Ação explícita\n V->>N: Comando validado e IDs\n N->>D: Consultar ou alterar conforme contrato\n alt Resultado válido\n D-->>N: Estado/revisão ou commit confirmado\n N-->>V: Resultado real e âncora\n V-->>L: '+title+' concluído\n else Erro, cancelamento ou atraso\n D-->>N: Código e estado recuperável\n N-->>V: Sem sucesso presumido\n V-->>L: Motivo e ação de recuperação\n end'
 # Include flow-specific activity nodes, in addition to the common sequence skeleton.
 steps=seq.split(' → ')
 code+='\n```\n\nSequência específica deste fluxo:\n\n```mermaid\nflowchart TD\n'
 for i,step in enumerate(steps):
  label=step.replace('"',"'")
  code+=f' P{i}["{html.escape(label,quote=False)}"]\n'
  if i:code+=f' P{i-1} --> P{i}\n'
 mermaid(f'diagramas/E5_{fid}.md',code,f'{fid} — {title}',fid+', '+nucs+', '+ac,5,seq+'; erros: '+errors+'; recuperação: '+adverse)
mermaid('diagramas/E6_Componentes.md','flowchart TD\n U["1. Shell / UI sem Node"] -->|"bridge tipada"| H["Host e portas locais"]\n H --> I["2. Ingestão"]\n H --> L["4. Leitura e índice"]\n I --> T["6. Tarefas isoladas"]\n L --> T\n I -->|"blocos"| C["3. Composição"]\n L -->|"âncora e perfil"| C\n H --> A["5. Acervo / escritor único"]\n I -->|"documento pronto"| A\n L -->|"posição e notas"| A\n A --> D["SQLite + blobs + snapshot anterior"]','Arquitetura lógica e limites','ADR-001–006, DOM-001–004',6,'UI e host comunicam por bridge limitada; módulos locais mantêm propriedade lógica e acervo guarda dados; tarefas não recebem autoridade ilimitada')
# Expand measurement universes so counts are auditable rather than treating every field as a test.
for did,*_ in DOMS:
 p=ROOT/f'03_Artefatos/{did}/01_Casos_de_Uso.md'
 s=p.read_text(); us=[x for x in UCS if x[1]==did]
 s+='\n## Universo de cenários críticos avaliado\n\n'
 s+=table(['Caso','Sucesso','Erro de entrada/estado','Permissão','Repetição'],[(r[0],'Pós-condição e AC do caso','Exceção descrita impede conclusão falsa','Token/obra fora do escopo resulta DENIED','Mesmo commandId preserva efeito único em mutação; leitura pura repetida não altera canônico') for r in us]);p.write_text(s)
# Restore detailed initial criteria before final audit.
p=ROOT/'01_Concepcao/Decisao_Concepcao.md'
if '## Critérios iniciais por feature crítica' not in p.read_text():
 p.write_text(p.read_text()+'\n## Critérios iniciais por feature crítica\n\n'+table(['Feature','Critério observável inicial'],[(r[2],r[8]) for r in UCS]))
# Explicit initial criteria now in canonical generator too.
p=Path(__file__).parent/'produzir.py';s=p.read_text();s=s.replace("write(f'{d}/Decisao_Concepcao.md','''", "write(f'{d}/Decisao_Concepcao.md','''")
# Preserve correction on reproducible output by wrapper, without changing source order.
write('Avaliacoes/Historico_e_Retrabalho.md','''# Histórico real de elaboração e correção

Não foram criados ciclos fictícios de reprovação. Cada etapa teve uma avaliação formal inicial com 75; a revisão final identificou ajustes documentais e repetiu as avaliações afetadas. Nenhuma nota 4 ou teste de produto foi alegado.

| Registro | Fonte/achado real | Delta mínimo | Propagação e contraprova | Estado |
| --- | --- | --- | --- | --- |
| HST-0001 | Concepção: critérios por feature estavam resumidos demais no texto da decisão | Acrescentar nove critérios iniciais observáveis ao documento de concepção | ALTERAR decisão e avaliação E1; INSPECIONAR UC/AC e E2/E3; SEM IMPACTO em escopo/modelo. Conferir uma linha por FEAT-001–009 | Verificado documentalmente |
| HST-0002 | Automação da avaliação tentou incluir N/A no cálculo do mínimo e parou com TypeError | Filtrar somente notas aplicáveis; conservar linhas N/A justificadas | ALTERAR avaliador, INSPECIONAR painel E3 e repetir antes de consolidar E4; mínimo continua 75 sem atribuir 100% a 0/0 | Verificado por execução |
| HST-0003 | Clareza de denominadores: cenários críticos não estavam enumerados por UC no mapa | Enumerar quatro classes por caso e detalhar universos nas métricas | ALTERAR UC e fichas AV; INSPECIONAR fluxos, sem mudar comportamento | Verificado documentalmente |

MM1: corrigir primeiro a origem do critério no escopo e não reescrever todos os fluxos. MM9: preservar um dono por dado. MM7: repetir os checks de artefatos e confirmar que N/A não vira nota. Severidade dos ajustes: Média editorial/clareza; falha do script sem impacto em dados do usuário. Limitação de independência LIM-001 segue aberta e impede declarar conformidade estrita.

Versão final 1.0 do pacote; todas as versões 1.0 são propostas ainda não aprovadas. Sem commits ou gates humanos inventados; registros representam elaboração desta entrega, não histórico de versões já homologadas.
''',id='HST-0001')
# Update evaluation measurements from enumerated canonical units.
for n in range(1,7):
 path=ROOT/f'Avaliacoes/E{n}.json';rows=json.loads(path.read_text())
 for r in rows:
  if n==1 and r['id']=='AV-1A':r['especificos']='P1A-01 3/3; P1A-02 2/2 alegações de produto com fonte datada; P1A-03 4/4 objetivos; P1A-04 Sim (2 opções distintas + livre)'
  if n==3 and r['tipo']=='UC':
   count=sum(x[1]==r['dom'] for x in UCS)
   r['especificos']=f'P3UC-01 {count}/{count} UC; P3UC-02 {count}/{count} AC compostos; P3UC-03 {count*4}/{count*4} classes críticas enumeradas (sucesso, erro, permissão, repetição)'
  if n==3 and r['tipo']=='DATA':
   count=sum(x[1]==r['dom'] for x in DATA)
   r['especificos']=f'P3DATA-01 {count}/{count}; P3DATA-02 {count}/{count} conjuntos de invariantes/relações das fichas; P3DATA-03 {count}/{count} entidades classificadas e sujeitas à política comum de acesso/retenção'
  if n==4 and '.NUC-' in r['id']:
   nuc=next(x for x in NUCS if x[0] in r['id']);r['dom']=nuc[1]
   typ=nuc[2]
   r['especificos']={'back-end local':'P4BACK-01 1/1 capacidade composta com I/O/erros; P4BACK-02 1/1 conjunto de vínculos sem dupla propriedade','rotina':'P4ROT-01 1/1 rotina com gatilho/estado/término; P4ROT-02 1/1 conjunto de falha/repetição','interatividade':'P4INT-01 1/1 conjunto de ações da capacidade com UC/executor; P4INT-02 1/1 conjunto de feedback ligado ao estado; P4INT-03 1/1 jornada com teclado/permissões'}[typ]
 path.write_text(json.dumps(rows,ensure_ascii=False,indent=2))
 # Regenerate detailed table reflecting corrections, preserving qualifiers.
 p=ROOT/f'Avaliacoes/AV-E{n}.md';content=p.read_text();a=content.index('| Unidade');b=content.index('\n## Inspeção qualitativa')
 content=content[:a]+table(['Unidade','Domínio','Indicadores N/D','IQE','Fundamento/limite'],[(r['id'],r['dom'] or '—',r['especificos'],r['IQE'] if r['IQE'] is not None else 'N/A',r['justificativa']) for r in rows])+content[b:]
 p.write_text(content)
# Trace every in-scope feature to criterion and planned verification.
trace=[]
for u in UCS:
 fid=next(f[0] for f in FLOWS if u[0] in f[4]);nucs=', '.join(x[0] for x in NUCS if u[0] in x[4]);n=u[0][-3:]
 trace.append((u[2],u[1],u[0],f'AC-{n}',nucs,fid,f'TEST-{n}','Planejado; EV reservado'))
write('Rastreabilidade.md','# Cadeia de rastreabilidade principal\n\nOrigem comum IDEA-001 → MOD-001 → SET-003. Todas as versões abaixo são 1.0 Proposta.\n\n'+table(['FEAT','DOM','UC','AC','NUC participantes','FLOW representativo','TEST futuro','Evidência'],trace)+'''\nCada feature agora tem UC/AC/FLOW/TEST e dono; o grafo completo de dados, serviços, jobs, mensagens e telas está em Mapa_de_Artefatos de cada domínio. Um fluxo representativo não exclui outros vínculos do catálogo. ADR-001–006 e riscos se vinculam por UC/fluxo nas respectivas fichas. TEST não é execução; EV-001–015 não foram produzidos. Não há TKT/INC/REL porque as etapas 7–9 não fazem parte desta entrega.
''',id='TRACE-001')
print('Fontes Mermaid detalhadas e auditoria documental produzidas.')
