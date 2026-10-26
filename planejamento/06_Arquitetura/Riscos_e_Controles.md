---
{
  "id": "RISK-MAPA",
  "etapa": 6,
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
  "avaliacao": "AV-E6",
  "diagrama": "DIAG-006",
  "gate": "Pendente de ratificação humana; avanço documental delegado",
  "aprovado_por": null,
  "aprovado_em": null,
  "commit_pr": null
}
---

# Matriz de riscos

| ID | Nível | Cenário | Papel responsável | Mitigação | Verificação planejada | Retorno |
| --- | --- | --- | --- | --- | --- | --- |
| RISK-001 | Alto | Parser/EPUB hostil acessa dados ou executa script | Responsável técnico de segurança (a designar) | Isolamento/allowlist, nenhum script remoto, normalização de caminho, proibir symlinks | TEST-010: entradas hostis, tráfego zero, tentativa de path traversal | Abandonar job, apagar staging e manter acervo anterior |
| RISK-002 | Alto | Extração PDF muda ordem/some texto | Responsável de ingestão (a designar) | Prévia obrigatória nos alertas; corpus gold; nunca garantir fidelidade universal | TEST-001/002: corpus PDF difícil e fonte lado a lado | Recusar arquivo e preservar original; reabrir ADR-002 |
| RISK-003 | Alto | Layout perde/repete texto ou âncora | Responsável de composição/leitura (a designar) | Texto único, mapeamento canônico e generation | TEST-003/004/007: contagem/ordem/Unicode/zoom | Voltar ao último perfil/mapa válido; modo acessível com aviso |
| RISK-004 | Alto | Excluir/restaurar destrói acervo errado | Responsável de persistência (a designar) | Confirmar impacto, tokens limitados, staging validado, troca de geração e rollback | TEST-008/009/011: falha em cada ponto e hash corrompido | Restaurar geração anterior íntegra; nunca apagar original externo |
| RISK-005 | Alto | Backup/documentos expõem conteúdo privado | Responsável técnico/produto (a designar) | Aviso de backup em claro, sem logs de conteúdo, sem rede, uso da proteção do SO | TEST-010/012: inspecionar saída de rede e logs com conteúdo sentinela | Interromper exportação/envio indevido e eliminar staging; usuário controla cópias externas |
| RISK-006 | Alto | Documento grande esgota memória/trava UI | Responsável técnico de desempenho (a designar) | Limites por etapa, um job pesado, cancelamento, virtualização de páginas | TEST-013: documento limite e bomba de descompressão | Cancelar job isolado e manter leitura/acervo responsivos |
| RISK-007 | Médio | Quatro colunas dificultam leitura em telas pequenas | Responsável de produto (a designar) | Folha virtual e modo acessível explícito; estudo de conforto | TEST-004/014: zoom/teclado/leitor de tela + estudo com usuários | Mudar modo sem perder âncora; reavaliar H-002 |
| RISK-008 | Médio | Dependência muda licença/API ou é vulnerável | Responsável técnico (a designar) | Auditar versões/licenças, SBOM e lockfile antes de implementar | TEST-015: inventário e atualização controlada | Fixar versão anterior segura ou trocar adaptador; sem distribuir dependência não aprovada |

Classificação qualitativa: Alto quando compromete conteúdo, privacidade ou fluxo central; Médio quando há recuperação ou afeta conveniência. Não há probabilidades inventadas. Seis riscos altos têm controles/testes/retorno; isso não os torna aceitos ou testados. Responsáveis são papéis; pessoas ainda não foram designadas. Falha em controle essencial impede implementação/distribuição até correção e aprovação técnica.
