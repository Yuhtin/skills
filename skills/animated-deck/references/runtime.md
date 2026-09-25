# O runtime dos slides — o que ele faz com a sua cena

Fatos do tipo **Slides** dos Artifacts (claude.ai), lidos do próprio runtime (`artifact-type/app.js`)
e confirmados em uso. Cada item é uma armadilha que já quebrou um deck.

## A cena mora num `<x-embed>`

- É o **único** lugar onde algo se move. `<svg>` inline no slide é imagem estática: scripts, SMIL e
  `<animate>` não rodam. `data-build-in`/`magic` são transições de Present, não animação.
- O conteúdo do `<x-embed>` é **texto cru** até `</x-embed>` (como `<script>`): nunca escreva essa
  sequência dentro dele. Limite **16 384 caracteres**; mire em ≤ 15 000.
- Filho **direto** da `<section>`, `position:absolute` com `left/top/width/height`. No máximo 8 por slide.
- Vira um iframe `sandbox="allow-scripts"` com CSP `default-src 'none'`: nada de rede, **nenhuma web
  font** (use pilhas de fonte do sistema: `ui-sans-serif,-apple-system,…`, `ui-serif,"New York",…`,
  `ui-monospace,"SF Mono",…`), nenhuma imagem externa. Scripts e estilos inline funcionam.
- O documento do iframe é `html,body{margin:0;padding:0;overflow:hidden}` + o seu HTML no `<body>`.
- **Pinte o fundo da página da cena**: `html,body{background:<fundo do slide>;color-scheme:only light}`.
  O host pode pôr uma tela branca opaca atrás do iframe; "transparente" vira um retângulo branco no slide.
- O texto do slide (fluxo) pinta **por cima** da cena. Liste a cena **primeiro** na `<section>`.
- Desenhe num `<svg viewBox="0 0 W H">` com W×H = o tamanho da caixa do embed, e
  `svg{width:100vw;height:100vh}`: aí 1 unidade = 1 px do slide, qualquer que seja o zoom.

## Quando a cena roda

- Ao **entrar** no slide o runtime cria o iframe; ao **sair**, remove. Por isso "tocar uma vez e só
  recomeçar ao voltar" é só medir o tempo desde o primeiro quadro (`T0`) — ver `motion-kit.md`.
- No primeiro instante o iframe pode ainda **não ter layout**: `clientWidth` = 0,
  `getComputedTextLength()` = 0. Canvas: dimensione pelo tamanho lógico (`cv.clientWidth||W`);
  medidas de texto: `canvas.measureText` com a mesma fonte, ou meça de novo quando der não-zero.
- Rotação ambiente contínua (capa/fim) usa `performance.now()` direto; mantenha a do resto no `tick`.

## Miniatura, PDF, PowerPoint

- Para exportar, o runtime chama `window.appifactEmbed.onUpdate(cb)` com `{exporting:true}` e fotografa
  o DOM **na hora** (clona o documento, troca canvas por `toDataURL`). Sem gancho, sai um quadro
  qualquer. O kit tem o gancho: `onUpdate(s ⇒ s.exporting && frame(F))`.
- Por isso `F` (o pôster) tem que explicar o slide sozinho — é o que o PDF e a miniatura mostram.

## Publicar e editar

- Fluxo: `quickstart` (intent `slides`) → publique com o `type_url` e um `title` → escreva
  `project/deck.json` (com `"order"` de **todos** os slides e `createdOnFiles`) e a capa → publique
  os dois; depois os outros slides, só os arquivos novos por chamada.
- `project/deck.json` + `project/slides/<id>.html` com **uma** `<section id="<id>">` cada. Faces de
  fonte do slide no `faces` do `deck.json` (Google Fonts `css2`, até 4 famílias).
- O editor **regrava** arquivos que o usuário abriu (reordena estilos, hex minúsculo, move
  `font-family`). Uma publicação recusada por versão nova: leia o arquivo da versão atual, compare
  com o que você publicou; se só mudou a formatação, publique o seu por cima e diga isso; se o usuário
  mudou conteúdo, aplique a sua mudança sobre a versão dele.
- O deck nasce privado; compartilhar é o menu Share da página — avise o usuário.

## As ferramentas de `tools/`

- `render.py` imita o runtime (mesma CSP, cena num iframe, fluxo por cima) e congela a cena via
  `window.__FREEZE_T`. É a sua forma de **ver** um quadro. Um Chrome por vez na máquina (trava em diretório).
- Não tente simular a exportação com screenshot: o Chrome headless fotografa antes do callback. A
  prova de exportação é o gancho presente + o render do pôster.
- `check_slide.py` reprova: tag/propriedade fora do subconjunto, fonte menor que o mínimo, cena sem
  fundo pintado, sem `__FREEZE_T`, sem gancho de exportação, JS que não compila, cor proibida pelo
  `deck.config.json`, fundo de seção fora da lista.
