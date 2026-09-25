# As cenas em paralelo — o workflow

Cada slide passa por **autor → revisor adversarial** (pipeline: o revisor do slide 2 começa quando o
autor do slide 2 termina, sem esperar os outros), e o deck inteiro por **uma passada de consistência**
no fim. O revisor pegou, na primeira vez, sobreposições, legendas que sumiam antes de serem lidas,
contraste baixo e fatos trocados que o autor não viu — não pule ele.

Regras de concorrência: cada agente escreve **só o seu arquivo de slide**; nenhum toca `deck.json`
nem o repositório do projeto. Renders são serializados pela trava do `render.py`, então vários agentes
podem chamá-lo ao mesmo tempo.

## Com a ferramenta Workflow

Preencha `ROOT` e `SLIDES` (todos menos a capa, que você escreveu), e rode:

```js
export const meta = {
  name: 'animated-deck-scenes',
  description: 'Author each animated slide, review it adversarially, then a deck-wide consistency pass',
  phases: [{ title: 'Author' }, { title: 'Review' }, { title: 'Consistency' }],
}
const ROOT = '<ROOT absoluto>'
const SKILL = '<caminho absoluto desta skill>'
const SLIDES = [ /* { id: 'jornada', n: '03' }, … na ordem do deck.json, sem a capa */ ]

const COMMON = `
You work on ONE slide of an animated deck. ROOT = ${ROOT} (a scratch folder). Touch only your slide's file.
Read first, whole: ROOT/DESIGN.md (words, palette by role, type, templates, facts, and your slide's brief in §7),
${SKILL}/references/runtime.md, ${SKILL}/references/motion-kit.md, and the exemplar slide named in DESIGN.md.
Tools: python3 ROOT/tools/check_slide.py <file> (must end "RESULT PASS"); python3 ROOT/tools/render.py <file> <t…|poster>
(renders the slide with its scene frozen at scene time t into ROOT/renders/; READ every PNG you make).
Facts only from DESIGN.md §6. Language and the word table from DESIGN.md §1.`

const authorPrompt = (s) => `${COMMON}
YOUR SLIDE: "${s.id}" (${s.n}), file ROOT/project/slides/${s.id}.html (write it). Brief: DESIGN.md §7 entry ${s.n}.
Make the scene motion design that carries meaning (motion-kit.md § A régua de criatividade): things travel, snap, fill,
stamp, type, scan; one focal point at a time; calm easing. Play once and rest on F = END; the resting frame explains the
slide alone. Pace: every text visible ≥ the reading rule in motion-kit.md § Ritmo before the next beat.
Process: plan the stage regions and beat times → write → check → render ~6 times across 0…END plus poster and READ them →
fix overlaps, clipped or tiny text, low contrast, a beat that reads too fast, anything off-palette → repeat (≤ 6 rounds).
Return JSON: id, title, END (ms), summary (2 sentences), check (last RESULT line).`

const reviewPrompt = (s, a) => `${COMMON}
YOUR SLIDE: "${s.id}" (${s.n}), just written by another agent: ${JSON.stringify(a || {}).slice(0, 2000)}
You are the adversarial reviewer: assume problems remain; FIX them in the file. Render ≥ 8 times across 0…END plus poster
and READ each. Check: legibility in every frame (no overlaps, nothing clipped, ≥ 24 units, contrast); reading pace measured
by rendering just before and after each beat; the story reads without narration; facts and words match DESIGN.md exactly
(future things labelled); palette roles; STAGE template and eyebrow number; play-once tail, F = END, export hook; if the
scene is a static diagram with fades, raise it to motion that carries meaning.
Return JSON: id, verdict (ok | fixed | needs-human), fixes[], remaining[], END (ms), check.`

const deckPrompt = (r) => `${COMMON}
Scope now: the WHOLE deck in deck.json order; you may edit any slide file (not deck.json). Reports: ${JSON.stringify(r).slice(0, 6000)}
Run python3 ROOT/tools/contact_sheet.py and READ the sheets in order, as the audience flips through. Align with small edits:
the same thing drawn the same way on every slide (the question, the answer, the main actor, a data box, refusal), one palette,
eyebrows numbered in order, titles in one grammar, identical STAGE markup. Every slide passes check_slide.py.
Return JSON: titles[{id, eyebrow, title, END}], fixes[], concerns[], allPass.`

const A = { type: 'object', properties: { id: { type: 'string' }, title: { type: 'string' }, END: { type: 'number' }, summary: { type: 'string' }, check: { type: 'string' } }, required: ['id', 'summary', 'check'] }
const RV = { type: 'object', properties: { id: { type: 'string' }, verdict: { type: 'string', enum: ['ok', 'fixed', 'needs-human'] }, fixes: { type: 'array', items: { type: 'string' } }, remaining: { type: 'array', items: { type: 'string' } }, END: { type: 'number' }, check: { type: 'string' } }, required: ['id', 'verdict', 'fixes', 'remaining', 'check'] }
const DK = { type: 'object', properties: { titles: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, eyebrow: { type: 'string' }, title: { type: 'string' }, END: { type: 'number' } }, required: ['id', 'title'] } }, fixes: { type: 'array', items: { type: 'string' } }, concerns: { type: 'array', items: { type: 'string' } }, allPass: { type: 'boolean' } }, required: ['titles', 'fixes', 'concerns', 'allPass'] }

const done = await pipeline(SLIDES,
  (s) => agent(authorPrompt(s), { label: `author:${s.id}`, phase: 'Author', schema: A }),
  (a, s) => agent(reviewPrompt(s, a), { label: `review:${s.id}`, phase: 'Review', schema: RV }).then((r) => ({ a, r })))
const reports = SLIDES.map((s, i) => ({ id: s.id, verdict: done[i]?.r?.verdict, END: done[i]?.r?.END, remaining: done[i]?.r?.remaining }))
const missing = SLIDES.filter((s, i) => !done[i]?.r).map((s) => s.id)
if (missing.length) log(`No review result for: ${missing.join(', ')}`)
phase('Consistency')
const deck = await agent(deckPrompt(reports), { label: 'consistency', phase: 'Consistency', schema: DK })
return { reports, deck, missing }
```

O mesmo esqueleto serve para as rodadas de mudança (recolorir, mudar ritmo, trocar o estilo): troque o
prompt do autor por um de **conversão fiel** ("a história, os beats e os fatos estão aprovados; mude só
<X>") e mantenha o revisor e a consistência.

## Sem a ferramenta Workflow

Com a ferramenta de subagentes (`Agent`): para cada slide, lance o autor com o `authorPrompt` e, quando
ele voltar, o revisor com o `reviewPrompt`; no fim, um agente com o `deckPrompt`. Vários slides em paralelo
só se a máquina aguenta vários Chromes em fila (a trava serializa os renders, não o resto). Sem subagentes:
faça autor e revisor você mesmo, slide a slide, com os mesmos critérios.

## Depois

Leia `remaining` e `concerns`: o que é decisão do usuário (texto diferente do brief, duração longa,
trocas de título) vai para a entrega, uma linha cada. O resto você corrige antes de publicar.
