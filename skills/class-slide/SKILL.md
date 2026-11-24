---
name: class-slide
description: >
  Use quando for fazer os slides de uma aula, treinamento, workshop ou palestra
  que precisa ter personalidade: capa que é o próprio assunto desenhado, animação
  em todo slide, código, terminal e telas de verdade rodando passo a passo, uma
  foto real com crédito em cada conceito, cores com papel fixo, capítulos e um
  exercício para a plateia. Vale para criar um deck novo e para dar vida a um deck
  que ficou sem graça, cru ou com cara de documento. Funciona sozinha ou como a
  camada de estilo da skill animated-deck. Triggers: "slide de aula", "deck de
  aula", "deixa mais vivo", "mais fun", "mais divertido", "mais personalidade",
  "tá sem graça", "abusa da animação", /class-slide
---

# Class slide

Uma aula boa parece uma coisa acontecendo na frente da plateia, não um documento
projetado. A personalidade vem do desenho, das fotos e do movimento. O texto
continua simples: frase inteira que diz o que acontece, sem slogan, sem frase de
palco. Se o deck só ficar "fun" porque o texto ficou engraçadinho, errou.

O tema é o argumento da invocação; sem argumento, é o deck ou o assunto da
conversa.

Tudo o que esta skill precisa vem com ela: as receitas com código pronto estão em
[`references/recipes.md`](references/recipes.md), inclusive um deck completo num
HTML só, para quem não tem nenhuma outra ferramenta. Se a skill animated-deck
estiver instalada, você pode usar o runtime e as checagens dela (cena num
`<x-embed>`, `check_slide.py`, `render.py`) e tratar esta como o estilo; ela é
opcional.

## Antes do primeiro slide, decida e escreva

- **A tese da aula numa frase.** Ela é o título da capa ("A gramática já é o
  código"). Não é slogan: é o que a plateia vai entender no fim.
- **Os capítulos (3 a 5).** Viram o eyebrow de cada slide: `NN · CAPÍTULO`
  ("03 · A MÁQUINA"). A plateia sempre sabe onde está.
- **A tabela de papéis das cores.** Um fundo claro e um escuro, duas cores de
  destaque com papel fixo no deck inteiro (por exemplo, o que vem da máquina × o
  que a pessoa decide) e uma cor só para erro ou recusa, sempre junto da palavra.
  Quem olha aprende a legenda no terceiro slide e lê o resto sem pensar.
- **Onde fica escuro.** Fundo escuro tem motivo: os slides em que a máquina
  trabalha (execução, terminal, o agente de noite). Ideia e conceito ficam no
  claro.

## As regras, e por quê

1. **A capa é o assunto desenhado.** Fundo cheio numa cor forte da paleta e um
   único desenho grande do tema (a árvore, o fluxo, a peça) em meio-tom, feito de
   pontinhos que se juntam uma vez e param. O título é a tese, o subtítulo diz o
   que vem. Uma capa genérica (logo e título) promete um deck genérico.
2. **A coisa real ganha da maquete.** Código, terminal, tela, PR, issue: mostre o
   de verdade e faça ele rodar passo a passo. Uma seta avança token por token, a
   linha que executa fica destacada, um painel de estado muda de valor, a pilha
   de chamadas cresce, a árvore se monta de dentro para fora. Maquete só quando a
   coisa real não existe. O que é sensível (cliente, paciente, segredo) sai limpo
   antes de entrar no slide.
3. **Uma foto real em cada conceito.** Uma metáfora concreta do mundo (pilha de
   pratos para "pilha", catraca para "comparar", matrioska para "recursão"),
   pequena no canto superior direito, com o crédito no rodapé: `foto: autor ·
   licença`. Só Wikimedia Commons com licença livre ou foto do próprio usuário. A
   foto dá textura de mundo real que nenhum diagrama dá.
4. **Ícones de verdade.** As ferramentas aparecem com a marca delas (Slack,
   GitHub, Linear, Figma): paths do simple-icons, monocromáticos, na cor da marca
   só quando é o símbolo dela. Glifos pequenos de interface (colchetes de leitura,
   escudo, lápis, bandeira) marcam o tipo de bloco ao lado do texto, nunca
   sozinhos como enfeite.
5. **Um exercício, pelo menos.** Um slide em que a plateia faz: um editor vazio
   escrito "seu editor" e, ao lado, "precisa devolver" ou "precisa ter". Aula em
   que ninguém faz nada vira palestra.
6. **Rodapé fixo.** `NN / total · tema` à esquerda, créditos das fotos à
   direita, em mono pequeno.

## Movimento: abuse, com propósito

Todo slide tem uma cena, e toda cena mostra uma coisa acontecendo. O vocabulário
que dá vida:

- **Montar:** pontinhos de meio-tom voando até formar o desenho; uma árvore que
  cresce nó a nó; linhas que se desenham.
- **Executar:** seta que avança, linha destacada que desce pelo código, valor que
  troca no painel, pilha que empilha e desempilha.
- **Reagir:** carimbo que cai com um pouco de mola, cartão que treme no erro e
  volta, check que dá um pop, contador que sobe até o número real.
- **Transformar:** um bloco que se parte em pedaços, cartões que viram, um item
  que viaja de uma coluna para outra.

Mola e overshoot são bem-vindos (é o que deixa "fun"), mas a leitura manda:

- Um ponto focal por vez.
- Texto parado enquanto é lido, por 650 ms + 200 ms por palavra.
- A cena toca uma vez e repousa num quadro que explica o slide sozinho, porque é
  esse quadro que vai para a miniatura e o PDF.
- Só capa e fecho podem ter movimento contínuo, calmo e sem emenda.

## Como construir

1. Monte a paleta, os capítulos e a capa primeiro. A capa é o exemplar que os
   outros slides copiam.
2. Para cada slide, nesta ordem: o que é real ali (código, tela, terminal), a foto
   do conceito, a cena que faz a coisa acontecer, o texto curto.
3. Os padrões prontos estão em [`references/recipes.md`](references/recipes.md):
   a capa em meio-tom, o passo a passo de código, a janela de terminal, como
   buscar a foto no Wikimedia com o crédito e os ícones das marcas. Leia a
   receita antes de escrever a cena que a usa.
4. Renderize o quadro de repouso e dois ou três quadros no meio de cada cena e
   leia as imagens. Corrija sobreposição, texto cortado ou pequeno, contraste baixo
   e beat rápido demais.

## Antes de entregar

- A capa desenha o assunto, não só o logo.
- Os slides em que existe uma coisa real a mostram rodando, e não uma maquete.
- Todo slide de conceito tem foto com crédito no rodapé.
- As cores obedecem à tabela de papéis; a cor de erro só aparece com a palavra.
- Há pelo menos um exercício.
- Nenhuma frase de efeito: o visual tem personalidade, o texto é simples.
- Cada quadro de repouso foi lido como a plateia leria.
