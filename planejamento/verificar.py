from pathlib import Path
import json,re,hashlib
from PIL import Image
root=Path(__file__).resolve().parent
checks=[]
def check(label,value):
 checks.append((label,bool(value)))
 if not value:raise AssertionError(label)
check('Seis imagens PNG',len(list((root/'imagens').glob('etapa_*.png')))==6)
check('Seis fontes SVG',len(list((root/'imagens').glob('etapa_*.svg')))==6)
for p in sorted((root/'imagens').glob('*.png')):
 im=Image.open(p);check(p.name+' 1600x1060',im.size==(1600,1060));im.verify()
rows=[]
for i in range(1,7):
 r=json.loads((root/f'Avaliacoes/E{i}.json').read_text());rows+=r
 check(f'Etapa {i}: mínimo aplicável >=75',min(x['IQE'] for x in r if x['IQE'] is not None)>=75)
 for x in r:
  if x['IQE'] is not None:check(x['id']+' fórmula IQE',x['IQE']==sum(w*x[k]/4 for k,w in [('C',25),('K',25),('R',20),('E',20),('G',10)]))
check('24 tipos por domínio',sum('.DOM-' in x['id'] and x['tipo'] in ['UC','DATA','API','JOB','MSG','VIEW'] for x in rows)==24)
check('N/A sem nota fictícia',sum(x['IQE'] is None for x in rows)==3)
for d in range(1,5):
 p=root/'03_Artefatos'/f'DOM-{d:03}'
 check(f'DOM-{d:03}: seis subetapas + mapa',len(list(p.glob('*.md')))==7)
check('7 fichas FLOW',len(list((root/'05_Fluxos').glob('FLOW-*.md')))==7)
check('9 fichas NUC',len(list((root/'04_Nucleos').rglob('NUC-*.md')))==9)
check('6 fichas ADR',len(list((root/'06_Arquitetura/decisoes').glob('ADR-*.md')))==6)
# Markdown metadata is valid JSON within YAML delimiters; no human approval is invented.
for p in root.rglob('*.md'):
 if p.name=='Normativa_Fonte.md':continue
 s=p.read_text();check(str(p.relative_to(root))+' metadados',s.startswith('---\n'))
 meta=json.loads(s.split('---\n',2)[1]);check(p.name+' Proposta',meta['estado']=='Proposta');check(p.name+' aprovação null',meta['aprovado_por'] is None and meta['aprovado_em'] is None)
canonical='\n'.join(p.read_text() for p in root.rglob('*.md') if p.name!='Normativa_Fonte.md')
for prefix,count in [('FEAT',14),('DOM',4),('UC',9),('AC',9),('DATA',8),('API',8),('JOB',2),('MSG',4),('VIEW',4),('NUC',9),('FLOW',7),('ADR',6),('TEST',15)]:
 for i in range(1,count+1):check(f'{prefix}-{i:03} registrado',f'{prefix}-{i:03}' in canonical)
# Check numeric references of typed artifacts stay inside catalogued universe.
limits={'FEAT':14,'DOM':4,'UC':9,'AC':9,'DATA':8,'API':8,'JOB':2,'MSG':4,'VIEW':4,'NUC':9,'FLOW':7,'ADR':6,'TEST':15}
for prefix,n in re.findall(r'\b(FEAT|DOM|UC|AC|DATA|API|JOB|MSG|VIEW|NUC|FLOW|ADR|TEST)-(\d{3})\b',canonical):check(f'Referência {prefix}-{n} válida',1<=int(n)<=limits[prefix])
print(json.dumps({'resultado':'OK','checks':len(checks),'unidades':len(rows),'menor_IQE':75,'limite':'Verificação documental; sem teste de produto'},ensure_ascii=False))
