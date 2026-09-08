---
description: "Seis skills independentes para tarefas comuns de entrega de software e documentação."
metaDescription: "Workflows oferece skills independentes para worktrees Git, commits, pull requests, revisões, documentação para desenvolvedores e artefatos HTML autocontidos."
summary: "Workflows transforma tarefas recorrentes de engenharia em procedimentos portáteis, com limites claros, conclusão baseada em evidências e sem exigir um framework no projeto."
highlights:
  - "Worktrees Git"
  - "Commits e pull requests"
  - "Revisões somente leitura"
  - "Documentação para desenvolvedores"
  - "Artefatos HTML"
  - "Skills independentes"
---

## Produto

Agentes de engenharia precisam com frequência preparar worktrees, organizar commits, redigir pull requests, revisar mudanças, manter documentação e explicar sistemas visualmente. Workflows reúne essas tarefas em seis skills focadas, que podem ser instaladas e usadas de forma independente.

Cada skill define as evidências necessárias para concluir sua tarefa e preserva as escolhas existentes no repositório. Prefixos de branches definidos pelo host, instruções do usuário, templates de pull request e estruturas de documentação continuam sendo a referência.

## O que construí

Construí fluxos independentes para planejar worktrees e verificar seu ciclo de vida, criar commits coesos, redigir pull requests fiéis às mudanças, fazer revisões baseadas em evidências, manter documentação para desenvolvedores e produzir artefatos HTML portáteis.

O fluxo de revisão permanece somente leitura, a menos que uma correção também seja solicitada. Commits e publicações continuam sendo ações explícitas, e todas as skills funcionam sem Harness; uma integração opcional e restrita pode acrescentar contexto de continuidade quando Harness já estiver instalado.

## Decisões de engenharia

Cada skill orienta o agente a usar as ferramentas de Git, arquivos e revisão já disponíveis. O pacote contém instruções, sem runtime próprio ou scripts executáveis incluídos. Essas instruções definem o resultado, as decisões relevantes e as evidências de conclusão, mantendo o julgamento técnico com o agente e o usuário.

Por padrão, os fluxos de escrita preservam arquivos e layouts existentes. As revisões exigem evidências concretas, as afirmações da documentação são conferidas com o código-fonte e os relatórios HTML incorporam seus recursos essenciais para abrir diretamente do disco.
