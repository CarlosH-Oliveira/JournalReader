from produzir import *
from avaliar import run
NUCS=[
('NUC-001','DOM-001','back-end local','Aceitar importação','UC-001, UC-002','DATA-001, DATA-002','API-001, API-002','NUC-008','Aceite entrega revisão persistida ou erro explícito','AC-001, AC-002'),
('NUC-002','DOM-001','rotina','Extrair em segundo plano','UC-001, UC-002','DATA-001, DATA-002','JOB-001, MSG-001','NUC-001','jobId progride até prévia/erro/cancelado; nunca confirma sozinho','AC-001, AC-002'),
('NUC-003','DOM-001','interatividade','Importar com prévia','UC-001, UC-002','DATA-002','VIEW-001, API-001, API-002, MSG-001','NUC-001, NUC-002','Ações de seleção, aceite e cancelamento recebem feedback do estado real','AC-001, AC-002'),
('NUC-004','DOM-002','back-end local','Compor e localizar','UC-003, UC-004','DATA-003, DATA-004; lê DATA-001','API-003, API-004, MSG-002','NUC-001 (documento pronto)','Perfil + revisão + viewport geram mapa; versão velha descartada','AC-003, AC-004'),
('NUC-005','DOM-003','back-end local','Navegar e persistir leitura','UC-005, UC-006, UC-007','DATA-005, DATA-006; lê DATA-001','API-005, API-006, MSG-003','NUC-004, NUC-008','Resolve âncora e confirma gravação por commandId ou relata falha','AC-005, AC-006, AC-007'),
('NUC-006','DOM-003','rotina','Construir índice','UC-005','DATA-001 (leitura), índice derivado','JOB-002, MSG-003','NUC-001 (documento pronto)','Índice compatível com revisão torna busca disponível; falha permite reconstruir','AC-005'),
('NUC-007','DOM-003','interatividade','Ler e anotar','UC-003, UC-004, UC-005, UC-006, UC-007','DATA-003–006','VIEW-002, VIEW-003, MSG-002, MSG-003','NUC-004, NUC-005, NUC-006','Leitor enxerga layout e confirmação de estado; mantém foco/âncora em alterações','AC-003, AC-004, AC-005, AC-006, AC-007'),
('NUC-008','DOM-004','back-end local','Persistir e recuperar acervo','UC-008, UC-009; suporte UC-001/002/006/007','DATA-007, DATA-008; repositórios dos demais donos','API-007, API-008, MSG-004','Nenhum núcleo síncrono; portas de dados dos domínios','Transação confirma mudanças; restore troca snapshot validado e preserva anterior até sucesso','AC-008, AC-009'),
('NUC-009','DOM-004','interatividade','Gerir biblioteca e backup','UC-008, UC-009','DATA-007, DATA-008','VIEW-004, MSG-004','NUC-008, NUC-003 (navegação para importar)','Excluir/restaurar exige confirmação do impacto; cancelamento não altera dados ativos','AC-008, AC-009')]
FLOWS=[
('FLOW-001','Importar e abrir','VIEW-004 → VIEW-001 → VIEW-002','NUC-009, NUC-003, NUC-001, NUC-002, NUC-008, NUC-004, NUC-007','UC-001, UC-002, UC-003','Selecionar arquivo → API-001 gera jobId → JOB-001 valida/extrai → MSG-001 atualiza prévia → confirmar API-002 → API-008 grava revisão/obra → API-003 gera layout → leitor exibe quatro colunas','Formato inválido/protegido ou sem texto impede pronto; PDF suspeito exige aceite da ordem; sem espaço não abre obra incompleta','Atraso mostra progresso e botão cancelar; token negado retorna à seleção; repetir commandId recupera job existente; cancelar limpa temporários','Obra pronta só depois de commit e layout; importação recusada permanece legível no erro','AC-001, AC-002, AC-003'),
('FLOW-002','Personalizar e reorganizar','VIEW-002 → VIEW-002','NUC-007, NUC-004, NUC-005, NUC-008','UC-003, UC-004, UC-006','Capturar âncora → validar perfil → incrementar generation → API-003 recompõe → API-004 localiza → MSG-002 pronto → salvar perfil/posição e renderizar','Fonte ausente usa fallback informado; generation obsoleta não substitui atual; falha mantém layout anterior','Recomposição mostra ocupado; obra removida cancela e volta ao acervo; mudança rápida só aplica última geração; desfazer perfil é recuperação','Mesma âncora visível com novo perfil, sem duplicar texto','AC-003, AC-004, AC-006'),
('FLOW-003','Buscar e usar sumário','VIEW-002 → VIEW-002','NUC-007, NUC-006, NUC-005, NUC-004','UC-005','Abrir busca → se necessário JOB-002 indexa revisão → API-005 retorna âncoras → selecionar resultado → API-004 resolve folha → foco volta ao trecho; sumário usa o mesmo resolver','Sem resultados mostra zero; índice falhou oferece reconstruir; sumário ausente não é erro de importação','Carga tem status; revisão indisponível invalida resultados; cancelar consulta descarta resultados; repetição não grava duplicatas','Resultado selecionado corresponde ao texto original, acento e Unicode preservados','AC-005'),
('FLOW-004','Retomar e marcar posição','VIEW-004 → VIEW-002','NUC-009, NUC-007, NUC-005, NUC-004, NUC-008','UC-006','Abrir obra → ler EstadoLeitura → validar revisão/âncora → API-004 resolve → exibir; ao navegar API-006 salva com debounce → API-008 commit → MSG-003 confirma; marcador por comando explícito','Âncora incompatível mostra órfã e oferece início sem apagar referência; disco cheio exibe não salvo','Escrita lenta mantém indicador pendente; obra removida encerra sessão; repetir commandId não duplica; ao fechar com pendência perguntar tentar/fechar sem salvar/cancelar','Reabertura após confirmação retorna à mesma localização; perda antes de commit é explicitada','AC-006'),
('FLOW-005','Destacar e escrever nota','VIEW-002 → VIEW-003 → VIEW-002','NUC-007, NUC-005, NUC-008, NUC-004','UC-007','Selecionar intervalo DOM → converter em âncoras canônicas → editar nota → API-006 valida e grava via API-008 → MSG-003 confirma → painel lista → ir ao trecho por API-004','Seleção inválida não grava; nota acima do limite pede reduzir; erro de disco preserva rascunho; revisão antiga mostra nota órfã','Escrita em atraso mostra pendente; obra excluída impede salvar; repetir commandId devolve mesma nota; cancelar antes de salvar descarta somente com aviso se rascunho','Destaque acompanha mesmo intervalo após repaginar; nota salva somente com confirmação','AC-007'),
('FLOW-006','Excluir obra do acervo','VIEW-004 → VIEW-004','NUC-009, NUC-008, NUC-007','UC-008','Selecionar obra → mostrar notas e arquivos internos afetados → confirmar → API-007 marca excluindo, bloqueia novas escritas → API-008 transaciona remoção dos vínculos → apagar blobs sem referências → MSG-004 informa conclusão','Falha antes de commit faz rollback; depois de commit mantém exclusão lógica e pendência visível de limpeza de blobs; original externo nunca tocado','Operação lenta mostra andamento; ID fora do acervo é negado; repetir exclusão já finalizada retorna concluído; cancelar antes do commit preserva obra','Obra desaparece após exclusão lógica; resíduos pendentes têm estado e nova tentativa de limpeza','AC-008'),
('FLOW-007','Exportar e restaurar backup','VIEW-004 → VIEW-004','NUC-009, NUC-008','UC-009','Escolher exportar → snapshot consistente → manifesto/hashes → gravar destino temporário → finalizar; restaurar → validar esquema/hashes/limites em staging → mostrar impacto de substituir acervo → confirmar → bloquear escritas → trocar ponteiro de geração → reabrir acervo → MSG-004 conclui','Corrupção ou schema futuro aborta; backup não confiável passa pelas mesmas validações de caminho/zip; falha preserva geração anterior; exclusão de cópias externas é manual','Sem acesso ao destino pede nova seleção; progresso e cancelamento antes da troca; após commit cancelar é N/A, oferecer restaurar snapshot anterior; repetir commandId consulta resultado','Obras/notas/âncoras equivalentes após restauração; sucesso apenas com geração íntegra ativa','AC-009')]

