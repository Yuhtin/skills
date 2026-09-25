---
name: animated-deck
description: >
  Use para preparar um deck de slides animado que explica um projeto a uma plateia (arquitetura,
  produto, fluxo, pitch, onboarding): pesquisa o projeto, faz grilling com o usuário para preencher
  cada placeholder do brief — plateia, roteiro, fatos, cores e fontes da marca, cenas — e devolve um
  prompt pronto para colar num chat novo que constrói o deck (motion design em SVG/canvas, toca uma
  vez, exporta MP4). Triggers: "deck animado", "slides animados", "apresentação com animação",
  "monta um deck pra apresentar", /animated-deck
---

# Deck animado — do projeto ao prompt

Esta skill **não constrói** o deck. Ela produz o **brief** completo e o entrega como um prompt para
colar num chat novo, que então segue `references/build.md`. Separar assim deixa o chat que constrói
com o contexto limpo, só com o contrato.

O padrão de qualidade saiu de quatro pedidos de um usuário; o brief já nasce com eles:

| O pedido que foi preciso fazer | Vira padrão no brief |
|---|---|
| "seja criativo — animações, gráficos em SVG que se mexem" | toda cena é motion design que carrega significado, não diagrama com fade |
| "use as cores da marca" | paleta lida dos tokens do projeto, um acento, fundo da marca |
| "toca uma vez, sem loop" + "mais devagar pra dar tempo de ler" | a cena toca uma vez e repousa no **pôster**; ritmo de leitura |
| "exporta pra mp4" | gravação quadro a quadro pronta no fim |

## Fase 1 — Research do projeto

Antes de perguntar qualquer coisa, pesquise o projeto de onde o deck sai — o usuário responde melhor
a uma recomendação do que a uma pergunta em branco. Levante, com fonte (`arquivo:linha`, doc, URL):

- **O assunto:** o código, docs, ADRs, specs e métricas do tema que o usuário pediu; o caminho que a
  plateia precisa ver (ex.: "da pergunta à resposta"); números reais; o que é presente e o que é futuro.
- **A marca:** tokens de cor (tema CSS, Tailwind, design system), fontes, favicon/logo, landing page;
  um motivo visual que a capa possa usar.
- **O ambiente de build:** Chrome, `python3` + Pillow, `node`, `ffmpeg`, um `puppeteer` existente em
  algum `node_modules`.

Para temas grandes, delegue a leitura a subagentes e guarde só as conclusões.

**Pronto quando:** cada placeholder de [`references/prompt-template.md`](references/prompt-template.md)
tem uma **resposta recomendada** tirada do research, ou está marcado como decisão do usuário.

## Fase 2 — Grilling

Invoque a skill `grilling` (a mesma sessão do `/grill-me`) sobre a árvore de
[`references/grill.md`](references/grill.md), levando as recomendações da Fase 1. Sem `grilling`
instalada, siga as regras dela: uma pergunta por vez, cada uma com a sua recomendação; fato descobrível
você descobre; decisão é do usuário e você espera a resposta.

**Pronto quando:** todo placeholder tem valor confirmado e o usuário disse que fechou.

## Fase 3 — O prompt

Preencha [`references/prompt-template.md`](references/prompt-template.md) e devolva-o inteiro num único
bloco de código, pronto para colar, com uma linha antes: "Cole num chat novo." Nada fica em aberto: um
`{{…}}` sobrando quebra o build.

**Pronto quando:** o bloco não tem nenhum `{{`, todo número do roteiro está na lista de fatos, e cada
slide tem cena descrita em beats.
