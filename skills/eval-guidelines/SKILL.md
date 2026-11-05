---
name: eval-guidelines
description: >
  Use sempre que a tarefa for criar, fazer, melhorar, revisar ou discutir o eval
  de um sistema de IA: harness, agente custom, app com LLM, RAG, prompt. Vale
  também para escolher grader ou judge, montar golden set, ou responder se o
  agente funciona de verdade ou se uma mudança ajudou. Traz as regras de casos,
  graders, validação do grader, números honestos e rotina. Triggers: "cria um
  eval", "faz o eval desse agente", "melhora o eval", "evals do harness", "como
  sei se o agente funciona", /eval-guidelines
---

# Eval guidelines

O sistema avaliado é o que o usuário indicou; sem indicação, o harness ou agente
do projeto atual. A folha abaixo é a referência. Use as seções que o sistema
pede: a 5 só se ele tiver partes, a 6 só ao escolher modelo.

Para criar um eval, comece pela análise de erro da seção 1, porque é ela que diz
quais graders precisam existir, e escolha o grader mais barato que pega cada tipo
de falha. Para melhorar um eval que já existe, compare-o com a folha e ataque
primeiro o que distorce os números (sem test set separado, grader nunca conferido,
taxa sem barra de erro), antes de acrescentar casos ou graders.

Rótulo humano vem de humano: é a régua de todos os outros graders, então um rótulo
gerado por você não serve para validá-los. Quando faltar, peça ao usuário uma
amostra para rotular.

Termine reportando os 4 números do fim da folha, com quantos casos foram de fato
pontuados do total. O que ainda não der para calcular fica marcado como faltando, com
o que falta para obter, em vez de estimado.

```
Evals cheat sheet: how to know an AI system actually works

1. Inputs  (what you test on)
├─ Real cases, awkward ones included: start with 20-50 taken from real failures
├─ Gold answers: write down what "right" means for each case; this is the real asset
├─ Two piles: tune on the dev set, report only on the test set
└─ Error analysis first: read 100+ outputs, note each failure, group and count → that list is your grader plan

2. Graders  (who decides pass or fail)
├─ Code
│  ├─ [free] Exact match / F1: labels with one right answer
│  ├─ [free] Rule checks: format, length, required facts, banned phrases
│  └─ [free] Similarity (ROUGE, embeddings): a drift alarm, NOT a quality score
├─ Small models
│  ├─ [≈free] Hallucination detectors (HHEM, MiniCheck, LettuceDetect): "is this claim supported?"
│  └─ [¢] Typed judge (Jev): picks a label + gives a calibrated probability, writes no text
├─ LLM judge
│  ├─ [¢] One yes/no question per failure type + quote the evidence + give it the context
│  ├─ [¢¢¢] Panel of 3 judges, combined by median, not average
│  └─ Known biases: prefers first, longer, its own model family, and "pleasant" over "solved"
└─ Humans
   └─ [$$$] Ground-truth labels: the yardstick for every other grader

3. Check the grader  (the grader is part of the system)
├─ Compare with human labels → Cohen's kappa (0.6 to gate a release, 0.8 to run unsupervised)
├─ Report catch rate on bad outputs and false-fail rate on good ones; raw agreement misleads
└─ Record the judge model + version next to every result

4. Honest numbers
├─ An error bar on every rate: "70%, somewhere between 58 and 82"
├─ Paired comparison: both versions on the same cases + count the cases that got worse
├─ Detection floor: with 60 cases you can't see a change smaller than ~12 points
├─ Tried 20 prompt variants? Confirm the winner on fresh cases
└─ Check how many items actually got scored: when a judge call fails, most frameworks just drop it from the average and the number still looks fine

5. Systems with parts
├─ RAG: grade the finder (hit@k, recall@k) and the writer (faithfulness) separately
├─ Agents: final state + path, pass^k over several runs, rephrased tasks, cost per success
└─ Grader used for training or selection? It gets gamed; keep one the system never sees

6. Public benchmarks  (pick the engine, not the product)
├─ A score = model + prompt + harness + version
├─ Contamination and saturation: check the date
└─ ~5 benchmarks to shortlist 2-3 models → your own eval decides

7. Make it a habit
├─ Every commit: code graders  [free]
├─ Every prompt / model / retrieval change: judges + a human-read sample  [¢-$]
├─ After shipping: A/B test + graders on sampled live traffic
└─ Re-check the judge whenever the model, judge or domain changes

Ask for 4 numbers: pass rate with its error bar · grader vs human agreement ·
detection floor · share of cases that got worse in the last change
```
