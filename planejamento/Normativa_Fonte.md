# Normativa de Criação de Software com Inteligência Artificial

**Versão:** 2.0 — Proposta integral de reorganização orientada a modelos de produto, domínios, artefatos e núcleos de interação  
**Estado:** **PROPOSTA — PENDENTE DE APROVAÇÃO HUMANA**  
**Data da proposta:** 23/10/2026  
**Origem:** reestruturação conceitual das normativas v1.3/v1.4 e da descrição explícita do processo desejado pelo responsável.  
**Abrangência:** concepção, especificação, arquitetura, implementação, validação, operação e evolução de software com IA.  
**Natureza:** método operacional independente; preserva controles úteis de especificação, revisão, risco e rastreabilidade inspirados no AICD, sem reivindicar conformidade integral com o método externo.  
**Precedência:** esta proposta **não substitui automaticamente** documentos anteriormente aprovados. A adoção depende de decisão humana registrada e plano de migração.

> **Regra-mãe:** **ideia → modelos de produto → conjuntos de features → domínios → artefatos por domínio → núcleos funcionais → núcleos/fluxos de interatividade → arquitetura → execução → validação → operação**. Cada avanço exige conteúdo Markdown versionado, avaliação específica de qualidade/maturidade, retrabalho quando necessário, síntese visual fiel e **decisão humana nos gates**. IA propõe, estrutura, produz e verifica; pessoas escolhem e autorizam.

---

## 1. Objetivo, princípios e limites

### 1.1. Objetivo

Estabelecer uma forma reprodutível de transformar uma ideia inicial, mesmo vaga, em um software cujo produto, responsabilidades e comportamentos sejam explicitamente escolhidos e compreensíveis. A IA conduz a elaboração progressiva; o responsável humano intervém em **decisões de produto e gates**, sem precisar ditar antecipadamente cada requisito.

### 1.2. Princípios inegociáveis

1. **Modelo de produto antes de listas de requisitos:** a IA começa explorando categorias e referências existentes; um modelo inteiramente novo também é opção legítima.
2. **Duas decisões distintas na concepção:** escolher o **modelo de produto** e escolher/combinar **ao menos dois conjuntos alternativos de features**. Uma escolha não aprova automaticamente a outra.
3. **Domínios antes de detalhes técnicos:** a distribuição de responsabilidades de negócio é aprovada antes da modelagem aprofundada por domínio.
4. **Especificar dentro do domínio:** casos de uso, entidades, serviços, workers, mensageria e telas têm dono, IDs e vínculos explícitos.
5. **Não obrigar componentes desnecessários:** um domínio pode dispensar API remota, worker, mensageria, persistência própria ou tela, mediante `N/A` fundamentado. Não criar arquivos ou componentes vazios para cumprir ritual.
6. **Compor, não confundir:** *artefato* descreve uma peça; *núcleo* articula peças em uma responsabilidade executável; *fluxo* descreve a experiência e o percurso completo entre núcleos e domínios.
7. **Avaliar no menor nível útil:** cada subetapa/artefato de cada domínio recebe avaliação antes de compor um núcleo; cada núcleo, fluxo e etapa agregadora recebe avaliação própria.
8. **Retrabalho causal e seletivo:** corrigir a primeira fonte onde nasceu o erro e rever apenas descendentes afetados; não reiniciar o projeto inteiro por padrão.
9. **Markdown como fonte de verdade:** decisões, especificações, métricas, evidências, histórico e fontes de diagramas ficam em `.md` e arquivos auxiliares versionados. Figuras ajudam a decidir, não governam requisitos.
10. **IA produtora ≠ IA revisora:** revisão independente de sessão/contexto é exigida; outro modelo e/ou revisão humana são preferíveis em mudanças relevantes. A IA não se autoaprova.
11. **Evidência com estado explícito:** distinguir fato pesquisado, relato, hipótese, opção, decisão aprovada e resultado testado. Não inventar exemplos de mercado, pesquisas, testes, commits ou aprovações.
12. **Risco proporcional com autoridade humana:** identidade, segurança, dados sensíveis, pagamentos, contratos externos, migrações e publicação têm controle reforçado.
13. **Escopo é verificável:** cada funcionalidade e fluxo deve apontar para benefício ou obrigação legítima, critérios de aceite e modo de observação.
14. **Visualização reproduzível:** criar diagrama legível ao fim de cada etapa/subetapa relevante, com legenda, fontes, versão, estado e descrição acessível. Quando possível, usar Mermaid/SVG editável.
15. **Independência de plataforma:** o repositório Git é recomendado para versionamento e revisão; Drive pode servir como cópia/referência, sem duas fontes de verdade concorrentes.

### 1.3. O que não se infere desta normativa

A busca de produtos similares **não** prova validação de mercado; referência comercial **não** é licença para copiar código, marca, telas ou conteúdo de terceiros. IQE elevado **não** substitui teste real nem aceitação humana. Diagramas de uma arquitetura proposta **não** comprovam funcionamento. Uma proposta de API/worker **não** exige que ela exista quando o caso puder ser executado localmente.

### 1.4. Vocabulário operacional

| Conceito | Definição normativa |
|---|---|
| **Ideia** | Intenção inicial e contexto fornecidos pelo humano, ainda sem escopo decidido. |
| **Modelo de produto** | Categoria ou padrão de produto conhecido, combinação referencial, ou modelo livre/original. |
| **Conjunto de features** | Alternativa **coerente** de funcionalidades com escopo, custo relativo, riscos e objetivos próprios. |
| **Domínio** | Fronteira de responsabilidade de negócio/sistema com linguagem própria, comportamentos e proprietário lógico. Não é sinônimo de pasta ou microsserviço. |
| **Caso de uso** | Objetivo/ação observável de um ator ou evento; define comportamento e exceções. |
| **Entidade** | Conceito/dado persistente ou de estado relevante, incluindo regras e ciclo de vida; não equivale automaticamente a tabela. |
| **Serviço** | Responsabilidade/processamento síncrono ou sob demanda, local ou remoto; API é sua interface quando aplicável. |
| **Worker** | Execução assíncrona, periódica ou em segundo plano; não é serviço obrigatório. |
| **Mensageria** | Evento, notificação, comunicação ao usuário/sistema ou integração, incluindo canal, destinatário e contrato. |
| **Tela** | Interface/experiência de interação, inclusive estados e permissões; pode não existir em um domínio headless. |
| **Núcleo** | Composição rastreável de casos de uso e artefatos que presta uma capacidade funcional. |
| **Núcleo de interatividade** | Composição de tela(s) e um ou mais núcleos/capacidades que sustenta uma interação utilizável. |
| **Fluxo** | Sequência ponta a ponta, com respostas e erros, eventualmente cruzando domínios e núcleos. |
| **Gate** | Ponto explícito de decisão humana, instruído por avaliação e evidências, nunca substituído por nota. |
| **Retrabalho** | Correção documentada, orientada por causa e reavaliada, de artefato/núcleo/fluxo/etapa. |

---

## 2. Arquitetura do processo e responsabilidades

### 2.1. Etapas e decisões

| Etapa | Transformação principal | Unidade mínima avaliada | Decisão / gate | Diagrama obrigatório ou dispensa fundamentada |
|---|---|---|---|---|
| **1 — Concepção** | Ideia → modelo de produto → conjuntos de features → escolha | 1A modelo; 1B cada conjunto; consolidado | **G1A** modelo, **G1B** features | comparação de modelos + mapa de features aprovado |
| **2 — Domínios** | Features → fronteiras e responsabilidades | cada `DOM` + mapa geral | **G2** mapa de domínios | mapa de domínios, relações e features |
| **3 — Artefatos por domínio** | `DOM` → UC, DATA, API/SVC, JOB, MSG e VIEW | **cada tipo por domínio**, incluindo `N/A` | **G3.DOM.TIPO**, agregado **G3.DOM** | mapa de artefatos do domínio e diagramas de tipo pertinentes |
| **4 — Núcleos** | Artefatos → back-end, rotina, notificação e interatividade | **cada núcleo** por domínio | **G4.NUC**, agregado **G4.DOM** | mapa de composição e dependências dos núcleos |
| **5 — Fluxos** | Núcleos → jornadas completas e integrações | **cada `FLOW`** | **G5.FLOW**, agregado **G5** | sequência/atividade ponta a ponta e estados |
| **6 — Arquitetura** | Plano funcional → decisões técnicas, riscos e verificações | ADR, contratos transversais, arquitetura | **G6** | componentes, limites, ADR, segurança e dados |
| **7 — Execução** | Arquitetura/fluxos → roadmap, tickets, código e testes | **cada `TKT`** e incremento | **G7.TKT**, **G7.INC** | roadmap e status de entrega com evidência |
| **8 — Validação/entrega** | Incremento → aceitação comprovada e decisão de release | `AC`, fluxo, incremento/release | **G8** autorização explícita | painel de aceitação e riscos |
| **9 — Operação/evolução** | Release → sinais, correções e retorno ao planejamento | incidente, sinal, mudança | **G9** prontidão; revisões periódicas | ciclo de observação/decisão/evolução |

**Não substituir a ordem da vontade do usuário:** a **Etapa 1** começa com a ideia e inclui ambas as aprovações de modelo e features; a **Etapa 2** é a divisão em domínios; a **Etapa 3** é o trabalho detalhado **por domínio**. Etapas seguintes tornam o plano executável e sustentável.

