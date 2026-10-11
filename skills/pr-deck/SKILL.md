---
name: pr-deck
description: >
  Use para montar um deck de slides animado que explica as mudanças dos PRs abertos do usuário:
  levanta os PRs com `gh`, classifica cada um (correção pequena, feature, mudança de tela), decide
  o slide de cada um e entrega o research pronto para a skill `animated-deck`.
  Triggers: "deck dos meus PRs", "apresenta meus PRs abertos", "slides do que eu fiz", /pr-deck
---

# Deck dos PRs abertos

Esta skill é a **Fase 1 da `animated-deck`** especializada em PRs: ela levanta os PRs, decide o
tratamento de cada um e entrega a `animated-deck` com o research pronto e a maior parte do grilling
já respondida. O grilling que sobra, o prompt-guia e o build são da `animated-deck`
(se não estiver instalada: https://github.com/yuhtin/skills → skills/animated-deck).

Precisa do `gh` autenticado, dentro do repositório dos PRs.

Argumentos opcionais: a base (padrão: o branch padrão do repositório), números de PR para
restringir, a plateia.

## 1. Levantar os PRs

```sh
BASE=$(gh repo view --json defaultBranchRef -q .defaultBranchRef.name)
gh pr list --author @me --base "$BASE" --state open --limit 100 \
  --json number,title,url,isDraft,additions,deletions,headRefName,body,files
```

Rascunhos entram, marcados "rascunho". Nenhum PR aberto: diga isso e pare.

Um subagente por PR, em paralelo (PRs com menos de ~100 linhas você mesmo lê). Cada um lê o corpo do
PR e `gh pr diff <n>` e devolve uma **ficha**:

- **tipo**: `pequeno` (bug fix ou mudança que cabe numa frase) ou `feature` (capacidade nova, ou
  comportamento que muda o que a pessoa consegue fazer); e, à parte, **frontend: sim/não** — um
  PR é frontend quando muda algo que se vê numa tela, e isso soma ao tipo.
- **a mudança** em uma frase, nas palavras de quem usa o produto, e **o efeito** para essa pessoa.
- **antes → depois**: o que acontecia e o que acontece agora, com um exemplo concreto.
- para frontend: **a página** (nome no menu e rota), **a região** da tela que mudou e o que mudou
  nela (elemento, texto, posição, estado).
- o ticket ou a issue ligada ao PR, se houver.
- cada fato com fonte: `#<n>` + `arquivo:linha` do diff, ou a seção do corpo do PR.

Prints de antes/depois: quando o corpo do PR traz imagens, baixe-as para uma pasta nova e vazia do
scratchpad e leia-as — são a **referência** do redesenho da região, e a fonte do "antes".

**Pronto quando:** todo PR da lista tem ficha completa, e todo PR frontend tem página, região e
antes/depois identificados (por print ou, sem print, pelo diff do componente).

## 2. O tratamento de cada PR

| A ficha diz | Vira |
|---|---|
| `pequeno` | Uma linha num slide agregado: 3 a 5 por slide, agrupados por área do produto. Cada linha é o efeito, com o `#n` em mono. A cena é mínima: as linhas assentam uma a uma. |
| `feature` | Um slide só dele. A cena **é** a explicação: o caminho da feature em movimento (o que entra, o que a feature faz com isso, o que sai), com um exemplo fictício. Título e lede curtos; nenhum parágrafo. |
| frontend (qualquer tipo) | **Onde → o quê → antes/depois**: um mapa pequeno da página (menu e contorno da tela, a região marcada no acento) → zoom na região → o estado de antes dá lugar ao de depois, com a diferença marcada no acento. O pôster repousa com antes e depois lado a lado. |

A região é **redesenhada em SVG** com os tokens da marca, simplificada ao que mudou: a cena não
carrega imagem (CSP sem rede, 16 384 caracteres), e um `<img>` no slide fica parado, sem zoom. A
tela inteira aparece só como o mapa de localização.

`feature` com frontend: uma cena só, que localiza a página e depois mostra a feature funcionando
nela. `pequeno` com frontend: ganha meio slide (dois por slide), cada um com o seu antes/depois da
região.

## 3. O roteiro

Capa → panorama (quantos PRs, por tipo e por área) → features, da maior para a menor → mudanças
de tela → slides agregados dos pequenos → fecho. Na `animated-deck`, cada slide cita os `#n` que
cobre no eyebrow ou em mono.

**Pronto quando:** todo PR da lista aparece em exatamente um slide.

## 4. Entregar para a `animated-deck`

Invoque a skill `animated-deck` levando as fichas, a tabela de tratamento e o roteiro como o
research dela. Ainda falta, da Fase 1 dela: a marca (tokens de cor e fontes **do repositório
atual**) e o ambiente de build.

Chegam ao grilling já respondidos, como recomendação para confirmar em uma linha:

- **Mensagem:** a frase que resume o lote de PRs (proponha uma).
- **Fontes da verdade:** as fichas; nada fora delas vira fato. PR aberto é **proposta**: rótulo
  "em revisão" no slide, "rascunho" nos rascunhos.
- **Linguagem:** o idioma dos títulos dos PRs; sem jargão; exemplos fictícios e os mesmos no deck inteiro.
- **Movimento, saídas:** os padrões da `animated-deck`.
- **Cenas:** as da tabela de tratamento.

O grilling pergunta, numa rodada só: a plateia e a ocasião (se não vieram no argumento), a tabela
de classificação (PR · tipo · frontend · slide) para o usuário corrigir ou cortar PRs, e o roteiro
de títulos.

**Pronto quando:** a `animated-deck` entregou o prompt-guia dela, com as regras da tabela de
tratamento escritas na ideia de cena de cada slide do §7.
