---
name: skill-eval-guidelines
description: >
  Use sempre que a tarefa for criar, fazer, melhorar, revisar ou discutir o eval
  de uma skill de agente, ou decidir se uma skill merece ser instalada, mantida
  ou publicada. Vale também para escrever uma skill a partir de falhas do agente,
  desmontar a skill de outra pessoa, ou responder se uma skill funciona de verdade.
  Traz as regras de objetivo, pontos centrais, medição, braços de controle e
  decisão. Triggers: "essa skill funciona", "avalia essa skill", "faz o eval da
  skill", "vale instalar essa skill", "a skill melhora o agente", /skill-eval-guidelines
---

# Skill eval guidelines

A skill avaliada é a que o usuário indicou; sem indicação, a do diretório atual. A
folha abaixo é a referência. Para o eval de um sistema de IA inteiro, e não de uma
skill, use `eval-guidelines`.

Para escrever uma skill, comece pelas falhas repetidas do agente sem ela e só
depois escreva o texto. Para avaliar uma que já existe, extraia os pontos centrais
antes de medir qualquer coisa: é deles que saem as checagens de [A], e sem nenhum
ponto a seção 2 já encerra a avaliação.

Skill de terceiros é código de um estranho. Leia antes de instalar ou rodar, e rode
o eval isolado do que é real.

Eval custa dinheiro: combine o teto com o usuário antes de rodar e confirme que
braços × tarefas × execuções cabe nele. Se não couber, corte tarefas ou braços e diga
o que deixou de medir.

Termine com a decisão da seção 5 por ponto, os dois placares lado a lado e as
respostas às 4 perguntas do fim da folha. O que não foi medido fica marcado como
faltando, em vez de estimado.

```
Skill evals cheat sheet: does that skill make my agent better?
[A] adherence: did the agent do what the skill says     [E] effect: did doing it help

1. Why bother  (what the evidence says about skills today)
├─ A skill = text in the context; nothing in the model changes
├─ Installed ≠ used: the model opens a skill about half the time; 81 of 89 never invoked on one machine
├─ More skills, worse pick: right choice 29.6% with 5 skills → 3.3% with 100
├─ Published ≠ tested: 39 of 49 public skills gave zero gain; tokens up to +451%
├─ Doesn't transfer: same skill +33 points on one model, −22 on another
└─ 1 in 4 marketplace skills has a vulnerability pattern: treat it as code from a stranger

2. Write it (or take someone else's apart)  (ideas first, text last)
├─ Objective: one sentence, measurable. Unmeasurable = unstudied
├─ Core points: "do X, because it makes Y better"; no hypothesis = folklore
├─ Best source of points: the repeated failures of the agent with no skill (beats doctrine)
├─ Text: every sentence comes from a point; examples in the agent's own language
└─ Someone else's skill: extract its points first; none found → don't install

3. Measure  (two scores, read as a pair)
├─ [A] One code check per point over the harness log (files written, commands, exit codes)
├─ [A] Loaded-or-not flag: an unloaded skill scores zero; keep that visible
├─ [E] Hidden checks the agent never saw (e.g. hidden tests)
├─ [E] Quality, not quantity: label each output critical / useful / nitpick / useless / harmful
│      (anchored to runs against the old code + planted faults, then a judge checked against hand labels)
├─ [E] Honesty (claimed done vs hidden checks), cost (tokens, turns, $), stability (several runs)
└─ Ablation: remove one point, re-run; if the effect doesn't drop, the point goes

4. Run the evals  (your tasks, your context, your model)
├─ A few dozen real tasks with hidden ground truth; name the skill in the task so it loads
├─ Arms: no skill · the skill · an alternative procedure · unrelated text of the same length
├─ The length control is the arm people skip; irrelevant text alone cost ~3 points
└─ 2-3 runs per task per arm; budget = arms × tasks × runs, with a money ceiling set first

5. Decide
├─ [A] low → the wording is at fault: rewrite the text, keep the idea
├─ [A] high, [E] flat → the idea is at fault for this model: drop the point
├─ [A] high, [E] up → keep it, with the extra cost written next to the gain
└─ Beats no-skill but loses to the length control → there are no usable ideas in it

6. Ship and keep alive
├─ Ship 4 things: text + points + evals + results (with model and version)
├─ Re-run after every model or library change: one skill drifted 95% → 65% in a month
└─ A skill is accepted per model and per date; the acceptance expires

Someone says a skill "works"? Ask: which model, which version, what baseline, what length control.
```
