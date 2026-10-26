# Implantação

## Uso local

O perfil de desenvolvimento abre `http://localhost:5080`. O acervo é pessoal e compartilhado por todas as requisições da instância. Não existe login.

Para publicar localmente, use `dotnet publish`, uma pasta de dados persistente fora da publicação e binding em loopback. Não apague a pasta de dados ao substituir os binários.

## Docker opcional

```bash
docker compose up --build -d
```

Abra `http://localhost:5080`. O Compose expõe somente o endereço loopback e usa volume persistente `leitor-dados`. Não execute `docker compose down -v` se quiser preservar o acervo. Exportar backup pela aplicação continua recomendado.

O Dockerfile usa imagens oficiais .NET 8. Em produção, atualize as imagens para correções de segurança e fixe digest conforme sua política de distribuição. O usuário `app` é não privilegiado; a pasta de dados recebe sua propriedade durante o build. Para bind mounts em vez de volume nomeado, ajuste as permissões do diretório no host.

## Acesso por domínio

- Terminar HTTPS no proxy reverso e configurar `AllowedHosts` com o domínio.
- Manter processo interno na rede privada/loopback e adicionar autenticação no proxy antes de qualquer acesso remoto.
- Ajustar limites de corpo e timeout do proxy para importação/restauração.
- Uma instância apenas: o lock de arquivo desta implementação é por processo, não distribuído.
- Monitorar erros, espaço em disco, tempo de extração e memória do processo.
- Preservar chaves de Data Protection se precisar manter cookies válidos entre reinícios; prévias em memória sempre expiram ao reiniciar.
- A extração é síncrona no processo depois do upload. Arquivos complexos podem consumir CPU; não é um serviço público de conversão.

Não foram realizados build da imagem, execução dos containers ou testes do proxy no ambiente de autoria.
