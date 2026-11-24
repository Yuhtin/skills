# Construir o deck (o chat que recebeu o prompt)

Você recebeu um prompt-guia gerado pela skill `animated-deck` (plateia, mensagem, palavras, paleta,
fontes, fatos com fonte, roteiro e ideias de cena). O que ele traz decidido vale; o que vem como
orientação você decide, seguindo `motion-kit.md`. Construa num tiro só; pergunte só se algo bloquear.

`SKILL` = a pasta desta skill (a que contém este arquivo). **Pasta de trabalho** (`ROOT`): uma pasta no
scratchpad (`<scratchpad>/<slug>-deck/`), nunca dentro do repositório do projeto.

## Fase 1 — Ferramentas e contrato

1. Copie `SKILL/scripts/` para `ROOT/tools/`. Escreva `ROOT/deck.config.json` com o bloco `deck.config`
   do brief, e `ROOT/DESIGN.md` com a parte "Brief" do prompt (seções §1–§7), acrescentando no topo os caminhos de `SKILL/references/runtime.md` e `motion-kit.md` e o do slide exemplar (a capa).
2. Pré-requisitos: Chrome, `python3` com Pillow, `node`; se as Saídas do brief incluem MP4, também
   `ffmpeg` e `puppeteer`/`puppeteer-core` (o caminho vem no `deck.config`).
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
`tools/standalone.py` (HTML).

**Pronto quando:** a capa passa na checagem, você leu o render dela, e ela está publicada.

## Fase 3 — As outras cenas, uma por vez

Você mesmo escreve todos os slides, na ordem do `deck.json`, sem subagente nem workflow: um contexto só
mantém o deck coerente (o mesmo cartão, a mesma pessoa, o mesmo exemplo desenhado igual em todo slide).
Para cada slide:

1. Planeje as regiões e os tempos dos beats; escreva o arquivo copiando o molde do exemplar.
2. `check_slide.py` até `RESULT PASS`; `render.py` em ~6 tempos de 0 a `END` mais o pôster, e **leia** cada PNG.
3. Releia como revisor adversarial, supondo que ainda há defeito: texto sobreposto ou cortado, legenda que
   some antes de ser lida (renderize logo antes e logo depois de cada beat), contraste baixo, fato ou palavra
   diferente do `DESIGN.md`, papel de cor trocado, cena que é diagrama com fade. Corrija e renderize de novo.
4. Publique os slides prontos de três em três, para o usuário acompanhar.

**Pronto quando:** todos os slides dão `RESULT PASS` e você leu o pôster e os beats de cada um.

## Fase 4 — Sua leitura, publicação, entrega

`python3 tools/contact_sheet.py` → leia as folhas **em ordem**, como a plateia. Corrija o que destoa,
publique, e entregue: link, duração de cada cena, o que ficou para o usuário decidir (uma linha cada).
Se a ocasião é ao vivo, avise que no Present o clique sempre passa de slide, e que o `out/deck.html` termina
a cena primeiro.

**Pronto quando:** o deck publicado é o que você leu nas folhas, e as decisões pendentes estão na resposta.

## Fase 5 — HTML standalone e MP4

Gere o que está nas Saídas do brief, seguindo `SKILL/references/video.md`. O MP4 só existe se estiver lá ou se
o usuário pedir depois.

## Depois da entrega

Os ajustes que sempre chegam — "mais devagar/mais rápido", "cores erradas", "tá em loop", "esse objeto
parece girar ao contrário" — têm receita em `SKILL/references/motion-kit.md` § Ajustes. Mexa só no slide
citado; se já existe MP4, regrave-o depois.
