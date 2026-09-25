# Construir o deck (o chat que recebeu o prompt)

Você recebeu um prompt-guia gerado pela skill `animated-deck` (plateia, mensagem, palavras, paleta,
fontes, fatos com fonte, roteiro e ideias de cena). O que ele traz decidido vale; o que vem como
orientação você decide, seguindo `motion-kit.md`. Construa num tiro só; pergunte só se algo bloquear.

`SKILL` = a pasta desta skill (a que contém este arquivo). **Pasta de trabalho** (`ROOT`): uma pasta no
scratchpad (`<scratchpad>/<slug>-deck/`), nunca dentro do repositório do projeto.

## Fase 1 — Ferramentas e contrato

1. Copie `SKILL/scripts/` para `ROOT/tools/`. Escreva `ROOT/deck.config.json` com o bloco `deck.config`
   do brief, e `ROOT/DESIGN.md` com a parte "Brief" do prompt (seções §1–§7), acrescentando no topo os caminhos de `SKILL/references/runtime.md` e `motion-kit.md` e o do slide exemplar (a capa).
2. Pré-requisitos: Chrome, `python3` com Pillow, `node`; para MP4 também `ffmpeg` e
   `puppeteer`/`puppeteer-core` (o caminho vem no `deck.config`).
3. Leia **agora** `SKILL/references/runtime.md` e `SKILL/references/motion-kit.md` — são as regras que
   quebram se ignoradas.

**Pronto quando:** `ROOT/DESIGN.md` e `deck.config.json` existem, com as orientações do prompt já
resolvidas em valores (nenhum placeholder), e
`python3 tools/render.py` roda.

## Fase 2 — Capa exemplar

Você mesmo escreve a capa: é o **exemplar** que todos os outros copiam (kit de movimento, pintura do
fundo, gancho de exportação, estilo do texto). Com a ferramenta Artifact: `quickstart` de slides → crie o
deck pelo `type_url` → escreva `project/deck.json` completo (ordem de todos os slides) e a capa →
`check_slide.py` + `render.py` → publique os dois. Sem Artifact: mesmo layout de arquivos; a entrega é
`tools/standalone.py` (HTML) e o MP4.

**Pronto quando:** a capa passa na checagem, você leu o render dela, e ela está publicada.

## Fase 3 — Cenas em paralelo

Um autor por slide → um revisor adversarial do mesmo slide → uma passada de consistência no deck
inteiro. Script e prompts em `SKILL/references/workflow.md`.

**Pronto quando:** todos os slides dão `RESULT PASS`, todo revisor voltou `ok`/`fixed`, e a consistência
voltou `allPass`.

## Fase 4 — Sua leitura, publicação, entrega

`python3 tools/contact_sheet.py` → leia as folhas **em ordem**, como a plateia. Corrija o que destoa,
publique, e entregue: link, duração de cada cena, o que ficou para o usuário decidir (uma linha cada).
Ofereça o MP4 em uma linha se não foi pedido.

**Pronto quando:** o deck publicado é o que você leu nas folhas, e as decisões pendentes estão na resposta.

## Fase 5 — MP4 e HTML standalone

`SKILL/references/video.md`.

## Depois da entrega

Os ajustes que sempre chegam — "mais devagar/mais rápido", "cores erradas", "tá em loop", "esse objeto
parece girar ao contrário" — têm receita em `SKILL/references/motion-kit.md` § Ajustes. Mexa só no slide
citado; regrave o MP4 depois.
