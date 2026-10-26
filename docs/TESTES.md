# Roteiro de verificação pelo destinatário

Nenhum item desta lista foi executado em runtime .NET no ambiente de autoria. Marque os resultados obtidos e guarde versão do SDK, navegador e arquivos usados.

## Compilação

```bash
dotnet --info
dotnet restore LeitorDeJornal.sln
dotnet build LeitorDeJornal.sln -c Release
dotnet list src/LeitorDeJornal.Infrastructure package --vulnerable --include-transitive
dotnet run --project src/LeitorDeJornal.Web
```

A solução não inclui suíte automatizada .NET. Este roteiro cobre os fluxos que precisam de homologação; recomenda-se automatizá-los após a primeira execução e estabilização do corpus.

## Acervo e importação

1. Com pasta de dados vazia, abrir o acervo e verificar o estado inicial.
2. Importar `amostras/leitura-numerada.txt`; conferir título, texto integral e normalização dos finais de linha na prévia; cancelar. O acervo deve continuar vazio.
3. Repetir e confirmar. Reimportar o mesmo texto: deve abrir a obra existente, sem duplicar.
4. Alterar título na confirmação; verificar busca de título, filtro TXT e ordenações.
5. Importar TXT com acentos, emoji e caracteres combinantes; confirmar ausência de substituições por `�`.
6. Importar TXT em Windows-1252 sem BOM: deve recusar codificação inválida. Converter para UTF-8 e tentar novamente.
7. Tentar extensão não suportada, arquivo vazio e arquivo acima de 50 MiB. Verificar erro sem gravar obra.
8. Importar PDF conhecido de duas colunas: comparar prévia com páginas originais, verificar alertas, aceitar explicitamente. PDF somente imagem deve ser recusado; PDF misto deve alertar sobre páginas sem texto.
9. Importar PDF com senha: deve recusar se o parser não conseguir abrir; confirmar que não existe importação silenciosa sem texto.
10. Importar EPUB com capítulos/títulos, notas e imagens alt. Verificar ordem do spine, capítulos e avisos. Tentar criptografia e layout fixo padronizado: devem ser recusados.
11. Abrir duas sessões de navegador e tentar acessar token de prévia de outra sessão: deve falhar. Repetir após 15 minutos: a prévia deve expirar.

## Leitura e âncoras

1. Usar o corpus numerado. Ler colunas 1, 2, 3 e 4, depois avançar a folha. Não pode haver lacunas nem duplicações na passagem de coluna ou folha.
2. Conferir primeira/última folha e bloqueio de avançar/voltar nos extremos.
3. Marcar um trecho no meio de parágrafo, aumentar fonte de 18 para 24, alternar 4 → 1 → 4 colunas. O mesmo trecho deve continuar na folha visível.
4. Testar fontes mínima/máxima, palavra muito longa, linhas em branco consecutivas, emoji, títulos e zoom de 200%.
5. Em tela estreita, verificar folha horizontal com quatro colunas e modo acessível refluível sem rolagem horizontal. Usar navegação por teclado.
6. Buscar `coração`, frase entre parágrafos e termo ausente. Verificar offsets corretos, máximo de 100 resultados e navegação ao trecho. Busca ignora caixa, mas não remove acentos.
7. Esperar “Salvo no acervo”, fechar e reabrir a obra. Confirmar âncora, tema, fonte e modo.
8. Abrir a mesma obra em duas abas, gravar na primeira e depois na segunda. A segunda deve mostrar conflito, sem sobrescrever. Recarregar explicitamente.
9. Desligar o servidor durante um salvamento: não deve mostrar sucesso falso; repetir após restabelecer a conexão. Encerramento abrupto antes do commit pode perder a última posição.

## Notas e destaques

1. Selecionar trechos com acentos e emoji; criar destaque, nota e marcador de posição.
2. Selecionar texto que atravesse parágrafos/colunas; conferir o intervalo salvo.
3. Mudar fonte/tema/modo e reabrir: o intervalo deve continuar apontando ao texto original.
4. Editar nota e cor pelo painel; ir ao trecho; remover marcação.
5. Simular falha de gravação: o rascunho da nota deve permanecer no diálogo e permitir repetição.
6. Excluir uma obra com marcações pelo diálogo: texto, índice derivado e anotações devem desaparecer do acervo; arquivo original deve permanecer.

## Backup e persistência

1. Exportar backup com pelo menos duas obras, preferências, posições e notas.
2. Em pasta isolada, restaurar confirmando substituição. Comparar todos os dados com a origem.
3. Alterar um caractere do payload sem atualizar o hash: deve recusar sem alterar o acervo ativo.
4. Testar JSON inválido, schema desconhecido, IDs duplicados, offsets fora do texto e nota acima de 10.000 caracteres; deve recusar.
5. Retirar permissão de escrita ou simular disco cheio: nenhuma operação pode anunciar sucesso; catálogo anterior deve continuar legível.
6. Reiniciar durante escrita transitória: catálogo deve ser íntegro; documentar o comportamento do filesystem de destino. Não assumir garantia em falha de energia.
7. Testar recuperação manual com `.previous`, com servidor parado, conforme README.

## Acessibilidade e conteúdo ativo

1. Tab/Shift+Tab, foco visível, Escape, foco contido nos diálogos e retorno ao acionador.
2. Leitor de tela: ordem única do texto e nomes dos controles. Validar navegação entre folhas com tecnologia assistiva.
3. Título/nota/EPUB contendo `<script>` ou handlers: devem aparecer como texto ou ser removidos; nunca executar.
4. EPUB com links externos, recursos remotos ou XXE no package: não pode buscar recursos de rede.
5. POST sem antiforgery token deve retornar erro; GET não pode excluir, confirmar ou restaurar dados.
