---
name: animated-deck
description: >
  Use para criar um deck de slides animado que explica algo a uma plateia: arquitetura,
  produto, fluxo, pitch, onboarding, resultado de projeto. Cada slide ganha uma cena de motion
  design (SVG/canvas que se move) nas cores da marca do próprio projeto, tocando uma vez no
  ritmo de leitura; o escopo fecha numa sessão de grilling e o deck sai também em MP4.
  Triggers: "deck animado", "slides animados", "apresentação com animação", "monta um deck
  pra apresentar", "exporta o deck pra mp4", /animated-deck
---

# Deck animado

Cada slide carrega **uma ideia** no texto e uma **cena** viva que a mostra. O padrão de qualidade
saiu de quatro pedidos de um usuário; a skill já começa onde eles terminaram:

| O pedido que foi preciso fazer | Vira padrão aqui |
|---|---|
| "seja criativo — animações, gráficos em SVG que se mexem" | toda cena é motion design que carrega significado, não diagrama com fade |
| "use as cores da marca" | paleta lida dos tokens do projeto, um acento, fundo da marca |
| "toca uma vez, sem loop" + "mais devagar pra dar tempo de ler" | a cena toca uma vez e repousa no **pôster**; ritmo de leitura |
| "exporta pra mp4" | gravação quadro a quadro pronta, oferecida no fim |

**Pasta de trabalho** (`ROOT`): uma pasta no scratchpad (`<scratchpad>/<slug>-deck/`), nunca dentro
do repositório do projeto. Tudo abaixo — `DESIGN.md`, `project/`, `tools/`, `renders/`, `video/` — vive nela.

## Fase 0 — Escopo (grilling)

Invoque a skill `grilling` (a mesma sessão do `/grill-me`) sobre a árvore de perguntas de
[`references/grill.md`](references/grill.md). Sem `grilling` instalada, siga as regras dela: uma
pergunta por vez, cada uma com a sua resposta recomendada; o que dá para descobrir (tokens de cor,
fontes, fatos no código, logo, landing) você descobre em vez de perguntar; as decisões são do usuário.

**Pronto quando:** `ROOT/DESIGN.md` §1–§3 e o roteiro de títulos (§7 só com títulos) estão escritos
([`references/design-template.md`](references/design-template.md)) e o usuário confirmou que fechou.

## Fase 1 — Ferramentas

Copie `scripts/` desta skill para `ROOT/tools/` e escreva `ROOT/deck.config.json` a partir de
`scripts/deck.config.example.json` (fundo da marca, cores proibidas, fontes). Pré-requisitos: Chrome,
`python3` com Pillow, `node`; para MP4 também `ffmpeg` e `puppeteer`/`puppeteer-core` (o de um
`node_modules` do projeto serve — aponte em `"puppeteer"`).

**Pronto quando:** `python3 tools/render.py` roda numa página de teste e `node --version`,
`ffmpeg -version` respondem (ou o MP4 foi descartado na Fase 0).

## Fase 2 — Fatos, sistema visual, briefs

Leia [`references/runtime.md`](references/runtime.md) e [`references/motion-kit.md`](references/motion-kit.md)
**agora** — são as regras que quebram se você as ignorar. Então complete o `DESIGN.md`:

- **§6 Fatos:** todo número e afirmação com fonte (`arquivo:linha`, doc, métrica) lida nesta sessão.
  O que é futuro vai marcado para receber o rótulo de proposta no slide.
- **§2 Paleta por papel**, dos tokens reais do projeto (tema CSS, Tailwind, landing, favicon): fundo,
  card, borda, tinta, texto secundário, **um** acento, cor de recusa. Mesma cor = mesmo papel em
  todas as cenas.
- **§7 Brief por slide:** título, lede, e a cena descrita em *beats* (o que entra, o que se move,
  onde repousa).

**Pronto quando:** cada slide do roteiro tem brief com beats, e todo número dos briefs está em §6.

## Fase 3 — Capa exemplar

Você mesmo escreve a capa: é o **exemplar** que todos os outros copiam (kit de movimento, pintura
do fundo, gancho de exportação, estilo do texto). Com a ferramenta Artifact: `quickstart` de slides →
crie o deck pelo `type_url` → escreva `project/deck.json` completo (ordem de todos os slides) e a capa
→ `check_slide.py` + `render.py` → publique os dois. Sem Artifact: mesmo layout de arquivos; a entrega
é `tools/standalone.py` (HTML) e o MP4.

**Pronto quando:** a capa passa na checagem, você leu o render dela, e ela está publicada.

## Fase 4 — Cenas em paralelo

Um autor por slide → um revisor adversarial do mesmo slide → uma passada de consistência no deck
inteiro. Script e prompts em [`references/workflow.md`](references/workflow.md).

**Pronto quando:** todos os slides dão `RESULT PASS`, todo revisor voltou `ok`/`fixed`, e a
consistência voltou `allPass`.

## Fase 5 — Sua leitura, publicação, entrega

`python3 tools/contact_sheet.py` → leia as folhas **em ordem**, como a plateia. Corrija o que
destoa, publique, e entregue: link, duração de cada cena, o que ficou para o usuário decidir
(lista curta, uma linha cada). Ofereça o MP4 em uma linha se ele não foi pedido.

**Pronto quando:** o deck publicado é o que você leu nas folhas, e as decisões pendentes estão na resposta.

## Fase 6 — MP4 (e HTML standalone)

[`references/video.md`](references/video.md).

## Depois da entrega

Os ajustes que sempre chegam — "mais devagar/mais rápido", "cores erradas", "tá em loop", "esse
objeto parece girar ao contrário" — têm receita em [`references/motion-kit.md`](references/motion-kit.md)
§ Ajustes. Mexa só no slide citado; regrave o MP4 depois.
