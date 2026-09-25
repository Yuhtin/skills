# Kit de movimento — como toda cena é escrita

## O contrato

- A cena inteira é **uma função `frame(t)`**: todo atributo sai de `t` (ms de tempo de cena). Nada de
  `setTimeout`, `@keyframes`, transições CSS, estado entre quadros. É o que deixa renderizar qualquer
  quadro sob demanda (`render.py`, o MP4, a exportação).
- A cena **toca uma vez** e **repousa**: `END` = quando o estado final está completo; `F = END` é o
  **pôster** (repouso, miniatura, PDF). Sem loop, sem fade-out. Sair e voltar ao slide recomeça sozinho.
- O pôster explica o slide **sozinho**. Se a sequência termina num contraexemplo ou num fluxo que não
  assenta, reencene o final para o repouso mostrar a ideia inteira (o caso certo e o recusado lado a lado,
  contadores assentados).
- Exceção: capa e fim podem ter um movimento **ambiente** contínuo (um anel girando, grão respirando).
  Loop ambiente sem emenda: cada coisa dá um número inteiro de voltas/passos por ciclo.

## O código (copie literalmente; escreva o SVG e o corpo de `frame`)

```html
<style>
html,body{background:#FFFFFF;color-scheme:only light}svg{display:block;width:100vw;height:100vh}
.s{font-family:ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}
.f{font-family:ui-serif,"New York",Georgia,"Times New Roman",serif}
.m{font-family:ui-monospace,"SF Mono",Menlo,Consolas,monospace}
</style>
<svg id="v" viewBox="0 0 1664 552" preserveAspectRatio="xMidYMid meet">
 <!-- marcação estática com ids; ou crie os elementos UMA vez no script -->
</svg>
<script>
(function(){
var END=14000,F=END,SP=1;               /* SP: velocidade do relógio da cena (ajuste fino de ritmo) */
var R=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
function cl(x){return x<0?0:x>1?1:x}
function eo(x){x=cl(x);return 1-Math.pow(1-x,3)}                 /* entradas */
function ez(x){x=cl(x);return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2} /* viagens */
function pop(x){x=cl(x);return x<.7?eo(x/.7)*1.06:1.06-.06*eo((x-.7)/.3)} /* só confirmações */
function p(t,a,b){return cl((t-a)/(b-a))}
function L(a,b,k){return a+(b-a)*k}
function $(i){return document.getElementById(i)}
function A(e,o){for(var k in o)e.setAttribute(k,o[k])}
function frame(t){
  /* … todo atributo a partir de t … */
}
var T0=null;
function tick(){var f=window.__FREEZE_T;if(T0==null)T0=performance.now();
 var t=f!=null?f:R?F:Math.min((performance.now()-T0)*SP,END);frame(t);
 if(f==null&&!R&&t<END)requestAnimationFrame(tick)}
tick();
if(window.appifactEmbed)appifactEmbed.onUpdate(function(s){if(s&&s.exporting)frame(F)});
})();
</script>
```

- Troque `#FFFFFF` em `html,body` pela cor de fundo do slide; `viewBox` = tamanho da caixa do embed.
- Muitas partículas (milhares de grãos, poeira, ruído): `<canvas>` desenhado em `frame(t)` com PRNG
  determinístico (mulberry32), dimensionado por `cv.clientWidth||W` × devicePixelRatio. Texto e ícones
  continuam num `<svg>` por cima, nítidos.
- Orçamento: ≤ ~120 elementos SVG, ≤ 15 000 caracteres por embed, texto ≥ 24 unidades.

## A régua de criatividade

Toda cena é uma pequena peça de **motion design**, não um diagrama com fade: metáforas físicas, coisas
que **viajam, encaixam, enchem, carimbam, se digitam, escaneiam**; profundidade por sobreposição e
opacidade; uma sequência de beats que a plateia segue sem narração. Calma e precisa (keynote, não
videoclipe): **um ponto focal por vez**, easing suave, espaço generoso, grade alinhada.

Metáforas que funcionaram (reuse o princípio, não o desenho):
- um caminho com estações e uma "pílula" (a pergunta) viajando por elas, cada parada deixando o seu resultado;
- um portão que separa um fluxo: a maioria passa reto e rápido, uma parte desce por outro caminho mais lento;
- um scanner que varre uma frase e liga cada número ao fato de onde veio — e um número sem fato fica vermelho e cai;
- um marca-texto que confere uma citação palavra por palavra contra a fonte;
- um cofre que tranca um envelope, uma chave que se quebra depois do prazo;
- um radar que varre pontos de dados e deixa cartões numa caixa de entrada;
- um escudo que divide uma mensagem: a ordem escondida bate e cai, o resto segue para revisão;
- uma árvore que cresce em dois níveis conforme o número de itens aumenta.

Evite: emoji, gradiente em tudo, cards com borda lateral colorida, brilho em tudo, texto que se mexe
enquanto precisa ser lido.

## Cor por papel

A paleta vem dos tokens da marca (`DESIGN.md` §2). Numa cena, **cor = papel**, igual em todos os slides:
- **acento da marca** = a escolha/ação principal da história (o que decide, o que foi escolhido, o que confirma);
- **tinta** em serifa = palavras, a voz do produto/da IA;
- **escada de cinzas** em mono, caixas com borda fina = dados, código, o que é sistema;
- **cor de recusa** = só junto da palavra que recusa ("barrado", "recusado", "não é um fato").
- Ênfase sem segunda cor: peso, tamanho, o contraste serifa/mono, um sublinhado ou ponto no acento.
- Brilho que funciona no escuro fica sujo no claro: no claro, troque por mudança de estado nítida
  (o preenchimento vira acento, um anel pulsa uma vez).

## Ritmo

- Todo texto que aparece na cena fica inteiro na tela, antes do próximo beat puxar o olho, por pelo
  menos **650 ms + 200 ms por palavra** (o meio-termo que agradou). Mais lento: 900 ms + 280 ms/palavra.
  Máquina de escrever conta a partir da última letra.
- Viagens de 600–1000 ms, entradas de 400–600 ms, um beat por vez.
- Cenas com muito texto ficam entre 15 e 30 s — ela toca uma vez e repousa; o apresentador fala por cima.

## Ajustes (o feedback que sempre chega)

- **"Está lento/rápido demais"** → mude só o `SP` daquele slide (o relógio da cena); os tempos internos
  ficam. Meio-termo entre duas versões: `SP = 2·END_novo / (END_antigo + END_novo)`. Se o slide tiver
  outra leitura de `performance.now()` (loop ambiente, redesenho de reserva), multiplique por `SP` lá também.
- **"As cores não são da marca"** → remapeie por papel com a tabela do `DESIGN.md` §2 e ponha as
  antigas em `bannedColors`; `check_slide.py` acha as que sobraram.
- **"Está em loop / reseta"** → a cauda do kit acima (`T0`, `Math.min(...,END)`, sem fade-out).
- **"Parece uma bola girando ao contrário"** → um anel/grão tem todas as partes girando no **mesmo**
  sentido; nada de faixas em sentidos opostos (lê como um segundo objeto), nada de disco/halo atrás
  do ícone central.
- **Fundo com retângulo branco** → a cena não pintou `html,body` com a cor do slide.