def stage4():
 d=STAGES[3]
 write(f'{d}/Mapa_de_Nucleos.md','# Capacidades compostas\n\n'+table(['ID','DOM','Tipo','Capacidade','UC','DATA','Artefatos','Dependências','Contrato','AC'],NUCS)+'''
Componentes referenciam exclusivamente versão 1.0, em estado Proposta. “back-end” significa regra local, sem serviço remoto. Dependências de documento pronto são dados de entrada e não chamada recursiva. NUC-008 não chama NUC-001 nem NUC-005 durante commit; recebe payload tipado e valida namespace.

## Categorias não aplicáveis por domínio

DOM-001: back-end, rotina e interatividade aplicáveis; notificação independente N/A porque MSG-001 integra a mesma operação e VIEW-001, sem capacidade autônoma. DOM-002: só back-end local aplicável; rotina N/A (recomposição vinculada à interação), notificação N/A (status incorporado), interatividade própria N/A (NUC-007 compõe VIEW-002). DOM-003: back-end, rotina e interatividade aplicáveis; notificação independente N/A (MSG-003 é feedback da ação). DOM-004: back-end e interatividade aplicáveis; rotina persistente N/A (backup por comando), notificação independente N/A (MSG-004 incorporado). Não existem e-mails, push ou scheduler.

G4.NUC e G4.DOM permanecem pendentes de ratificação; autoavaliação permite continuidade documental. Nenhuma capacidade essencial está sem executor; eventos não exigem núcleo artificial de notificação.
''',id='MAP-NUC',stage=4)
 for row in NUCS:
  nid,did,typ,title,uc,data,arts,deps,result,ac=row
  write(f'{d}/{did}/{nid}.md',f'''# {nid} — {title}

Tipo: {typ}. Componentes v1.0: {uc}; {data}; {arts}. Dependências: {deps}. Critérios herdados sem redefinição: {ac}. Documentos canônicos em 03_Artefatos; nenhum componente aprovado pelo humano é alegado.

Contrato observável: {result}. Ator: leitor local/evento do comando; permissões herdadas dos serviços. Entrada sempre inclui obra/revisão ou jobId e, nas mutações, commandId. Saída é resultado tipado/estado real; erro nunca vira confirmação visual de sucesso.

Cenário adverso: negar token/obra removida → erro e retorno à seleção/acervo; injetar repetição → mesmo efeito lógico; falha de cálculo → manter último layout; falha de escrita → preservar rascunho e estado não salvo; cancelamento → nenhuma troca de geração não confirmada. São inspeções de especificação, não testes executados.

Riscos: perda de continuidade e feedback antecipado. Controles: revisão imutável, âncora lógica, confirmação após commit, consulta autoritativa caso evento se perca. Acessibilidade dos núcleos interativos: foco/teclado/estado anunciado nos contratos VIEW. Dispensável nas rotinas headless como UI própria, mas não no consumidor do resultado.

Métricas P4 do tipo: cada ação tem entrada/executor/saída e erro; cada vínculo possui dono; repetição e falha são tratadas; ações de tela têm UC e feedback. Avaliação individual AV-4.{nid}; G4.{nid} pendente. Visual: mapa detalhado Mermaid e DIAG-004.
''',id=nid,stage=4,dom=did)