### 2.2. Papéis e segregação

| Papel | Faz | Não faz sem autorização |
|---|---|---|
| **Responsável pelo produto — humano** | fornece ideia; escolhe modelo, features, domínios; aprova escopo, jornadas e gates de produto | delegar à IA decisão final de valor/escopo |
| **Responsável técnico — humano** | aprova fronteiras de alto impacto, contratos, arquitetura, dados, segurança e rollback | permitir mudança estrutural silenciosa |
| **Responsável de qualidade — humano** | valida suficiência de critérios, revisão e evidências; autoriza entrega segundo risco | aceitar "a IA disse que funciona" como prova |
| **IA exploradora de produto** | investiga modelos reais, registra fontes/data, propõe conjuntos; explicita lacunas | inventar produtos, inferir validação, decidir em nome do humano |
| **IA especificadora por domínio** | escreve artefatos Markdown, vincula IDs e faz propostas | aprovar o próprio trabalho |
| **IA diagramadora** | gera fonte editável, imagem e descrição | inventar estados/conexões ausentes da fonte |
| **IA revisora independente** | procura contradições, cenários adversos e vínculos órfãos; recomenda retrabalho | mudar escopo/aprovar gate |
| **IA implementadora** | planeja ticket e codifica em branch | merge/publicação unilateral em itens controlados |
| **IA verificadora** | desenha/roda verificações proporcionais e registra provas | enfraquecer teste para "passar" |
| **IA operacional restrita** | lê sinais, prepara relatórios, executa runbooks autorizados | acesso irrestrito, exclusão ou alteração de produção |

Um humano pode acumular papéis humanos. Em projeto individual, separar ao menos **execução de IA autora e revisão de IA revisora**; registrar quando a independência efetiva for limitada e aplicar o risco correspondente. A aprovação humana continua obrigatória em cada gate de escopo consolidado e nos gates técnicos relevantes. Aprovações de lotes são permitidas se citarem **todos os IDs/versões aprovados**.

### 2.3. IDs estáveis e cadeia de rastreabilidade

| ID | Conteúdo | ID | Conteúdo |
|---|---|---|---|
| `IDEA-###` | entrada conceitual | `REF-###` | referência externa com data/fonte |
| `MOD-###` | opção de modelo de produto | `SET-###` | conjunto alternativo de features |
| `FEAT-###` | feature | `DOM-###` | domínio |
| `UC-###` | caso de uso | `AC-###` | critério de aceite |
| `DATA-###` | entidade/estado | `API-###` | serviço/API ou processamento local |
| `JOB-###` | worker/rotina | `MSG-###` | evento/notificação/mensagem |
| `VIEW-###` | tela/interface | `NUC-###` | núcleo funcional/interativo |
| `FLOW-###` | fluxo ponta a ponta | `ADR-###` | decisão arquitetural |
| `TKT-###` | ticket | `TEST-###` | verificação/teste |
| `EV-###` | evidência | `DIAG-###` | diagrama |
| `CHG-###` | mudança de especificação/decisão | `HST-####` | histórico de avaliação/retrabalho |
| `REL-###` | release/versão de entrega | `INC-###` | incremento vertical |

**Exemplo exclusivamente ilustrativo:**  
`IDEA-001 → MOD-002 → SET-001 → FEAT-003 → DOM-002 → UC-007 → [DATA-004, API-005, MSG-002, VIEW-003] → NUC-004 → FLOW-003 → AC-011 → TKT-012 → TEST-009 → EV-006 → REL-001`.

A relação é um **grafo**, não uma exigência de que todas as peças sejam usadas em toda cadeia. IDs não são reutilizados nem renumerados após aprovação. Itens excluídos ficam `Substituído`/`Descontinuado`, mantendo justificativa e referência `CHG/HST`.

### 2.4. Estados e rastreabilidade temporal

- **Artefato:** `Rascunho | Proposta | Em revisão | Aprovado | Substituído | Descontinuado`.
- **Avaliação:** `Não iniciada | Em avaliação | Aprovada para gate | Reprovada | Reavaliada`.
- **Gate:** `Pendente | Aprovado | Reprovado | Reaberto | Dispensa parcial aprovada` (dispensa de artefato, não de obrigação crítica).
- **Achado:** `Aberto | Em correção | Verificado | Aceito com risco (somente se elegível) | Reaberto`.

Cada Markdown canônico informa `id`, `etapa`, `dominio` (quando pertinente), `versao`, `estado`, `fontes`, `ids_relacionados`, `responsavel`, `revisor`, `avaliacao`, `diagrama`, `gate`, `aprovado_por`, `aprovado_em`, `commit_pr` (se houver). Campos desconhecidos devem ficar `null`/`Pendente`, nunca preenchidos por suposição. O gate aprovado é válido **para uma versão exata**, não para qualquer edição futura.

---

## 3. Etapa 1 — Concepção: da ideia ao modelo e às features

### 3.1. Subetapa 1A — Interpretação e seleção do modelo de produto

**Entrada:** descrição livre do humano (`IDEA`), restrições, público imaginado, referências e resultados desejados. A IA faz perguntas **apenas para lacunas decisivas**, registra outras como hipóteses e não bloqueia a elaboração de opções por falta de pormenores.

**Procedimento:**

1. Registrar literalmente a ideia original e produzir uma **interpretação separada** (problema, público potencial, tarefas desejadas, resultado mensurável, não objetivos e suposições).
2. Pesquisar/identificar **categorias e produtos existentes** análogos; buscar fonte oficial e, quando útil, contexto independente. Em cada referência `REF-...`, registrar **nome, URL, data da consulta, capacidade observada, limite de comparação e grau de confiança**. Não declarar pesquisa real se acesso externo não foi realizado; listar referências de memória como **não verificadas**.
3. Oferecer **pelo menos duas opções materialmente distintas de modelo**, quando houver modelos plausíveis; recomendar até 3–4 para não sobrecarregar, além de **"Modelo livre/original"** sempre disponível. É válido propor mistura de referências.
4. Comparar com as **mesmas dimensões**: aderência à ideia, público, ganhos, limitações, complexidade relativa, riscos, dependências, diferenciais e pontos ainda não demonstrados. Não inventar preço/participação de mercado.
5. Recomendar a opção mais coerente **sem decidir pelo humano**. Registrar a escolha e o que não será copiado ou assumido.
6. Fazer avaliação `AV-1A` e retrabalho se necessário. Obter **G1A** com ID de modelo escolhido (ou `MOD-LIVRE` registrado com ID estável).

**Saídas:** `planejamento/01_Concepcao/Ideia_e_Contexto.md`, `Modelos_de_Produto.md`, `Referencias_de_Mercado.md`, avaliação e `DIAG` comparativo. **Bloqueio:** opção apresentada como fato de mercado sem fonte/ressalva, ausência de escolha humana, modelo que contradiz objetivo declarado.

**Métricas específicas de 1A** (medir N/D, meta 100% dos aplicáveis):

- `P1A-01` = modelos propostos com análise comparável **/ modelos propostos**.
- `P1A-02` = afirmações factuais de mercado com fonte datada **ou rótulo não verificado / afirmações factuais de mercado**.
- `P1A-03` = objetivos de valor com público, necessidade e forma de aferição **/ objetivos prioritários**.
- `P1A-04` = alternativas distintas e decisão registrada (`Sim/Não`, exigência de 2 opções **quando plausível** + caminho livre).

**Retrabalho mental:** "qual parte veio da ideia, qual veio de mercado, qual é hipótese da IA?"; eliminar falsa analogia e refazer comparação com critérios constantes. **G1A aprova somente o modelo**, não features futuras.

### 3.2. Subetapa 1B — Proposição, comparação e aprovação de conjuntos de features

**Entrada:** modelo aprovado (incluindo livre), problema e público priorizados.

**Procedimento:**

1. Derivar `FEAT-...` do valor pretendido, obrigações legítimas e experiências esperadas; indicar origem `IDEA/MOD/REF` e hipótese/validação.
2. Montar **pelo menos dois `SET-...` coerentes e genuinamente diferentes** (ex.: `Essencial` vs `Equilibrado/Ampliado`). Três opções são úteis quando existe uma diferença real, mas **não obrigatórias** nesta v2.0.
3. Para cada conjunto registrar features incluídas/excluídas, jornada principal, benefícios, riscos, complexidade relativa, dependências, limites do MVP, acessibilidade/segurança pertinente e estratégia de comprovação.
4. Usar matriz **lado a lado** com a mesma escala e explicitar o custo de não incluir cada feature crítica. Permitir combinação humana dos conjuntos, produzindo `SET` consolidado distinto.
5. Verificar que toda feature atende a problema/benefício/obrigação e que o conjunto não contradiz modelo, público ou limites.
6. Avaliar **cada conjunto** com `AV-1B.SET-...`, depois avaliar a coerência do consolidado; retrabalhar opções fracas antes da decisão; obter **G1B** com lista de features **aprovadas e excluídas**.

**Saídas:** `Conjuntos_de_Features.md`, `Features_Aprovadas.md`, `Decisao_Concepcao.md`, comparação `DIAG` e ficha de avaliação. Não mover feature para `Aprovado` com base apenas na recomendação da IA.

**Métricas específicas de 1B** (metas 100%):

