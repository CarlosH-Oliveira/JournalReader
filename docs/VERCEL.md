# Implantação na Vercel

A raiz usa `framework: container` em `vercel.json` e `Dockerfile.vercel`. A imagem compila .NET 8 e executa o ASP.NET Core na porta 80. Um serviço Node.js acessível somente em `127.0.0.1:8081` adapta o SDK oficial `@vercel/blob` para a aplicação C#.

## Armazenamento privado

O Blob `journalreader-blob` fica na região IAD1 e está conectado aos ambientes Preview e Production. A Vercel fornece `BLOB_STORE_ID` e a credencial OIDC em cada requisição. O código encaminha essa credencial apenas pela ponte interna; nenhuma chave permanente é enviada ao navegador ou incluída no repositório.

- `state/catalog.json`: acervo com escrita condicional por ETag. Atualizações concorrentes são rejeitadas com orientação para recarregar, evitando sobrescrita silenciosa.
- `drafts/{owner}/{token}.json`: prévias compartilhadas entre instâncias; expiram logicamente após 15 minutos e são removidas na confirmação, no cancelamento ou na consulta depois da expiração.
- `keys/`: chaves Data Protection para cookies e antifalsificação entre reinícios.
- `uploads/{owner}/{id}.{ext}`: arquivos de entrada privados. Removidos após a tentativa de extração. Um upload abandonado antes da extração pode permanecer e requer limpeza periódica.

O proprietário de uma importação é identificado por cookie HttpOnly protegido, não por sessão em memória. O acervo continua pessoal e compartilhado; isso não implementa contas de usuários. Manter Deployment Protection da Vercel ativada.

## Upload de arquivos grandes

1. O navegador pede autorização em `POST /Import/PrepareBlob`, com antifalsificação e metadados.
2. O servidor valida extensão e tamanho até 50 MiB e gera uma URL de PUT válida por 15 minutos, limitada a um caminho e tamanho; não permite sobrescrever.
3. O navegador envia o arquivo diretamente ao Blob privado, exibindo progresso. O corpo não atravessa a Vercel Function e seu limite de 4,5 MB.
4. Um pequeno formulário em `POST /Import/FromBlob` identifica o arquivo. O servidor verifica o vínculo ao cookie, lê o Blob internamente, valida/extrai o conteúdo e oferece a prévia.

A proteção antifalsificação permanece ativa em ambas as rotas. O aplicativo nunca busca uma URL arbitrária fornecida pelo usuário; usa somente caminhos internos validados. A ponte exige segredo aleatório por processo e não abre porta pública.

## Operação

- O host aceita localhost e `*.vercel.app`. Adicionar domínios personalizados a `AllowedHosts` quando necessário.
- Fora da imagem Vercel, a execução .NET local mantém os adaptadores de arquivo JSON e prévia em memória, sem depender de Node.js.
- O catálogo inteiro é um único objeto JSON, adequado ao uso pessoal. Acervos muito grandes exigem particionamento ou banco de dados; considerar operações e transferência do Blob nas cotas do plano.
- O fluxo de restauração de backups ainda utiliza POST tradicional e, na Vercel, está sujeito a 4,5 MB. Não foi ampliado por esta correção de importação.
- O build reporta NU1902 no AngleSharp 1.1.2. A atualização do extrator EPUB deve ser validada separadamente.

## Validação

Verificar build .NET e Node, importação real acima de 4,5 MB, prévia, confirmação e leitor. Confirmar disponibilidade do mesmo acervo em outro deployment para comprovar persistência fora do contêiner. Não confundir HTTP 200 da página inicial com validação do fluxo de importação.

### Evidência de 26/10/2026

O EPUB fornecido (13.594.113 bytes) atravessou o fluxo de upload direto e gerou prévia com 2.459.219 caracteres. Após confirmação, o leitor abriu em quatro colunas, com 1.090 folhas na viewport do teste. O mesmo livro foi aberto em outro deployment e o comando de posição retornou “Salvo no acervo”. A retomada após recarregar também foi verificada. A quantidade de folhas depende de fonte, viewport e modo acessível.