def stage5():
 d=STAGES[4]
 write(f'{d}/Mapa_de_Fluxos.md','# Jornadas ponta a ponta\n\n'+table(['ID','Objetivo','Telas','Núcleos','UC','Aceites'],[(r[0],r[1],r[2],r[3],r[4],r[9]) for r in FLOWS])+'''\nCobertura: FLOW-001 cobre FEAT-001–003; FLOW-002 FEAT-003/004; FLOW-003 FEAT-005; FLOW-004 FEAT-006; FLOW-005 FEAT-007; FLOW-006 FEAT-008; FLOW-007 FEAT-009. A sessão começa na biblioteca e alcança resultado persistido ou erro recuperável. Todas as ações de abrir/retomar e backup são locais; conectividade externa não participa.
''',id='MAP-FLOW',stage=5)
 for fid,title,screens,nucs,ucs,seq,errors,adverse,post,ac in FLOWS:
  write(f'{d}/{fid}.md',f'''# {fid} — {title}

Ator: leitor local. Objetivo: {title.lower()}. Domínios: donos dos núcleos {nucs}, conforme etapa 4. Tela inicial/final: {screens}. Núcleos: {nucs} v1.0. Casos: {ucs}. Aceites: {ac}.

Pré-condição: sessão local aberta, parâmetros/tokens válidos, revisão existente quando a ação pede uma obra. Entrada: seleção explícita, documento/âncora ou snapshot, conforme UC. Sequência com saídas e contratos: {seq}.

Estado inicial → em andamento → sucesso ou erro/cancelado. Estado de sucesso: {post}. Regras: texto imutável, um dono lógico por dado, geração atual prevalece, confirmação após persistência e acesso só aos arquivos selecionados/acervo.

Exceções e recuperação: {errors}. Cenários de atraso/acesso negado/repetição/cancelamento: {adverse}. Não há timeout que conclua sucesso por inferência. Requisição/cálculo obsoleto pode ser descartado sem alterar estado autoritativo.

Observabilidade planejada: commandId/jobId, duração, tamanho em faixas, estado e errorCode local; sem texto, notas, caminho absoluto ou consulta de busca. Feedback exibe apenas o conteúdo necessário dentro da janela do leitor. Erro pode ser copiado como diagnóstico redigido pelo próprio usuário; sem envio automático.

Contratos nas fronteiras: serviço de origem valida entrada; destino valida revisão/expectedVersion, erro retorna tipado; UI consulta o estado se perder MSG. Dependências são portas locais da etapa 3, não integrações remotas. Critérios de conclusão acima são verificados por TEST correspondente e contraprovas de falha da etapa 6. O fluxo é proposto, não demonstrado em aplicativo.

AV-5.{fid}: inspeção de cinco classes (sucesso/erro, atraso, acesso negado, cancelamento, repetição), com N/A localizado quando cancelamento pós-commit não é reversível; em tal caso há operação de recuperação explícita. Gate humano pendente; limiar automático documental ≥75.
''',id=fid,stage=5)