- `P1B-01` = features com vínculo a valor ou obrigação legítima **/ features propostas**.
- `P1B-02` = conjuntos com escopo, limites, ganhos, esforço/risco e diferença explícitos **/ conjuntos propostos**.
- `P1B-03` = features consolidadas com prioridade `agora/depois/fora` **/ features consideradas**.
- `P1B-04` = features críticas com comportamento esperado e critério inicial observável **/ features críticas**.

**Retrabalho mental:** "se removo esta feature, qual benefício se perde?"; corrigir feature órfã, duplicada, supérflua ou sem limite. **G1B** libera o mapa de domínios; não aprova arquitetura nem implementação.

---

## 4. Etapa 2 — Decomposição em domínios

**Entrada:** `SET` consolidado e `FEAT` aprovadas.

**Procedimento:**

1. Identificar capacidades de negócio e subáreas de responsabilidade; gerar candidatos `DOM-...` com **objetivo, vocabulário, regras, dados de propriedade lógica, atores, features atendidas e fronteiras**.
2. Distinguir **domínios de negócio** de serviços compartilhados e componentes técnicos. Autenticação pode ser domínio de suporte, serviço externo ou capacidade compartilhada, **segundo o projeto**, não sempre pasta obrigatória.
3. Produzir tabela `FEAT × DOM`, aceitando vínculo muitos-para-muitos; para cada feature **designar domínio responsável primário** e consumidores, evitando ambiguidade de propriedade.
4. Mapear `DOM → DOM` por eventos, contratos, dependências e informações compartilhadas. Não impor microsserviços: domínios podem coexistir em aplicação monolítica ou módulo local.
5. Quando as fronteiras forem ambíguas, apresentar **duas opções de decomposição** com comparação coesão/acoplamento; explicar por que não fundir ou não separar.
6. Avaliar **cada domínio** individualmente e depois a cobertura/global; retrabalhar domínios excessivamente amplos, fragmentados ou órfãos. Obter **G2** (pode aprovar conjunto de domínios com IDs listados).

**Saídas:** `planejamento/02_Dominios/Mapa_de_Dominios.md`, `Matriz_Features_Dominios.md`, `DOM-###/Identidade.md`, avaliações e mapa `DIAG`.

**Métricas** (meta de gate 100% nos itens críticos/aplicáveis):

- `P2-01` = features aprovadas com domínio responsável principal **/ features aprovadas**.
- `P2-02` = domínios com propósito, fronteiras, responsabilidades e dono lógico definidos **/ domínios propostos**.
- `P2-03` = dependências relevantes com origem, destino, motivo e contrato/evento previsto **/ dependências relevantes**.
- `P2-04` = regras/processos com **responsável não ambíguo** **/ regras/processos identificados**.

**Retrabalho mental:** *mapa de responsabilidade* ("quem é dono desta regra?"), *teste da remoção* ("se o domínio sumir, que capacidade desaparece?"), *teste de fronteira* ("há dois donos para o mesmo dado?"). **Bloqueio:** feature essencial sem domínio responsável ou domínio crucial com responsabilidades conflitantes.

---

## 5. Etapa 3 — Especificação de artefatos por domínio

### 5.1. Regra geral e ordem dentro do domínio

Para **cada `DOM-...` aprovado**, executar subetapas separadas e avaliá-las **antes da composição**:

`3.1 Casos de uso → 3.2 Entidades/estados → 3.3 Serviços/APIs → 3.4 Workers → 3.5 Mensageria → 3.6 Telas`.

A sequência é uma **ordem de consolidação**, não obrigação de implementação nem proibição de iteração: entidades podem revelar falta de caso; serviço pode exigir revisar critério; a correção volta à menor origem causal. Identificar sempre o universo aplicável; `N/A` para tipo ausente requer justificativa verificável e exame de seus consumidores. `G3.DOM.TIPO` aprova **o tipo dentro daquele domínio**. Somente com esses resultados explícitos, o domínio recebe `G3.DOM`.

### 5.2. Subetapa 3.1 — Casos de uso (`UC`) e critérios (`AC`)

**Gerar:** ator/evento, feature, objetivo, pré-condição, fluxo principal, exceções, permissões, pós-condição, invariantes, AC em `Dado/Quando/Então` ou equivalente; evitar especificar implementação arbitrária. Um caso automático não exige tela.

**Métricas por domínio:**

- `P3UC-01` = `UC` com `FEAT`, ator/gatilho, pré/pós-condição **/ UC aplicáveis** (100%).
- `P3UC-02` = `AC` com cenário demonstrável (condição, ação, resultado, negativo pertinente) **/ AC aplicáveis** (100%).
- `P3UC-03` = cenários críticos (sucesso, erro, permissão, idempotência quando cabível) cobertos por `AC` **/ cenários críticos identificados** (100%).

**Retrabalho:** inversão da jornada (resultado → passos → precondição), cenários adversários, remover casos que não correspondem a feature/obrigação; se o escopo muda, voltar a G1B/G2 afetados. **Bloqueia:** fluxo essencial sem resultado observável.

### 5.3. Subetapa 3.2 — Entidades, estados e propriedade dos dados (`DATA`)

**Gerar:** dono do dado, finalidade, identificador, atributos e tipos lógicos, cardinalidade, restrições, estados/transições, quem cria/lê/altera/exclui, retenção/privacidade, consumidores e estratégia de persistência. Referenciar entidade de outro domínio **sem duplicar propriedade**. Um domínio sem dado próprio registra `N/A` ou contrato de leitura pertinente.

**Métricas:**

- `P3DATA-01` = entidades com finalidade, dono e consumidores identificados **/ entidades pertinentes** (100%).
- `P3DATA-02` = regras e relações críticas com invariantes, cardinalidade e ciclo de vida **/ regras/relações críticas** (100%).
- `P3DATA-03` = dados pessoais/sensíveis relevantes com necessidade, controle de acesso e retenção/eliminação definidos **/ dados classificados aplicáveis** (100%).

**Retrabalho:** simular criação, duplicidade, mudança de estado, exclusão e recuperação; eliminar campos especulativos; pedir decisão se houver migração ou privacidade. **Bloqueia:** dupla propriedade crítica ou dado sensível sem política pertinente.

### 5.4. Subetapa 3.3 — Serviços, processamento e APIs (`API`)

**Gerar:** responsabilidade; caso de uso e `DATA` associados; processamento local/remoto; entrada, saída, validação, autorização, erros, efeitos colaterais, idempotência quando relevante, contratos e limites. Não criar API de rede apenas por padrão.

**Métricas:**

- `P3API-01` = ações que requerem processamento com executor explícito (local ou serviço) **/ ações processáveis** (100%).
- `P3API-02` = contratos aplicáveis com entrada, saída, erros e permissões **/ contratos aplicáveis** (100%).
- `P3API-03` = efeitos colaterais críticos com proteção contra duplicidade/falhas **/ efeitos críticos** (100%).

**Retrabalho:** traçar sequência do pedido até resposta/erro, buscar responsabilidades repetidas, verificar se solução local basta; revisar contratos antes de código. **Bloqueia:** autorização ausente em ação protegida ou contrato crítico ambíguo.

### 5.5. Subetapa 3.4 — Workers e rotinas (`JOB`)

**Gerar quando necessário:** gatilho, periodicidade, entrada, entidade/estado que lê ou altera, execução, dependência, reprocessamento, concorrência, falhas/retries, observabilidade, limites e efeito sobre casos de uso. "Processo de fundo" não é automaticamente worker separado.

**Métricas:**

- `P3JOB-01` = jobs aplicáveis com gatilho, execução, condições de término e consumidores **/ jobs aplicáveis** (100%).
- `P3JOB-02` = jobs sujeitos a reexecução com idempotência, repetição e tratamento de falha **/ jobs com risco de repetição** (100%).
- `P3JOB-03` = resultados críticos de jobs com forma de acompanhamento/verificação **/ resultados críticos de jobs** (100%).

**Retrabalho:** simular execução repetida, atrasada, simultânea e falha no meio; preferir execução síncrona se não houver necessidade comprovada. `N/A` fundamentado é resultado válido.

### 5.6. Subetapa 3.5 — Mensageria, eventos e notificações (`MSG`)

**Gerar quando necessário:** natureza (`evento interno | notificação ao usuário | mensagem de integração`), origem, destinatário/assinante, canal, payload mínimo, consentimento/permissão, prioridade, prazo, repetição, deduplicação, falha, confidencialidade e vínculo a casos/estados. Mensageria **não equivale somente a broker**: e-mail, push, aviso na tela ou mensagem local podem satisfazer a necessidade.

**Métricas:**

- `P3MSG-01` = mensagens/eventos aplicáveis com produtor, destinatário, gatilho e canal definidos **/ mensagens aplicáveis** (100%).
- `P3MSG-02` = mensagens críticas com conteúdo/payload, privacidade, entrega/erro e duplicidade tratados **/ mensagens críticas** (100%).
- `P3MSG-03` = comunicações ao usuário com preferência/consentimento e retorno de estado pertinentes **/ comunicações sujeitas a essas regras** (100%).

**Retrabalho:** percurso "acontecimento → mensagem → destinatário → confirmação/falha"; distinguir evento técnico de conteúdo visível; não inventar mensageria desnecessária. **Bloqueia:** notificação confidencial sem regras de destinatário/acesso.

### 5.7. Subetapa 3.6 — Telas, interações e estados (`VIEW`)

