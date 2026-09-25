# MP4 e HTML standalone

## MP4

O vídeo não é gravado da tela: cada cena roda num **relógio virtual** (`performance.now()` trocado),
o gravador avança 1/30 s, espera a cena confirmar que desenhou e fotografa. Sai liso a 30 fps em
qualquer máquina, e os quadros vão direto para o ffmpeg (nenhum arquivo intermediário; o disco só
recebe o MP4, ~5 MB por minuto).

1. Pré-requisitos: `ffmpeg`; `puppeteer` ou `puppeteer-core` (aponte um existente em
   `deck.config.json` → `"puppeteer"`, ou `npm i --no-save puppeteer-core` dentro do `ROOT`); Chrome.
2. `python3 tools/video_pages.py` — uma página por slide + `video/plan.json`. Cada slide dura
   `END ÷ SP + holdMs` (padrão 2,5 s parado no pôster); capa e fim ambiente: `ambientMs` /
   `ambientTailMs` do config. Confira a duração total que ele imprime.
3. Teste antes: `node tools/record.cjs --test <id> 0 3000 12000` e **leia** os PNGs — a cena tem que
   estar em estados diferentes (se estiver igual nos três, o relógio não pegou) e as fontes carregadas.
4. Grave em segundo plano: `node tools/record.cjs video/<slug>.mp4 > video/record.log 2>&1`, com um
   monitor em `record.log` para `done|DONE|Error|NO ACK|Target closed`. Leva ~2,5× a duração do vídeo.
5. Confira: `ffprobe` (duração, 1920×1080, 30 fps, número de quadros = plano) e extraia 6–8 quadros
   espalhados (`ffmpeg -ss <t> -i … -frames:v 1`) numa folha; leia. Copie para onde o usuário pediu
   (padrão `~/Downloads/<slug>.mp4`).

Mudou um slide depois? Regenere as páginas e regrave o vídeo inteiro (o fade entre slides depende da ordem).
Se uma gravação em andamento ficou velha por causa de uma mudança pedida, pare-a antes de mexer.

## HTML standalone

`python3 tools/standalone.py` → `out/deck.html`: um arquivo só, setas/espaço/clique avançam, `F` tela
cheia, cada slide recomeça a cena ao ser mostrado. É a entrega quando não há ferramenta Artifact, ou um
extra para abrir offline (as web fonts ainda vêm do Google Fonts).