ADRS=[
('ADR-001','Desktop local e monólito modular','MOD-001, FLOW-001–007','Electron + TypeScript, UI em HTML/CSS, domínios em módulos locais; runtime e dependências fixados após prova','Web/PWA: menor distribuição, maior incerteza de armazenamento e files; Tauri: menor runtime, exige avaliar plugins Rust/parsers','Tamanho do runtime e atualização de segurança ficam sob responsabilidade técnica. Sem rede para abrir documentos; instaladores/assinatura futuramente por plataforma','Provar IPC mínimo, renderizador sem Node e leitura sem rede. Se memória/segurança forem inviáveis, reabrir escolha de runtime sem mudar contratos'),
('ADR-002','Normalização e parsers','UC-001/002, DATA-001/002','TXT com UTF-8/BOM e escolha explícita de codificação legada; PDF.js candidato para camada textual; EPUB como ZIP/XML/XHTML sanitizado em ordem do spine','Conversor remoto: expõe conteúdo e cria infraestrutura; OCR local: amplia custo e escopo; renderizar apenas imagem: não permite quatro colunas textuais','Aceitar somente EPUB refluível e PDF textual sem proteção. PDF usa agrupamento por coordenadas como heurística, nunca garantia de semântica. Sem remoção automática de palavras, cabeçalhos ou hifens sem regra conservadora e aviso','Corpus com textos de referência e PDF multicoluna, ligaduras e notas. Se não houver ordem aceitável, recusar aquela entrada; preservar original e diagnóstico'),
('ADR-003','Paginação de quatro colunas','UC-003/004, DATA-004, FLOW-002','Protótipo de CSS Multi-column com altura finita, column-count:4, column-fill:auto e column-gap:24px; mapa de intervalos por coluna e agrupamento a cada quatro','Grid com texto duplicado: quebra seleção e acessibilidade; Canvas: exige reconstruir texto acessível; copiar número de página: âncora instável','column-count sozinho não é um paginador completo. Overflow e corte de folha precisam controle e testes; conteúdo textual fica em fluxo único. Títulos não atravessam colunas no escopo inicial','Corpus numerado, seleção entre colunas e 200% zoom. Se CSS não fornecer mapeamento robusto, reabrir ADR e adotar fragmentador DOM por medição; sem prometer solução não testada'),
('ADR-004','Persistência e snapshots','UC-006–009, API-008','SQLite para metadados/leitura; blobs imutáveis por hash em diretório de gerações; um escritor serializado; manifestos e ponteiro de geração para troca de acervo','JSON solto: transações e concorrência frágeis; banco remoto: contraria preferência local; copiar DB aberto para backup: snapshot pode ser inconsistente','Atomicidade SQLite não torna banco e filesystem uma transação única. Usar staging, diário de intenção e reconciliação no início; blob finalizado antes de referenciá-lo, resíduo sem referência pode ser limpo','Injetar falha após cada ponto de commit/troca e restaurar anterior. Backup usa exportação lógica consistente ou API de backup, nunca cópia ingênua de arquivo aberto'),
('ADR-005','Âncoras estáveis e Unicode','UC-004–007, DATA-005/006','Âncora = docId/revision/blockId/offset UTF-16 no texto canônico; não cortar grafemas; índice normalizado mantém mapa inverso para a versão original','Número de página/coordenadas: inválidos ao repaginar; EPUB CFI puro: não cobre TXT/PDF uniformemente; trecho de contexto sem revisão: ambiguidade','blockId estável dentro da mesma revisão, por identidade de origem e ordinal; revisão muda se extração muda. Trecho/contexto pode sugerir remapeamento, sempre com confirmação; jamais mover nota silenciosamente','Testar emoji, diacríticos combinantes, ligaduras e trechos repetidos. Revisão sem bloco correspondente mantém órfã e exportável'),
('ADR-006','Isolamento, dados e governança','OBJ-004, FLOW-001/006/007','Renderer com contextIsolation true, sandbox true, nodeIntegration false; bridge allowlist tipada; parser em processo utilitário restrito; recursos de EPUB nunca executados','Carregar EPUB diretamente com scripts: risco inaceitável; permitir file paths livres no IPC: acesso excessivo; telemetria de conteúdo: desnecessária','Processo separado não é sandbox de SO por si só. Limitar permissões e validar IPC no host. Bloquear rede/subrecursos de documentos; política CSP restrita. Não há criptografia própria: confidencialidade em repouso depende da conta/volume do SO','EPUB com script, caminhos ../, ZIP bomb e links externos não executa nem lê fora do staging. Auditável antes da etapa 7; falha bloqueia suporte ao formato em vez de relaxar isolamento')]
RISKS=[
('RISK-001','Alto','Parser/EPUB hostil acessa dados ou executa script','Responsável técnico de segurança (a designar)','Isolamento/allowlist, nenhum script remoto, normalização de caminho, proibir symlinks','TEST-010: entradas hostis, tráfego zero, tentativa de path traversal','Abandonar job, apagar staging e manter acervo anterior'),
('RISK-002','Alto','Extração PDF muda ordem/some texto','Responsável de ingestão (a designar)','Prévia obrigatória nos alertas; corpus gold; nunca garantir fidelidade universal','TEST-001/002: corpus PDF difícil e fonte lado a lado','Recusar arquivo e preservar original; reabrir ADR-002'),
('RISK-003','Alto','Layout perde/repete texto ou âncora','Responsável de composição/leitura (a designar)','Texto único, mapeamento canônico e generation','TEST-003/004/007: contagem/ordem/Unicode/zoom','Voltar ao último perfil/mapa válido; modo acessível com aviso'),
('RISK-004','Alto','Excluir/restaurar destrói acervo errado','Responsável de persistência (a designar)','Confirmar impacto, tokens limitados, staging validado, troca de geração e rollback','TEST-008/009/011: falha em cada ponto e hash corrompido','Restaurar geração anterior íntegra; nunca apagar original externo'),
('RISK-005','Alto','Backup/documentos expõem conteúdo privado','Responsável técnico/produto (a designar)','Aviso de backup em claro, sem logs de conteúdo, sem rede, uso da proteção do SO','TEST-010/012: inspecionar saída de rede e logs com conteúdo sentinela','Interromper exportação/envio indevido e eliminar staging; usuário controla cópias externas'),
('RISK-006','Alto','Documento grande esgota memória/trava UI','Responsável técnico de desempenho (a designar)','Limites por etapa, um job pesado, cancelamento, virtualização de páginas','TEST-013: documento limite e bomba de descompressão','Cancelar job isolado e manter leitura/acervo responsivos'),
('RISK-007','Médio','Quatro colunas dificultam leitura em telas pequenas','Responsável de produto (a designar)','Folha virtual e modo acessível explícito; estudo de conforto','TEST-004/014: zoom/teclado/leitor de tela + estudo com usuários','Mudar modo sem perder âncora; reavaliar H-002'),
('RISK-008','Médio','Dependência muda licença/API ou é vulnerável','Responsável técnico (a designar)','Auditar versões/licenças, SBOM e lockfile antes de implementar','TEST-015: inventário e atualização controlada','Fixar versão anterior segura ou trocar adaptador; sem distribuir dependência não aprovada')]