**Gerar quando necessário:** ator, casos, objetivo, campos, ações, navegação, estado vazio/carga/erro/sucesso/sem acesso, feedback, responsividade, acessibilidade e correspondência a `AC`. Telas compartilhadas por vários domínios recebem **dono de composição** sem duplicar sua definição canônica; casos headless podem ser `N/A`.

**Métricas:**

- `P3VIEW-01` = casos interativos cobertos por tela/entrada equivalente **ou ausência justificada / casos interativos** (100%).
- `P3VIEW-02` = telas com estados essenciais, ações e resultados claros **/ telas pertinentes** (100%).
- `P3VIEW-03` = jornadas críticas com requisitos de acessibilidade e permissão aplicáveis **/ jornadas críticas** (100%).

**Retrabalho:** simular usuário com permissão negada, conexão falha, dados vazios, teclado/leitor de tela; perguntar "que sinal a interface mostra para cada estado?". **Bloqueia:** jornada essencial sem resultado perceptível ou ação indevidamente disponível.

### 5.8. Agregação da Etapa 3

Ao fim das seis subetapas **de cada domínio**:

1. Emitir `Mapa_de_Artefatos.md` com relações `UC ↔ DATA/API/JOB/MSG/VIEW` e vínculos às features.
2. Emitir avaliação de cada tipo **mesmo quando `N/A`** (registrar motivo, não nota fictícia). Avaliar **cada item crítico** e declarar a amostragem de itens não críticos.
3. Verificar consistência cruzada: não existe `VIEW` apontando para UC inexistente, `MSG` sem destinatário, `JOB` sem gatilho, entidade órfã ou serviço sem caso/obrigação transversal justificável.
4. Produzir diagrama de domínio e diagramas técnicos necessários; comparar com Markdown.
5. Submeter `G3.DOM` com o menor IQE aplicável e todas as pendências; **uma subetapa reprovada não é compensada pela média das outras**.

---

## 6. Etapa 4 — Composição dos núcleos por domínio

### 6.1. Fundamento

Núcleos são **composições lógicas**, não obrigatoriamente serviços físicos, pacotes ou processos isolados. Um núcleo herda especificações; não as copia integralmente. Criar um `NUC` **somente quando há capacidade correspondente** e referenciar os artefatos componentes pela versão aprovada.

### 6.2. Núcleo de back-end

**Composição preferida:** `UC + DATA + API` (incluindo processamento local).  
**Pergunta:** "quem executa a regra, sobre qual estado e com qual contrato?"  
**Métricas:** `P4BACK-01` = ações do núcleo com entrada/processamento/saída verificáveis **/ ações** (100%); `P4BACK-02` = contratos e dados compartilhados sem proprietários contraditórios **/ vínculos críticos** (100%).  
**Retrabalho:** percorrer caminho síncrono, negar permissões, injetar dados inválidos e conferir invariantes. Se não houver entidade própria, referenciar o estado/dado necessário ou justificar.

### 6.3. Núcleo de rotina

**Composição preferida:** `UC + DATA + JOB`.  
**Pergunta:** "qual objetivo o processo automático realiza e como recupera falhas?"  
**Métricas:** `P4ROT-01` = rotinas com acionamento, estado, término e resultado observável **/ rotinas** (100%); `P4ROT-02` = cenários de repetição/falha relevantes tratados **/ cenários relevantes** (100%).  
**Retrabalho:** simular tempo, duplicação, falha parcial e concorrência; reduzir infraestrutura quando não necessária.

### 6.4. Núcleo de notificação

**Composição preferida:** `UC + DATA + MSG`.  
**Pergunta:** "que fato gera a comunicação, quem pode recebê-la e qual confirmação/erro importa?"  
**Métricas:** `P4NOT-01` = mensagens com fato gerador, destinatário e estado de entrega previstos **/ mensagens** (100%); `P4NOT-02` = condições críticas de permissão/privacidade/duplicação verificáveis **/ condições críticas** (100%).  
**Retrabalho:** traçar origem/destino, checar autorização e mensagens repetidas, distinguir evento de interface.

### 6.5. Núcleo de interatividade

**Composição:** `VIEW + UC + (NUC de back-end e/ou rotina e/ou notificação, conforme fluxo)`. Se a interação for inteiramente local e simples, pode usar `VIEW + UC + executor local documentado`, sem criar núcleos artificiais.  
**Pergunta:** "o usuário consegue provocar uma ação, observar seus efeitos e recuperar-se de uma falha?"  
**Métricas:** `P4INT-01` = ações de UI com `UC` e capacidade executora/efeito explícito **/ ações de UI** (100%); `P4INT-02` = estados de feedback (síncrono/assíncrono) ligados ao resultado real **/ estados relevantes** (100%); `P4INT-03` = jornadas do núcleo com permissão e acessibilidade previstas **/ jornadas pertinentes** (100%).  
**Retrabalho:** traçar da ação até o retorno à interface, incluindo notificação posterior; se houver falha de contrato, voltar ao artefato de origem.

### 6.6. Gate de núcleos

Para cada `NUC-...`: registrar **componentes e versões**, contrato/resultados, dependências intra/interdomínio, AC, riscos, métricas, `DIAG`, revisão e **G4.NUC**. O `G4.DOM` compara **todos os núcleos aplicáveis** e as capacidades não alocadas. Nem todo domínio deve produzir os quatro tipos; `N/A` justificado é obrigatório para categorias dispensadas. **Bloqueia:** capacidade essencial sem núcleo/execução, dependência circular não resolvida ou interação sem feedback adequado.

---

## 7. Etapa 5 — Fluxos completos de interatividade

**Objetivo:** conectar os núcleos de interatividade e capacidades associadas em **jornadas ponta a ponta**, inclusive fluxos que cruzam domínios, e transformar especificações isoladas em experiências demonstráveis.

**Para cada `FLOW-...`:** usuário/ator, objetivo, domínios e `NUC` envolvidos, tela inicial/final, sequência de eventos, entradas/saídas, regras, estados, etapas assíncronas, mensagens visíveis, exceções, permissões, política de recuperação, observabilidade, `UC/AC` e dependências.

**Procedimento:** (1) enumerar fluxos críticos do conjunto de features; (2) desenhar percurso UI→núcleo(s)→dado→resultado→feedback; (3) incorporar workers/mensageria quando necessários; (4) simular sucesso, erro, atraso, acesso negado, cancelamento e repetição pertinentes; (5) verificar o contrato **na fronteira entre domínios**; (6) avaliar **cada fluxo** e produzir sequência Mermaid/diagrama; (7) obter `G5.FLOW` e depois **G5** para o conjunto priorizado.

**Métricas:**

- `P5-01` = jornadas essenciais com `FLOW` completo **/ jornadas essenciais do SET** (100%).
- `P5-02` = fluxos com todos os saltos entre núcleos/domínios resolvidos e `AC` **/ fluxos aplicáveis** (100%).
- `P5-03` = exceções críticas com recuperação/feedback definidos **/ exceções críticas** (100%).
- `P5-04` = efeitos visíveis (telas/mensagens) ligados a estado ou evento real **/ efeitos visíveis** (100%).

**Retrabalho mental:** "filme do usuário" (cada segundo/estado), "contrafactual" (se worker não rodar?), "fio quebrado" (qual passo não tem executor?). **Bloqueia:** fluxo essencial sem resposta demonstrável ou contrato entre núcleos indefinido.

---

## 8. Etapa 6 — Arquitetura técnica, riscos e governança

**Entrada:** especificação e fluxos aprovados. Selecionar stack, limites de módulos, persistência, integrações, segurança, privacidade, autenticação, deploy (se aplicável), testes, recuperação, observabilidade e acesso de agentes. Considerar solução local/offline e modular monolith antes de introduzir infraestrutura, sem preferência obrigatória.

**Artefatos:** `06_Arquitetura.md`, `Governanca.md`, `decisoes/ADR-...`, matriz riscos/controles, plano de verificação, diagramas de componentes e fronteiras. `ADR` é exigido para stack e decisões com impacto relevante em contratos/dados/segurança.

**Métricas:** `P6-01` = componentes justificados por fluxo/requisito **/ componentes adotados** (100%); `P6-02` = decisões estruturais com `ADR` **/ decisões estruturais** (100%); `P6-03` = riscos Altos/Críticos com mitigação, responsável, teste e retorno planejados **/ riscos Altos/Críticos** (100%); `P6-04` = contradições Críticas/Altas abertas entre etapas 1–6 (meta **0**).

**Retrabalho:** questionar cada componente ("qual requisito o exige?"), simular indisponibilidade, vazamento, migração e rollback; corrigir fonte/ADR e propagar ao código futuro; revisar privilégios de agentes. **G6:** humano técnico aprova arquitetura, riscos, plano de testes e recuperação. Não permite publicação por si só.

---

## 9. Etapa 7 — Roadmap, tickets e implementação assistida por IA

### 9.1. Preparação e roadmap

Criar incrementos **verticais**, cada um contendo fluxo mínimo utilizável e seu conjunto de interface/serviço/dados/rotina/mensagem **pertinente**, critérios, testes e dependências; manter código em `src/`, separado de `planejamento/`. Preparar Git, branch por ticket, permissões, ambiente controlado, automações CI quando disponíveis e `AGENTS.md` sem segredos.

**Métricas do plano:** `P7-01` = incrementos com `FLOW`, `AC`, dependências e revisores **/ incrementos planejados** (100%); `P7-02` = tickets prioritários rastreáveis a especificação e AC **/ tickets prioritários** (100%); `P7-03` = controles críticos de CI com defeito controlado detectado **/ controles críticos instalados alegados** (100% quando aplicável).

