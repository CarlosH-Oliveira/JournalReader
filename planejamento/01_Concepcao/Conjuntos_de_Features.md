---
{
  "id": "SET-003",
  "etapa": 1,
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
  "avaliacao": "AV-E1",
  "diagrama": "DIAG-001",
  "gate": "Pendente de ratificação humana; avanço documental delegado",
  "aprovado_por": null,
  "aprovado_em": null,
  "commit_pr": null
}
---

# Alternativas de escopo

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