def stage6():
 d=STAGES[5]
 write(f'{d}/06_Arquitetura.md','''# Arquitetura proposta

Seis componentes lógicos, justificados por fluxos: (1) shell desktop/UI e bridge, FLOW-001–007; (2) módulo ingestão e adaptadores, FLOW-001; (3) módulo composição, FLOW-001/002; (4) módulo leitura/índice, FLOW-003–005; (5) módulo acervo/repositórios, FLOW-001/004–007; (6) processo utilitário de tarefas, FLOW-001/003. SQLite e filesystem são recursos de persistência do componente 5, não domínios novos.

Camada privilegiada faz seleção de arquivo, tokens e escrita. UI em renderizador isolado contém conteúdo sanitizado, nunca o HTML arbitrário do EPUB. O processo de importação recebe bytes/recursos limitados, sem acesso amplo ao disco ou rede. Nenhuma API remota, autenticação, broker, nuvem ou servidor. Proteção de sessão herda a conta do sistema operacional; não se promete segurança em computador compartilhado desbloqueado.

Stack candidata: Electron/TypeScript/HTML/CSS, SQLite, PDF.js e bibliotecas ZIP/XML escolhidas após prova técnica e auditoria. Não definir versões inventadas ou “última versão” no plano; registrar versões exatas e licenças antes da etapa 7. Sem necessidade de framework React neste estágio.

Caminho: arquivo selecionado → token → validação/adaptador → DocumentoNormalizado → prévia/aceite → persistência → composição de quatro colunas → ação de leitura → âncora/nota → persistência. Índice e layout são descartáveis; texto/revisões/notas são canônicos.

Estrutura proposta, sem código implementado: `src/domains/{ingestao,composicao,leitura,acervo}`; `src/desktop/{main,preload}`; `src/ui`; `src/tasks`; contratos compartilhados sem regra de negócio. A etapa 7 poderá materializar essa estrutura.

Distribuição futura: desktop, plataforma piloto a confirmar; hipótese inicial Windows 11 x64, demais SOs após validar caminhos/fontes/sandbox. Empacotamento/assinatura, atualização e deploy ficam pendentes de autorização técnica. Não há publicação neste planejamento. Adoção do runtime depende de aprovação de ADR-001/006 e das provas da matriz de verificação.
''',id='ARCH-001',stage=6)
 for aid,title,origin,decision,alts,conseq,proof in ADRS:
  write(f'{d}/decisoes/{aid}.md',f'''# {aid} — {title}

Origem: {origin}. Estado: Proposta v1.0; decisão humana técnica pendente.

Contexto: entregar a formatação editorial solicitada sem acrescentar infraestrutura sem finalidade. Decisão candidata: {decision}.

Alternativas e tradeoffs: {alts}. Consequências/limites: {conseq}.

Critério de confirmação/refutação e retorno: {proof}. Validação de viabilidade será executada antes de adotar este ADR em código. Uma prova que falhe reabre este ADR e apenas UC/NUC/FLOW dependentes; não reduz controles para manter a opção preferida.

Fontes técnicas oficiais: Referencias_Tecnicas.md; consulta em 26/10/2026. Fonte documental descreve capacidade/restrição, não teste da combinação proposta. Responsável futuro: técnico a designar; revisora independente e aprovação pendentes. Nenhum ADR está aprovado pelo IQE.
''',id=aid,stage=6)
 write(f'{d}/Riscos_e_Controles.md','# Matriz de riscos\n\n'+table(['ID','Nível','Cenário','Papel responsável','Mitigação','Verificação planejada','Retorno'],RISKS)+'''\nClassificação qualitativa: Alto quando compromete conteúdo, privacidade ou fluxo central; Médio quando há recuperação ou afeta conveniência. Não há probabilidades inventadas. Seis riscos altos têm controles/testes/retorno; isso não os torna aceitos ou testados. Responsáveis são papéis; pessoas ainda não foram designadas. Falha em controle essencial impede implementação/distribuição até correção e aprovação técnica.
''',id='RISK-MAPA',stage=6)
 write(f'{d}/Contratos_Transversais.md','''# Contratos, limites e invariantes

## Envelope e confiança

Comando local: `{commandId:uuid, type:enum, docId?:uuid, revision?:sha256, expectedVersion?:int, payload:validated}`. Resposta: `{commandId,status:ok|pending|error,version?,data?,error?:{code,retryable}}`. Evento: `{eventId,sequence,commandId,docId?,type,status,errorCode?}`. Nunca expor SQL, execução de shell ou abertura de caminho arbitrário à UI. Tokens são opacos, curtos e ligados à janela/comando; duração de 15 minutos ou revogação ao fechar/cancelar. Validação de remetente IPC ocorre no host.

## Documento e texto

TXT UTF-8 padrão; BOM suportado; se decodificação substituir caracteres, pedir codificação ou recusar, sem silenciosamente salvar “�”. Detectar UTF-16 por BOM; codificação legada depende de escolha explícita. Preservar parágrafos; finais de linha normalizados; espaços e pontuação não são “corrigidos” por IA.

PDF: camada textual por página, referências de origem, agrupamento heurístico por coordenadas, alerta de possível ordem ruim. Imagem sem texto e proteção são recusadas. Não prometer extração de fórmulas/tabelas complexas. Tabela extraída de forma ambígua exige alerta e não vira texto supostamente fiel.

EPUB: container e package válidos, spine na ordem canônica; navegação gera sumário quando disponível; conteúdo não linear acessível por link interno se textual. Remover scripts/estilos ativos, handlers e recursos externos. Texto alternativo de imagem é exibido como bloco identificado; imagem sem alt gera aviso; preservação visual de figuras não é objetivo. Tabelas simples podem ser linearizadas com aviso; estruturas não textuais complexas são diagnosticadas. Notas e links internos resolvem âncoras de origem; link externo só abre navegador após ação explícita e confirmação de saída, nunca durante importação.

## Limites iniciais — hipóteses de capacidade

Até 50 MiB por arquivo; PDF até 2000 páginas; EPUB até 10000 entradas, 200 MiB descompactados e razão máxima 100:1 por entrada; documento normalizado até 5 milhões de caracteres UTF-16. Exceder qualquer limite interrompe antes de commit e mostra LIMIT. Biblioteca até 1000 obras no piloto, índice por obra carregado sob demanda. Nota até 10000 caracteres, consulta 1–256, 100 resultados por lote. Limites são configuração versionada do produto, não propriedade conhecida das bibliotecas.

Validação de ZIP: contagem/tamanho real durante leitura, proibir paths absolutos, `..`, symlinks, nomes equivalentes após normalização e colisões case-insensitive. XML sem entidades externas/DTD e com limite de profundidade 128. Arquivos restaurados não escapam do staging. Checagem de espaço livre é estimativa e não substitui tratamento de erro de I/O.

## Paginação e âncoras

Folha de largura padrão 1184px, margens internas 24px, três gutters de 24px: largura útil de texto por coluna = (1184 − 48 − 72)/4 = 266px. Altura útil deriva da janela descontando controles/margens e nunca é infinita. Fonte inicial serif 18px, entrelinha 1,5; carregar fontes antes de medir. Não usar column-width que altere count sem controle; contabilizar overflow em grupos de quatro colunas. Última folha pode ter colunas vazias.

Âncoras não dependem de coluna/folha. Offset UTF-16 no texto canônico com ajuste para fronteiras de grafema. Índice pode usar normalização para comparação, mas retorna offsets pelo mapa inverso. Alterar perfil incrementa generation; resultado antigo é descartado. Títulos são blocos, hifenização apenas visual; buscar usa texto sem hifens visuais. Palavra longa admite quebra de emergência sem inserir caracteres no canônico. Modo acessível usa uma coluna refluível, ativada explicitamente e anunciada.

## Persistência e recuperação

Posição salva com debounce alvo 500ms após movimento, em mudança de obra e no fechamento; só “salvo” após commit. Encerrar abruptamente antes do commit pode perder o último movimento e deve ser risco explícito; nota nunca some sem aviso de rascunho. Repetir commandId retorna resultado lógico existente. Não há conflito entre dispositivos; concorrência local usa expectedVersion e único escritor.

Backup v1: manifesto com schemaVersion, snapshotId, obras/revisões/âncoras e hashes SHA-256; exportação lógica consistente para ZIP local, sem caminhos absolutos. Hash detecta corrupção, não autentica origem; backup não confiável sempre é validado. Restauração substitui acervo inteiro com confirmação, sem merge silencioso. Preparar geração nova, flush/fsync quando suportado, validar, gravar diário de intenção e trocar ponteiro; iniciar reconciliando diário. Preservar geração anterior até confirmar abertura; rollback retorna ponteiro anterior. Não afirmar atomicidade conjunta banco/filesystem apenas por usar SQLite.

Exclusão bloqueia novas escritas da obra e invalida sessões; primeiro remove referências em transação, depois remove blobs sem referência. Falha posterior é pendência de limpeza visível, não rollback fictício de arquivo apagado. Não apagar originais ou cópias externas. Índice é reconstruível; nunca restaurar índice de versão incompatível como fonte de verdade.
''',id='CONTRACT-001',stage=6)
 write(f'{d}/Governanca.md','''# Governança técnica proposta

Documentos e decisões estão em Proposta. G6 exige ratificação técnica das versões exatas e designação dos papéis. A autorização de produção automática do plano não publica aplicativo nem aceita riscos operacionais. CHG-001 rege passagem documental com 75 e revisão limitada; LIM-001 deve ser resolvida por revisão independente antes de implementação relevante.

Sem conta/servidor, autenticação de produto é N/A. Usuário local do SO é a fronteira; outros usuários do mesmo perfil podem acessar o acervo. Texto/nota pode conter informação sensível; nenhum conteúdo, título, consulta ou caminho absoluto vai para telemetria. Sem coleta automática e sem promessa jurídica de conformidade. Backups em claro exigem aviso e destino escolhido.

Logs locais: IDs técnicos sem conteúdo, duração/errorCode e versão; rotação de sete dias, exclusão pelo usuário. Diagnóstico exportado só por ação explícita e prévia. Relatório não inclui texto/nota/caminho original. Dados canônicos ficam até exclusão; resíduos temporários são limpos no início; backups externos não são apagados pelo aplicativo.

Agentes futuros trabalham em sandbox, com corpus sintético ou autorizado e permissões mínimas. Sem acessar diretórios arbitrários, enviar documentos, registrar credenciais ou instalar serviços externos. Changes que afetem formatos, âncoras, schema ou segurança reabrem origem e descendentes: documento → núcleo → fluxo → ADR/testes. Nunca aprovar a própria mudança como revisão independente.

Plano de migração: schemaVersion monotônico; backup pré-migração, transação e validação de contagens/âncoras. Falha restaura snapshot anterior. Downgrade não abre schema futuro; oferecer restauração compatível. Nenhuma migração executada nesta entrega. Responsável técnico deve provar rollback com falha injetada antes da etapa 7.

Exclusão/restauração futuras exigem confirmação na interface; a presente produção não manipula acervo real. Publicação, assinatura de instalador e atualização exigem autorização própria. Revisão técnica e humana mantém gates G1A/G1B/G2/G3/G4/G5/G6 pendentes até ratificação.
''',id='GOV-001',stage=6)
 tests=[]
 for row in UCS:
  tests.append((f'TEST-{row[0][-3:]}',f'AC-{row[0][-3:]}',row[3],row[8],'Planejado; não executado'))
 tests += [('TEST-010','RISK-001, RISK-005','Segurança/adversarial','EPUB com scripts/DTD/traversal/bomba e IPC adulterado: nada executa, nada sai do staging, zero rede, nenhum texto sentinela em logs','Planejado'),('TEST-011','RISK-004, ADR-004','Falha e rollback','Injetar falha em staging, blob final, commit, ponteiro e início: sempre abre geração anterior ou nova íntegra; sem referência quebrada','Planejado'),('TEST-012','OBJ-004, RISK-005','Privacidade','Abrir arquivo com texto sentinela e monitorar rede/logs; nenhum byte do conteúdo em rede/log; backup avisa em claro','Planejado'),('TEST-013','RISK-006','Desempenho e limites','Corpus limite/corpus excedente: recusa controlada, cancelar ≤2s; limite de memória alvo 1GiB para 1 milhão de caracteres; sem crash do acervo','Planejado'),('TEST-014','FEAT-004/005, RISK-007','Acessibilidade e conforto','Teclado integral, leitor de tela, foco, contraste 4,5:1; zoom 200% modo acessível sem rolagem horizontal; estudo com 5 leitores sem alegar eficácia','Planejado'),('TEST-015','ADR-001/002/006, RISK-008','Dependências','Registrar versões, licenças, hashes e vulnerabilidades de Electron, PDF.js, ZIP/XML e SQLite; impedir distribuição com risco alto sem tratamento','Planejado')]
 write(f'{d}/Plano_de_Verificacao.md','# Verificações futuras do produto\n\n'+table(['ID','Origem','Escopo','Oráculo/aceite','Estado'],tests)+'''
## Corpus planejado e critérios de fidelidade

Preparar 24 arquivos sintéticos/abertos com referência legível: 4 TXT (UTF-8, BOM, UTF-16, codificação ambígua), 6 PDFs textuais (simples, duas colunas, ligaduras, hifenização, tabela, notas), 4 EPUB refluíveis (sumário, notas, imagem/alt, capítulos não lineares), 4 recusas (PDF imagem/protegido, EPUB fixo/DRM), 6 adversariais/limites (ZIP traversal, bomb, XML externo, script, arquivo excedente, truncado). Manifesto fixa hash, licença/permissão e saída esperada por arquivo. Ainda não criado nem executado.

Para TXT e EPUB textual suportado: igualdade do texto normalizado conforme regras explícitas, sem reescrita. Para PDF: referência manual de sequência de blocos por página; falha relevante de ordem ou conteúdo exige diagnóstico/rejeição da entrada, não nota de fidelidade fictícia. Para layout: sequência de intervalos concatenada deve reconstruir o documento uma vez; contagens não bastam sem ordem e Unicode.

Metas de desempenho hipotéticas em máquina piloto 4 núcleos, 8GiB RAM, SSD: obra de 1 milhão de caracteres abre layout inicial em até 3s após normalização; importação até 30s para corpus comum; feedback de ação em até 250ms; cancelamento até 2s; avanço de folha p95 até 100ms em 100 ações após aquecimento. Medir 10 execuções frias por classe e registrar distribuição, ambiente e versões. Nenhuma meta é benchmark já obtido.

Camadas previstas: unitários de normalização/âncoras/invariantes; integração de parser–documento–persistência; contratos IPC; E2E das sete jornadas com falha; inspeção manual de extração/acessibilidade e prova de segurança. Defeito injetado deve fazer a verificação falhar para provar sensibilidade.

EV-001–015 reservados a evidências futuras dos TEST correspondentes; não há evidências de produto nesta entrega. Registrar comando, ambiente, versão, corpus, resultado esperado/obtido, captura redigida quando necessário e limites. A aceitação requer revisão independente e gate humano; 75 documental não substitui o teste funcional.
''',id='TEST-PLANO',stage=6)
 write(f'{d}/Referencias_Tecnicas.md','''# Fontes primárias e limites — consulta 26/10/2026

| ID | Fonte | Fato limitado observado | Uso / hipótese da proposta |
| --- | --- | --- | --- |
| REF-004 | https://www.electronjs.org/docs/latest/tutorial/security/ | Documentação recomenda isolamento e cuidados com conteúdo/IPC | Configuração explícita em ADR-006; não prova segurança do produto |
| REF-005 | https://www.electronjs.org/docs/latest/tutorial/sandbox | Acesso privilegiado pode escapar por bridge/preload | Parser em outro processo também precisa privilégio mínimo |
| REF-006 | https://sqlite.org/atomiccommit.html | Transações do SQLite têm mecanismo de commit atômico | Consistência com blobs externos exige protocolo adicional |
| REF-007 | https://www.sqlite.org/lang_transaction.html | COMMIT pode falhar e transação pede tratamento | Erros e retry explícitos em API-008 |
| REF-008 | https://mozilla.github.io/pdf.js/getting_started/ | PDF.js expõe camadas de processamento e exibição | Candidato a parser, sem garantia de ordem textual |
| REF-009 | https://github.com/mozilla/pdf.js/blob/master/examples/node/getinfo.mjs | Exemplo oficial usa getTextContent | Viabilidade de extração a confirmar no corpus |
| REF-010 | https://www.w3.org/TR/css-multicol-1/ | Especifica column-count e column-fill | Paginação e mapeamento ainda são trabalho do aplicativo |
| REF-003 | https://www.w3.org/TR/epub-33/ | Spine define ordem primária | Parser deve respeitar capítulos e sinalizar recursos não suportados |

Fontes pesquisadas; não se testou combinação de runtime, bibliotecas e formatos. Decisões são inferências de engenharia explicitamente propostas. Sem versões, licenças ou desempenho inventados.
''',id='REF-TECNICAS',stage=6)

if __name__=='__main__':
 n=int(sys.argv[1]); prev=json.loads((ROOT/f'Avaliacoes/E{n-1}.json').read_text());assert min(r['IQE'] for r in prev if r['IQE'] is not None)>=75
 {4:stage4,5:stage5,6:stage6}[n]()
 run(n)