### 9.2. Ciclo obrigatório por ticket

1. Criar `TKT` com origem, escopo, files/módulos permitidos, `AC`, risco, custo/limite de tentativas e critérios de parada.
2. IA implementadora propõe plano antes de editar. IA verificadora define matriz `AC → TEST → EV` independentemente.
3. Implementar em branch; versionar commits. Nunca alegar branch, teste ou PR inexistente.
4. Rodar lint/build/testes aplicáveis, testes de contratos/segurança segundo risco; registrar ambiente, comando, resultado e limitações.
5. IA revisora independente confronta diff, especificação, `ADR`, efeitos colaterais e regressões. Defeitos geram retrabalho restrito e nova verificação.
6. Humano aprova merge segundo Tier; atualizar relação com docs/diagramas e histórico. `G7.TKT` e `G7.INC` não equivalem a autorização de publicação.

**Métricas de execução:** `P7-04` = `AC` do ticket com evidência de teste/inspeção adequada **/ AC do ticket** (100% ou bloqueio explicitado); `P7-05` = desvios arquiteturais/funcionais **não aprovados** abertos (0); `P7-06` = tickets mesclados com revisão independente e aprovação exigida **/ tickets mesclados** (100%).

---

## 10. Etapa 8 — Verificação integrada e decisão de entrega

**Entrada:** incremento implementado, merge e evidências por ticket.

**Procedimento:** revisar matriz `FEAT → DOM → UC/AC → NUC → FLOW → TEST/EV`; executar e registrar verificações proporcionais (funcional, integração, E2E/UI, autorização, contratos, segurança, performance, falhas e recuperação), investigar testes incapazes de acusar defeito e registrar limitações. Separar **critério não testado** de **critério reprovado**; nenhuma dessas situações vira "aprovado" por analogia.

**Métricas:** `P8-01` = `AC` críticos com evidência válida **/ AC críticos aplicáveis** (100%); `P8-02` = `FLOW` críticos demonstrados ponta a ponta **/ FLOW críticos** (100%); `P8-03` = achados Críticos/Altos abertos (0); `P8-04` = testes de regressão ligados a defeitos anteriores **/ defeitos aplicáveis** (100%).

**Saídas:** `08_Relatorio_Validacao.md`, limitações e riscos residuais, evidências e `DIAG`. **G8:** aprovação humana explícita de **release definido/artefato testado**; aprovação de planejamento ou CI verde não autoriza publicar.

---

## 11. Etapa 9 — Publicação, observação e evolução

Publicar **o mesmo artefato validado**, com tag `REL`, procedimento de retorno compatível com ambiente, observabilidade proporcional (inclusive aplicativo offline: logs locais/feedback), indicadores de valor, incidentes, tempo de resposta e falhas de jornada; não transmitir dados reais/confidenciais a agentes sem sanitização/permissão.

**Métricas:** `P9-01` = releases com identificação, versão validada e retorno viável **/ releases realizadas** (100%); `P9-02` = sinais/incidentes relevantes com evidência, decisão e responsável **/ sinais/incidentes relevantes registrados** (100%); `P9-03` = mudanças de comportamento com `CHG` e reavaliação da etapa de origem **/ mudanças comportamentais executadas** (100%).

**G9:** autoriza a prontidão operacional mínima/primeiro ciclo; operação e aprendizado seguem continuamente. Feedback pode reabrir **G1A** se o modelo de produto se revelar inadequado, **G1B** se a feature estiver errada, **G2** se a responsabilidade for incorreta, ou gates locais de artefato/núcleo/fluxo. Nada é corrigido silenciosamente.

---
## 12. Sistema universal de avaliação de qualidade e maturidade

### 12.1. Hierarquia de avaliação (sem médias mascaradoras)

A unidade **mais específica** é sempre avaliada antes do agregado:

`item crítico → arquivo/tipo de artefato por DOM → núcleo por DOM → fluxo → domínio → etapa → release`.

Na Etapa 1, avaliar **cada `MOD`/`SET`** antes do consolidado. Na Etapa 2, avaliar **cada `DOM`** e a matriz completa. Na Etapa 3, avaliar **cada tipo UC/DATA/API/JOB/MSG/VIEW de cada `DOM`**. Na Etapa 4, cada `NUC`; na Etapa 5, cada `FLOW`. Avaliar etapas 6–9 por componente/incremento/critério/sinal conforme definido acima.

**Não fazer média para aprovar**: a nota da etapa é informativa e pode ter mediana/média descritiva, mas a autorização depende de **todos os itens obrigatórios e críticos aprovados individualmente**, do **menor IQE aplicável**, do **número de pendências bloqueantes** e da decisão humana. Itens não críticos legitimamente adiados devem ficar `Fora do incremento`, com justificativa e risco, **não** são contados como aprovados. Não misturar maturidade de planejamento com evidência de execução.

### 12.2. Cinco dimensões transversais

Cada unidade aplicável recebe nota **0–4** em cinco dimensões, com justificativa e fonte:

| Dimensão | Peso | Pergunta objetiva |
|---|---:|---|
| `C` — Completude aplicável | 25% | requisitos mínimos, exceções e decisões pertinentes foram descritos? |
| `K` — Coerência e correção | 25% | a unidade não contradiz seus predecessores nem suas invariantes? |
| `R` — Rastreabilidade | 20% | há origem, responsáveis, consumidores e IDs válidos? |
| `E` — Evidência/verificabilidade | 20% | fatos têm fonte e hipóteses estão rotuladas; resultados podem ser demonstrados? |
| `G` — Governança/visual | 10% | estado, versão, avaliação/revisão, diagrama e aprovações estão corretos? |

**Nota:** `0` ausente; `1` fragmentário; `2` estruturado com lacunas; `3` completo no escopo e verificável, pronto para crítica independente; `4` revisado independentemente com prova/documentação suficiente. Não atribuir 4 com base apenas na autodeclaração de quem gerou. Uma hipótese classificada, com plano, pode pontuar bem em honestidade e rastreabilidade **sem ser tratada como validada**.

**Cálculo único:**  
`IQE = 25×C/4 + 25×K/4 + 20×R/4 + 20×E/4 + 10×G/4` (0–100; comparar limiares com valor **não arredondado**).

### 12.3. Maturidade do conteúdo versus autorização

| Faixa de IQE | Nível candidato | Interpretação |
|---|---|---|
| `0 ≤ IQE < 20` | **M0 — Inexistente** | não há conteúdo suficiente |
| `20 ≤ IQE < 40` | **M1 — Inicial** | ideias/fragmentos |
| `40 ≤ IQE < 60` | **M2 — Estruturado** | artefato reconhecível, lacunas relevantes |
| `60 ≤ IQE < 80` | **M3 — Verificável** | conteúdo analisável, ainda insuficiente para aprovação |
| `80 ≤ IQE < 90` | **M4 — Controlado** | candidato a gate, **exige aprovação humana** |
| `90 ≤ IQE ≤ 100` | **M5 — Maduro/rastreável** | candidato a melhoria contínua, evidências independentes e gate aprovado |

**Travas obrigatórias:** sem aprovação humana **teto M3**; sem versão canônica ou com achado **Crítico/Alto aberto teto M2**; sem revisão independente efetiva **não alcançar M5**. Assim, IQE 92 em um rascunho pode continuar **M3 efetivo**. `M4` e `M5` não significam software implementado; nas fases de planejamento significam planejamento aprovado/seguro para o próximo trabalho.

### 12.4. Critérios mínimos de gate e cobertura

**Para levar uma unidade de planejamento à decisão:** IQE `≥80`, **cada dimensão `≥3`**, indicadores obrigatórios da unidade cumpridos (`100%` dos aplicáveis para cobertura/segurança/propriedade), achados Críticos/Altos abertos `=0`, versão Markdown salva, revisão independente registrada, diagrama conferido ou dispensa formal, histórico atualizado e alternativas necessárias comparadas. **Para liberar a etapa** acrescer **aprovação humana com IDs/versões**.

O responsável pode classificar achado Médio como corrigir ou aceitar formalmente com risco/responsável; **Crítico/Alto bloqueia gate**. Exceção a meta numérica não pode aceitar lacuna que viole segurança/critério essencial. Revisar limiares por `ADR/CHG` de governança em projeto-piloto com evidências; **80 e pesos são convenções propostas, não ciência universal**.

**Indicadores transversais (universo e método anotados):**

| Código | Fórmula | Meta inicial |
|---|---|---|
| `CMP` | itens obrigatórios adequados ÷ itens obrigatórios aplicáveis | 100% |
| `TRC` | vínculos rastreáveis corretos ÷ vínculos necessários | 100% críticos; ≥95% demais |
| `VFC` | alegações críticas com fonte ou hipótese+plano ÷ alegações críticas | 100% |
| `COH` | contagem de contradições Críticas/Altas abertas | 0 |
| `VIS` | diagramas requeridos fiéis/legíveis/versionados ÷ diagramas aplicáveis | 100% ou dispensa humana |
| `RET` | achados reabertos após verificação ÷ achados declarados corrigidos | medir tendência; não inventar baseline |
| `EST` | itens alterados fora do impacto autorizado ÷ itens alterados | 0% |

**Atenção aos denominadores:** se nada for aplicável, registrar `N/A` + fundamento; jamais computar `0/0` como 100%. `100%` de campos preenchidos não implica que a decisão seja boa — sempre complementar com análise qualitativa/adversarial. Itens críticos exigem inspeção integral; amostragem de itens comuns deve ser descrita e não rotulada como cobertura completa.

### 12.5. Scorecard do conjunto e critérios de desempate

A avaliação de um conjunto `SET` ou opção `MOD` pode usar as cinco dimensões comuns mais fatores **de escolha**, sem misturar escores:

- **Adequação ao valor**, **cobertura e não objetivos**, **complexidade relativa**, **riscos**, **manutenibilidade**, **dependências** e **evidências das analogias** são comparados **lado a lado**.
- Registrar a distinção entre **"qualidade do documento da proposta"** (IQE) e **"conveniência da alternativa"** (decisão humana). Uma alternativa pode ser bem especificada (alto IQE) e não ser escolhida.
- Se duas alternativas atenderem requisitos com qualidade semelhante, priorizar **menor complexidade capaz de entregar o valor**, respeitadas decisões de produto e riscos.

### 12.6. Quadro consolidado obrigatório

O `planejamento/Avaliacoes/Painel.md` apresenta, por unidade/gate: ID, tipo, DOM (quando houver), versão, IQE, maturidade candidata/efetiva, indicadores específicos (N/D), bloqueios, diagrama, revisão, decisão humana e data. **Expor o menor IQE e o número de unidades pendentes**, não apenas uma média atraente.

---

## 13. Procedimento normativo de retrabalho e reavaliação

### 13.1. Gatilhos

Um ciclo de retrabalho abre quando: `IQE < 80`, qualquer dimensão `<3`, indicador obrigatório insuficiente, crítica/contradição, vínculo órfão, problema descoberto em domínio/núcleo/fluxo, feedback, mudança de ideia/escopo, diagrama divergente ou regresso em teste/operação. **Correção de texto sem mudança material também é registrada**, proporcionalmente, e pode ter fluxo simplificado Tier 0.

### 13.2. Ciclo de dez operações

1. **Congelar referência:** anotar arquivo, versão, commit, decisão e gate vigente.
2. **Delimitar achado:** indicar falha observável, severidade, quem detectou e evidência.
3. **Rastrear origem:** retornar `FLOW/NUC → UC/DATA/API/JOB/MSG/VIEW → DOM → FEAT → MOD/IDEA` até a primeira premissa incorreta.
4. **Medir antes:** guardar indicadores (numerador/denominador), notas, IQE, situação do gate.
5. **Analisar causa raiz:** diferenciar ausência, ambiguidade, contradição, inferência falsa, mudança de intenção e defeito de execução.
6. **Propor delta mínimo:** escrever **antes → depois**, hipótese de correção, o que não deve mudar e alternativas quando a mudança for material.
7. **Classificar risco e autorizar:** abrir `CHG` se mudar especificação/entendimento aprovado; `ADR` para decisão estrutural; `TKT` para execução. Aprovação humana **antes** de alterar comportamento relevante.
8. **Corrigir fonte e propagar:** atualizar primeiro o Markdown **causal**; depois vínculos, núcleos, fluxos, diagramas, tickets, testes, runbooks afetados. Para cada dependente marcar `ALTERAR / INSPECIONAR / SEM IMPACTO` + justificativa.
9. **Contraprova e reavaliação:** pedir revisão independente, repetir métricas, reproduzir defeito anterior e testar regressões adjacentes.
10. **Decidir e arquivar:** registrar `HST`, alteração/versões/evidências, reaprovar gate **impactado** quando necessário; preservar histórico e próxima ação.

**Parada operacional proposta:** após **três tentativas sem resolver a causa**, suspender repetição automática, rever hipótese e escalar a decisão ao responsável; o limite pode ser ajustado em ticket. Sem fonte ou ferramenta para comprovar, registrar `Não verificado`, jamais declarar sucesso.

### 13.3. Achados, prioridade e risco

| Severidade do achado | Exemplo | Consequência |
|---|---|---|
| **Crítico** | exposição de dado sensível, requisito de segurança essencial invertido | gate bloqueado; humana/técnica imediata |
| **Alto** | feature crítica sem comportamento, domínio sem dono, fluxo sem executor | gate bloqueado |
| **Médio** | omissão de estado secundário, ambiguidade controlável | corrigir ou aceitar formalmente o risco se elegível |
| **Baixo** | apresentação/legibilidade sem efeito semântico | programar correção com histórico |

**Tier de execução é conceito distinto**: `Tier 0` (editorial/documental sem comportamento); `Tier 1` (funcional sem contratos/dados críticos); `Tier 2` (dados/migrações, segredos, autenticação, pagamentos, infraestrutura, contratos externos, arquitetura protegida). Tier 2 requer salvaguardas reforçadas, revisão independente efetiva, rollback planejado/testado quando cabível e aprovação humana técnica. **Se a organização buscar aderência estrita ao AICD externo, aplicar também os requisitos de aprovações/segregação correspondentes, sem presumir certificação por esta adaptação.**

### 13.4. Modelos mentais obrigatórios como opções diagnósticas

| Código | Modelo mental | Pergunta de correção e contexto |
|---|---|---|
| `MM1` | **Causa antes do sintoma** | primeiro erro foi na feature, no domínio ou apenas na tela? |
| `MM2` | **Fato × hipótese × decisão** | algo suposto virou requisito sem aprovação? |
| `MM3` | **Caminho feliz e contrário** | quais exceções/negações derrubam o fluxo? |
| `MM4` | **Invariantes** | o que deve continuar verdadeiro em qualquer estado? |
| `MM5` | **Menor raio de impacto** | que consumidores precisam alterar/ser inspecionados? |
| `MM6` | **Revisor adversarial** | qual é o menor contraexemplo capaz de refutar esta proposta? |
| `MM7` | **Contrafactual antes/depois** | como demonstrar a correção, e o que não pode regredir? |
| `MM8` | **Reversibilidade e proporcionalidade** | podemos escolher alteração menor e reversível? |
| `MM9` | **Propriedade única** | qual domínio é dono da regra/dado? |
| `MM10` | **Experiência observável** | que tela/mensagem/status prova o efeito ao usuário? |

O revisor escolhe e documenta **ao menos um modelo mental pertinente**, não apenas cita a sigla. Em falha sistêmica, combinar modelos. Ajustes que alcancem domínios diferentes geram **matriz de propagação**, não duplicação arbitrária de fonte canônica.

### 13.5. Reabertura seletiva

- Mudou **modelo de produto ou público/valor** → reavaliar **G1A/G1B**, impactos em G2–G9.
- Mudou **conjunto de features** → reabrir **G1B** e partes impactadas do mapa DOM/artefatos/núcleos/fluxos.
- Mudou **dono/fronteira de domínio** → reabrir **G2** (parte), `G3.DOM.*`, `G4.DOM` e fluxos relacionados.
- Mudou **UC/DATA/API/JOB/MSG/VIEW** → reabrir **G3.DOM.TIPO**, núcleos/fluxos consumidores e testes; sem reaprovar todo o projeto se escopo base não mudou.
- Mudou **núcleo** → reavaliar **G4.NUC** e fluxos dependentes.
- Mudou **fluxo** → reavaliar **G5.FLOW**, impacto em arquitetura, tickets e testes.
- Mudou **implementação sem alterar especificação** → abrir `TKT` e validar correção/regressão, sem `CHG` desnecessário.
- Mudou **diagrama sem mudar semântica canônica** → corrigir `DIAG` e `HST`, sem falsificar reaprovação de requisito.

Reaprovação **nunca é retroativa**: versão anterior permanece no histórico e a nova é marcada `Proposta` até decisão humana.

---

## 14. Camada Visual de Decisão: diagramas por etapa

### 14.1. Regra de produção

Produzir síntese visual **após gerar e revisar conteúdo da unidade**, **antes de solicitar o gate**; gerar/atualizar figura consolidada **depois da aprovação** quando as opções não escolhidas devam ser removidas. Nas etapas de concepção, mostrar modelos e conjuntos **como alternativas não aprovadas** até decisão. O diagrama não substitui arquivo Markdown, matriz de AC ou teste.

### 14.2. Catálogo mínimo

| Etapa | Diagrama necessário | Conteúdo/legenda indispensáveis |
|---|---|---|
| **1A** | comparação de modelos de produto | `MOD/REF`, aderência, limites, riscos, estado `PROPOSTO`, modelo livre |
| **1B** | matriz/árvore de conjuntos de features | `SET/FEAT`, escopo agora/depois/fora, diferenças e decisão |
| **2** | mapa de domínios | `DOM`, dono da capacidade, dependências, `FEAT × DOM` |
| **3.1/DOM** | mapa de casos | `UC`, ator, `FEAT`, `AC` e exceções principais |
| **3.2/DOM** | ERD/diagrama de estados | `DATA`, dono, identificadores, cardinalidades, transições |
| **3.3/DOM** | fluxo de serviço/contrato | `API` local/remoto, request/response, permissão, erros |
| **3.4/DOM** | fluxo de rotina | `JOB`, gatilho, retry, estados e resultado |
| **3.5/DOM** | fluxo de eventos/mensagens | `MSG`, produtores, canais, destinatários, falhas |
| **3.6/DOM** | mapa de telas/navegação | `VIEW`, `UC`, estados, acessibilidade e permissões |
| **4/DOM** | mapa de composição dos núcleos | `NUC` back-end/rotina/notificação/interatividade e seus IDs constituintes |
| **5** | sequência/atividade ponta a ponta | `FLOW`, núcleos, domínios, decisões, sucesso/erro e retorno visível |
| **6** | arquitetura de componentes | módulos, limites, dados, integrações, ADR, riscos e controles |
| **7** | roadmap de incrementos | `INC/TKT/AC`, dependências, gates e status **real** |
| **8** | painel de validação | AC testados/sem prova, evidências, riscos e autorização |
| **9** | ciclo operacional | `REL`, indicadores observados, incidentes, retorno, `CHG/TKT` |

**Dispensa:** permitida quando tipo não aplicável ou valor da figura for nulo, com **justificativa e aprovação humana**; não usar figura falsa para satisfazer requisito. Para domínio headless, mapa de telas pode ser dispensado e o fato registrado. Opcionalmente, diagrama geral e um específico por tipo podem ser **combinados**, se a leitura e precisão não forem prejudicadas.

### 14.3. Ficha de diagrama e validação

Cada `DIAG-###` deve ter `.md` com ID, título, estágio, domínio, estado, fonte textual e versão/commit, IDs representados, legenda, objetivo da decisão, descrição acessível, simplificações, autor/revisor e resultado da verificação semântica. Preferir `Mermaid`/`SVG` como fonte editável e `PNG` para leitura; se o renderizador não estiver disponível, manter fonte Mermaid/diagrama textual marcado **Não renderizado**, sem afirmar que imagem existe.

Verificação obrigatória: IDs existentes, relações/direção das setas, contagens, status **proposta ≠ aprovada**, acessibilidade/contraste, ausência de nomes inventados, números legíveis e relação com documento/versão. Se divergirem, **prevalece o Markdown aprovado**, e o visual deve ser corrigido.

---

## 15. Organização em Markdown, versionamento e publicação documental

### 15.1. Estrutura de diretórios sugerida

```text
NomeDoProjeto/
├── planejamento/
│   ├── README.md                         # índice canônico, projeto, versão e próxima decisão
│   ├── 01_Concepcao/
│   │   ├── Ideia_e_Contexto.md
│   │   ├── Modelos_de_Produto.md
│   │   ├── Referencias_de_Mercado.md
│   │   ├── Conjuntos_de_Features.md
│   │   ├── Features_Aprovadas.md
│   │   └── Decisao_Concepcao.md
│   ├── 02_Dominios/
│   │   ├── Mapa_de_Dominios.md
│   │   ├── Matriz_Features_Dominios.md
│   │   └── DOM-001_Nome/
│   │       └── Identidade.md
│   ├── 03_Artefatos/
│   │   └── DOM-001_Nome/
│   │       ├── 01_Casos_de_Uso.md
│   │       ├── 02_Entidades_e_Estados.md
│   │       ├── 03_Servicos_e_APIs.md
│   │       ├── 04_Workers.md
│   │       ├── 05_Mensageria.md
│   │       ├── 06_Telas.md
│   │       └── Mapa_de_Artefatos.md
│   ├── 04_Nucleos/
│   │   └── DOM-001_Nome/
│   │       ├── Backend.md
│   │       ├── Rotina.md
│   │       ├── Notificacao.md
│   │       └── Interatividade.md
│   ├── 05_Fluxos/
│   │   └── FLOW-001_Nome.md
│   ├── 06_Arquitetura/
│   │   ├── Arquitetura.md
│   │   ├── Governanca.md
│   │   └── decisoes/ADR-001_Nome.md
│   ├── 07_Execucao/
│   │   ├── Roadmap.md
│   │   └── tickets/TKT-001_Nome.md
│   ├── 08_Validacao/
│   │   └── Relatorio_Validacao.md
│   ├── 09_Operacao/
│   │   └── Operacao_e_Evolucao.md
│   ├── Avaliacoes/
│   │   ├── Painel.md
│   │   └── DOM-001/AV-G3-DOM001-UC.md
│   ├── Historico/
│   │   └── Historico_por_Etapa.md
│   ├── Alteracoes.md                   # CHG — decisões materiais
│   ├── diagramas/
│   │   ├── DIAG-001.md                  # metadados + descrição acessível
│   │   ├── DIAG-001.mmd                 # fonte editável
│   │   └── DIAG-001.png                 # se renderizado/verificado
│   └── evidencias/                     # apenas dados seguros ou links CI
├── src/                                 # código, estrutura idiomática à stack
├── tests/                               # testes, estrutura idiomática à stack
├── infra/                               # se necessário
├── AGENTS.md
├── README.md
└── .gitignore
```

Pastas/arquivos para recursos `N/A` **não precisam ser materializados como arquivos vazios**: no `Mapa_de_Artefatos.md`, registrar formalmente a dispensa. Em projetos pequenos, consolidar Markdown por contexto desde que IDs, avaliações e gates **continuem separáveis**.

### 15.2. Fonte canônica e Drive/GitHub

1. Eleger um repositório **primário** (recomendado Git); Drive pode ser espelho, pasta de referência ou plataforma de colaboração com sincronização/revisão. Registrar a **fonte canônica única** no `planejamento/README.md`.
2. Registrar versão e estado dos arquivos Markdown; ao aprovar, identificar usuário decisor, data/hora e commit/revisão. Não aceitar aprovação apenas em conversa sem persistir no arquivo/histórico.
3. Toda alteração material de documento aprovado abre `CHG`, impact analysis e revisão; tarefas de execução abrem `TKT`; um ticket referencia `CHG` quando aplicável. Fazer PR e não alterar `main` diretamente quando há Git.
4. Preservar decisões substituídas e versões relevantes (Git + `HST`); não duplicar manualmente o mesmo histórico em repositórios concorrentes.
5. Não commitar tokens, segredos, PII real, logs confidenciais ou bancos de produção. Não compartilhar cópias públicas sem inspeção.

### 15.3. Documento de entrada/saída e aceite

Todo artefato relevante possui: objetivo/escopo; entradas aprovadas e respectivos IDs; conteúdo e decisões; hipóteses/lacunas; relacionamentos; critérios/indicadores N/D; avaliação IQE; relatório de achados; diagrama/ficha; gate e decisão. Não escrever "Aprovado" enquanto `aprovado_por`/`aprovado_em` forem nulos.

---

## 16. Modelo de histórico por etapa, domínio e subetapa

### 16.1. Diferenciar registro e decisão

`HST-####` registra **avaliação, retrabalho, correção, reabertura, dispensa, decisão e reavaliação**, com origem em **etapa/subetapa/domínio/artefato**. `CHG` conserva a decisão de mudar especificação aprovada; `ADR` arquitetura; `TKT` execução; `DIAG` imagem; Git/PR é trilha técnica. Nenhum substitui o outro.

### 16.2. Ficha mínima de `HST`

```md
#### HST-0001 — [título]
- Data/hora, autor e revisor: [ISO-8601 / identificadores]
- Etapa/subetapa de origem: [ex.: 3.5]
- Domínio/unidade: [DOM-002 / MSG-003 ou não aplicável]
- Etapas, domínios e unidades impactados: [IDs]
- Natureza/estado: [Avaliação | Correção | Retrabalho | Reabertura | Reaprovação | Dispensa]
- Fonte anterior: [arquivo, versão, commit, gate]
- Achado: [descrição + severidade + evidência]
- Causa e modelo mental: [MM usado + diagnóstico e hipótese refutável]
- Antes → depois: [diferença precisa]
- Impacto: [Alterar / Inspecionar / Sem impacto, por unidade]
- Métricas anteriores → novas: [indicador N/D; IQE; maturidade; bloqueios]
- CHG / ADR / TKT / DIAG / testes / PR: [IDs ou N/A]
- Regressões e evidências: [o que foi realmente verificado]
- Decisão humana e estado do gate: [identidade/data/evidência ou Pendente]
- Risco residual, próximo responsável e ação: [informar]
```

### 16.3. Índice e organização

Um índice transversal de HST contém `HST`, data, etapa, domínio, unidade, tipo, severidade, estado, gate e link. A ficha detalhada aparece **uma única vez**, **na etapa/subetapa causal**, e referencia outras etapas sem duplicação. Na Etapa 3, indexar separadamente `DOM-001/UC`, `DOM-001/DATA`, etc.; na Etapa 4, por núcleo; na Etapa 5, por fluxo. Alterações rejeitadas permanecem no histórico. Nunca gerar evento fictício para preencher formulário.

### 16.4. Métricas históricas úteis

- **Reabertura** = gates reabertos ÷ gates anteriormente aprovados no período (segmentar etapa/domínio; nunca atribuir causalidade sem análise).
- **Correção efetiva** = achados resolvidos sem reabertura no período de observação ÷ achados verificados.
- **Propagação imprevista** = unidades afetadas não previstas ÷ unidades afetadas de fato.
- **Dívida de evidência** = contagem de alegações críticas sem fonte ou plano válido.
- **Retrabalho por origem** = ocorrências por etapa e subetapa causal, para priorizar melhoria de processo.

Essas métricas exigem histórico real; iniciar como `Não medido`, não com números inventados.

---

## 17. Instruções de execução para agentes de IA

Ao receber **"Continue o planejamento conforme a normativa v2.0"**, a IA deve:

1. Ler `planejamento/README.md`/índice, identificar **próximo gate pendente**, últimas versões aprovadas, HST/CHG abertos e artefatos dependentes. Se o projeto não existe, iniciar **Etapa 1A** registrando a ideia.
2. Declarar **o nível de decisão em que está trabalhando**, ex.: `E3 / DOM-003 / MSG` ou `E4 / DOM-002 / NUC-007`, evitando saltos e mistura de domínios.
3. Carregar **somente o contexto relacionado** (modelo+SET+FEAT+DOM+UC e consumidores necessários), sem inventar requisitos de contexto ausente.
4. Na **Etapa 1A**, pesquisar produtos/categorias conhecidos quando a ferramenta estiver disponível; declarar fontes e data. Sempre apresentar caminho **livre/original**.
5. Na **Etapa 1B**, oferecer **dois ou mais conjuntos materialmente distintos** de features, comparar e aguardar escolha humana antes de consolidar.
6. Na **Etapa 2**, mapear domínios por capacidade/feature, conferir ownership e obter aprovação antes de detalhar todos os artefatos.
7. Nas **Etapas 3–5**, trabalhar por **domínio e unidade**, elaborar ficha de indicadores próprios e IQE; diante de falha, corrigir e reavaliar a unidade, não apenas apresentar uma nota geral.
8. Criar/atualizar fonte Mermaid/diagrama de cada gate, com versão e descrição textual; se não puder renderizar, dizer `Não renderizado`.
9. Gerar `HST` por evento **realmente ocorrido**, preservar `CHG/ADR/TKT` onde cabível, e reportar mudança antes/depois e impacto.
10. Em risco alto, parar para decisão humana. Não declarar aprovação, teste, PR ou deploy sem evidência observável.
11. Encerrar a interação com **estado auditável**, próximo gate, arquivos escritos, evidências reais, problemas e decisão exigida — **não** prosseguir automaticamente para próxima etapa sem aprovação quando ela for obrigatória.

### 17.1. Formato padrão da resposta por unidade

```md
## Contexto: Etapa [N] / Domínio [DOM] / Unidade [ID e tipo]
### Entradas canônicas (versões/IDs e premissas)
### Opções propostas e comparativo (quando aplicável)
### Especificação proposta (arquivo Markdown)
### Indicadores específicos (N/D) + IQE + maturidade candidata/efetiva
### Achados, modelo mental e plano de retrabalho (se necessário)
### DIAG: fonte, versão, descrição e estado de renderização
### Histórico CHG/HST/TKT/ADR (se aplicável)
### Decisão humana solicitada (gate, IDs, versões)
### Próximo passo condicionado à aprovação
```

### 17.2. Critérios de pronto por nível

- **Artefato por domínio pronto:** completo/sem bloqueios, score e avaliação guardados, vínculos e visual coerentes, `G3.DOM.TIPO` aprovado.
- **Domínio pronto para núcleos:** artefatos aplicáveis aprovados ou `N/A` documentado; cruzamento coerente; `G3.DOM` aprovado.
- **Núcleo pronto:** integrantes aprovados, contratos e AC, visual, avaliações e `G4.NUC` aprovado.
- **Fluxo pronto:** percurso de ponta a ponta, estados/erros/feedback, AC demonstráveis e `G5.FLOW` aprovado.
- **Incremento implementado pronto:** código/revisão/testes versionados de acordo com risco e `G7.INC` aprovado.
- **Entrega autorizada:** `G8` humano, evidência suficiente, riscos residuais/retorno registrados.

---

## 18. Adoção e compatibilidade com v1.3/v1.4

### 18.1. O que foi preservado

Persistem: problema/público e foco em valor, especificação textual como fonte de verdade, aprovação humana, IDs imutáveis, Git/tickets/ADRs/CHGs/DIAGs, separação implementação-verificação, risco proporcional, verificabilidade por `AC`, diagramas fiéis, propagação seletiva e realimentação operacional. Preserva-se o método de **IQE/M0–M5** proposto na v1.4 como **sistema transversal**, sem afirmar que tenha sido executado.

### 18.2. O que mudou estruturalmente

- O processo parte formalmente de **comparação com modelos de produto existentes ou modelo livre**, não apenas da declaração de problema.
- A **concepção** incorpora **seleção separada** de modelo e **mínimo dois conjuntos** de features.
- A aprovação de **domínios** passa a preceder artefatos detalhados.
- Casos de uso, entidades, serviços, workers, mensageria e telas passam a ser **modelados e medidos por domínio**, com gates granulares.
- São introduzidos **núcleos back-end, rotina, notificação e interatividade**, compostos de artefatos; a interatividade e os fluxos de ponta a ponta têm verificação própria.
- A aprovação de etapa **não é média**: o menor componente crítico reprovado impede passagem.
- Histórico `HST` passa a aceitar **etapa + subetapa + domínio + tipo + núcleo/fluxo**, permitindo retrabalho preciso.
- As antigas numerações **0–10** não devem ser copiadas sem remapeamento: esta é uma nova estrutura **1–9**, com correspondência semântica, não numérica.

### 18.3. Correspondência orientativa com documentos anteriores

| Organização anterior v1.3/v1.4 | Nova localização v2.0 |
|---|---|
| Etapa 0 Problemas/público + Etapa 1 Visão | **1A/1B** Concepção (inclui modelo de produto e features) |
| Etapa 2 Casos de uso | **3.1** por domínio |
| Etapa 3 Interfaces | **3.6** por domínio; **4.5/5** composição/interatividade |
| Etapa 4 Serviços | **3.3** por domínio e **4.2** núcleo back-end |
| Etapa 5 Dados | **3.2** por domínio e núcleos correspondentes |
| Rotinas/eventos distribuídos no fluxo anterior | **3.4–3.5**, núcleos 4.3–4.4 |
| Etapa 6 Arquitetura | **6** |
| Etapas 7–8 Roadmap/implementação | **7** |
| Etapa 9 Validação | **8** |
| Etapa 10 Operação | **9** |

**Migração:** não renumerar IDs históricos; exportar/citar documentos aprovados antigos, mapear os vínculos para a nova estrutura em `Migracao_v1x_para_v2.md` e **reavaliar novas relações/domínios/núcleos**. Gates antigos não implicam aprovação automática dos novos. Decisões materiais passam por `CHG` e aprovação humana; preservar v1.x íntegra como referência.

### 18.4. Ativação recomendada

1. Aprovar ou solicitar ajustes à v2.0, registrando responsável, data e versão.
2. Escolher projeto-piloto e fonte canônica (Git/Drive espelho).
3. Executar **Etapa 1A** e **G1A**; depois **Etapa 1B/G1B**, sem saltar direto para código.
4. Testar G2 e G3 com **um domínio piloto** antes de escalar aos demais.
5. Calibrar métricas com HST reais, sem suavizar bloqueios essenciais.

---

## 19. Anexos e modelos de trabalho

Este documento integra-se ao kit Markdown disponibilizado junto da normativa:

- `modelos/01_Ideia_e_Modelos.md` — ideia, referências de mercado e comparação de opções.
- `modelos/02_Conjuntos_de_Features.md` — dois ou mais conjuntos com comparativo e decisão.
- `modelos/03_Identidade_e_Mapa_Dominios.md` — mapa de domínios e matriz FEAT × DOM.
- `modelos/04_Artefatos_por_Dominio.md` — seis subetapas e `N/A` documentado.
- `modelos/05_Nucleos.md` — composição de núcleos.
- `modelos/06_Fluxo_de_Interatividade.md` — fluxo ponta a ponta.
- `modelos/07_Avaliacao_Granular.md` — scorecard e ficha de achados por unidade.
- `modelos/08_Historico_por_Etapa.md` — HST global organizado por etapa/domínio.
- `modelos/09_Mudanca_CHG.md` — mudança aprovada e matriz de impacto.
- `modelos/10_DIAG_Ficha.md` — proveniência e checklist visual.
- `modelos/11_ADR.md` — decisão de arquitetura.
- `modelos/12_Ticket_e_Aceite.md` — `TKT`, AC/Teste/Evidência.
- `modelos/13_Painel_e_Gates.md` — visão executiva de avaliação.
- `modelos/14_Runbook_Operacao.md` — publicação/feedback/rollback.
- `diagramas/*.mmd` — fontes Mermaid de **processo** e **composição conceitual**; não representam um produto implementado.
- `exemplo/Exemplo_Ficticio_Educacional.md` — exemplo **hipotético** explicitamente não aprovado.

---

## 20. Referências e atribuição

**Fontes diretas para a reorganização:** a descrição do fluxo desejado pelo responsável nesta conversa; `Normativa de Desenvolvimento de Aplicações com IA v1.3` (22/10/2026); `Normativa de Desenvolvimento de Aplicações com IA v1.4 — Proposta` e seus anexos de avaliação/retrabalho e histórico (23/10/2026). Essa v2.0 é **uma proposta nova**, não uma cópia com simples renumeração.

**Inspiração metodológica atribuída nas versões anteriores:** Alim Sahane (Rachid Alim Ngatcha Sahane), *AICD: Artificial Intelligence Centered Development*, versão 0.3, setembro de 2026, conforme referência das normativas anteriores. Os núcleos funcionais, as subetapas por domínio e os limiares IQE são **adaptações próprias desta normativa**, não exigências atribuídas ao AICD original.

**Estado final:** **não aprovada; nenhum gate de projeto executado; métricas ainda não aplicadas a software real por este documento.**
