# Receitas

Tudo aqui é autocontido: copie, troque os dados e use. Nenhuma receita depende de
outra skill nem de arquivo fora desta pasta.

1. [O kit de cena](#1-o-kit-de-cena): toca uma vez e repousa
2. [O deck sem nenhuma ferramenta](#2-o-deck-sem-nenhuma-ferramenta): um HTML só
3. [A capa em meio-tom](#3-a-capa-em-meio-tom)
4. [Código rodando passo a passo](#4-código-rodando-passo-a-passo)
5. [Janela de terminal](#5-janela-de-terminal)
6. [Foto real com crédito](#6-foto-real-com-crédito-wikimedia-commons)
7. [Ícones das marcas](#7-ícones-das-marcas)
8. [Reações com personalidade](#8-reações-com-personalidade)

## 1. O kit de cena

Toda cena é uma função `frame(t)`: cada atributo sai do tempo `t` (em ms). Isso deixa
renderizar qualquer quadro sob demanda (miniatura, PDF, vídeo) e faz a cena tocar
uma vez e parar no último quadro, que é o pôster.

```html
<svg id="v" viewBox="0 0 1664 552" style="width:100%;height:100%"></svg>
<script>
(function(){
var END=9000;                                    /* quando o estado final está completo */
var R=matchMedia('(prefers-reduced-motion: reduce)').matches;
function cl(x){return x<0?0:x>1?1:x}
function eo(x){x=cl(x);return 1-Math.pow(1-x,3)}                         /* entradas */
function ez(x){x=cl(x);return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2}       /* viagens */
function pop(x){x=cl(x);return x<.7?eo(x/.7)*1.08:1.08-.08*eo((x-.7)/.3)} /* mola curta */
function p(t,a,b){return cl((t-a)/(b-a))}        /* 0→1 entre a e b */
function L(a,b,k){return a+(b-a)*k}
function A(e,o){for(var k in o)e.setAttribute(k,o[k])}
function mk(tag,o,txt,par){var e=document.createElementNS('http://www.w3.org/2000/svg',tag);A(e,o);
  if(txt!=null)e.textContent=txt;(par||document.getElementById('v')).appendChild(e);return e}

var card=mk('rect',{x:0,y:0,width:300,height:64,rx:14,fill:'#FBFAF7',stroke:'#D9DED1'});
function frame(t){
  var k=eo(p(t,200,800));
  A(card,{opacity:k,transform:'translate('+L(0,400,ez(p(t,1000,1900)))+' '+(20*(1-k))+')'});
}
var T0=null;
function tick(){var f=window.__FREEZE_T;if(T0==null)T0=performance.now();
  var t=f!=null?f:R?END:Math.min(performance.now()-T0,END);frame(t);
  if(f==null&&!R&&t<END)requestAnimationFrame(tick)}
tick();
})();
</script>
```

- `window.__FREEZE_T = 4200` antes do script congela a cena nesse tempo: é assim que
  se tira uma captura de qualquer quadro.
- Movimento reduzido mostra direto o último quadro.
- Muitas partículas (a capa em meio-tom): desenhe num `<canvas>` dentro de
  `frame(t)` e deixe o texto num `<svg>` por cima, nítido.

## 2. O deck sem nenhuma ferramenta

Um arquivo HTML, uma `<section>` por slide em 1920×1080 escalado para a tela, setas
e clique para navegar, e a cena de cada slide recomeçando quando ele aparece. O
primeiro clique num slide cuja cena ainda toca termina a cena; o próximo passa.

```html
<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=JetBrains+Mono:wght@500&display=swap">
<style>
html,body{margin:0;height:100%;background:#111;overflow:hidden}
#stage{position:absolute;width:1920px;height:1080px;left:50%;top:50%;transform-origin:center}
section{position:absolute;inset:0;display:none;box-sizing:border-box;padding:128px;font-family:Inter,sans-serif}
section.on{display:block}
iframe{position:absolute;border:0}
</style></head><body><div id="stage">

<section style="background:#17302A;color:#F4EFE3">
  <iframe data-scene="capa" style="left:0;top:0;width:1920px;height:1080px"></iframe>
  <h1 style="position:relative;font:500 120px 'JetBrains Mono';margin:0">A gramática<br>já é o código</h1>
</section>
<!-- … um <section> por slide … -->

</div>
<template id="capa"><!-- o HTML da cena: <svg>/<canvas> + o kit da receita 1 --></template>
<script>
var S=[].slice.call(document.querySelectorAll('section')),i=0,stage=document.getElementById('stage');
function fit(){var k=Math.min(innerWidth/1920,innerHeight/1080);stage.style.transform='translate(-50%,-50%) scale('+k+')'}
function show(n){S[i].classList.remove('on');i=Math.max(0,Math.min(S.length-1,n));S[i].classList.add('on');
  S[i].querySelectorAll('iframe[data-scene]').forEach(function(f){
    f.srcdoc='<html><body style="margin:0;overflow:hidden">'+document.getElementById(f.dataset.scene).innerHTML+'</body></html>'})}
function next(){var f=S[i].querySelector('iframe[data-scene]');var w=f&&f.contentWindow;
  if(w&&!w.__done){w.__FREEZE_T=1e9;w.__done=true;return}show(i+1)}
addEventListener('keydown',function(e){if(['ArrowRight',' ','PageDown'].includes(e.key))next();if(['ArrowLeft','PageUp'].includes(e.key))show(i-1)});
addEventListener('click',next);addEventListener('resize',fit);fit();show(0);
</script></body></html>
```

`__FREEZE_T=1e9` faz o próximo quadro da cena ir direto para o final. Para a cena
marcar que terminou sozinha, acrescente no fim do `tick` do kit:
`if(t>=END)window.__done=true`.

## 3. A capa em meio-tom

Desenhe a forma do assunto num canvas escondido, com desfoque para as bordas virarem
degradê. Depois amostre uma grade: cada célula vira um ponto do tamanho da cobertura.
Na cena, cada ponto voa de um lugar sorteado até a sua célula.

```js
var W=1920,H=1080,G=14;                                   /* G = passo da grade */
function rng(a){return function(){a|=0;a=a+0x6D2B79F5|0;var t=Math.imul(a^a>>>15,1|a);
  t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
var off=document.createElement('canvas');off.width=W;off.height=H;var o=off.getContext('2d');
o.filter='blur(7px)';o.fillStyle=o.strokeStyle='#000';o.lineWidth=18;o.lineCap='round';
/* a forma do assunto: aqui, uma árvore */
function node(x,y,r){o.beginPath();o.arc(x,y,r,0,7);o.fill()}
function edge(a,b,c,d){o.beginPath();o.moveTo(a,b);o.bezierCurveTo(a,(b+d)/2,c,(b+d)/2,c,d);o.stroke()}
edge(1400,260,1180,520);edge(1400,260,1620,520);node(1400,260,70);node(1180,520,48);node(1620,520,48);
var px=o.getImageData(0,0,W,H).data,dots=[],r=rng(7);
for(var y=G/2;y<H;y+=G)for(var x=G/2;x<W;x+=G){var a=px[((y|0)*W+(x|0))*4+3]/255;
  if(a>.06)dots.push({x:x,y:y,r:G*.48*Math.sqrt(a),sx:r()*W,sy:r()*H,d:r()*900})}

var cv=document.querySelector('canvas'),cx=cv.getContext('2d');
function frame(t){var dpr=devicePixelRatio||1;cv.width=W*dpr;cv.height=H*dpr;cx.scale(dpr,dpr);
  cx.fillStyle='#D4AF6A';
  for(var i=0;i<dots.length;i++){var d=dots[i],k=ez(p(t,300+d.d,1900+d.d));
    cx.globalAlpha=k;cx.beginPath();cx.arc(L(d.sx,d.x,k),L(d.sy,d.y,k),d.r*(0.4+0.6*k),0,7);cx.fill()}}
```

- O canvas precisa de `style="width:100%;height:100%"` e o tamanho lógico fixo
  (1920×1080) para não depender do layout do primeiro quadro.
- Para um movimento contínuo calmo depois que a capa monta, some
  `Math.sin(now/900+d.x/80)*1.5` ao `y` de cada ponto, e só na capa.

## 4. Código rodando passo a passo

Três peças: a fila de entrada com uma seta, o código com a linha ativa destacada, e
um painel de estado. Cada passo é uma linha numa tabela de tempos; `frame(t)` só lê
qual passo está valendo.

```js
var TOK=['a','a','b','b','EOF'];
var STEP=[ /* tempo, índice do token, linha ativa, estado */
  [ 800,0,1,{posicao:0,token:"'a'"}],
  [2400,1,2,{posicao:1,token:"'a'"}],
  [4000,2,4,{posicao:2,token:"'b'"}]];
var CODE=['def S(self):','    self.comparar(\'a\')','    if self.tokenCorrente == \'a\':','        self.S()','    self.comparar(\'b\')'];
/* desenhe: tokens em caixas (x = 40 + i*64), a seta abaixo, as linhas de CODE em mono 24,
   um retângulo de destaque atrás da linha ativa, e o painel com chave → valor */
function frame(t){
  var s=0;for(var i=0;i<STEP.length;i++)if(t>=STEP[i][0])s=i;
  var a=STEP[Math.max(0,s-1)],b=STEP[s],k=ez(p(t,b[0],b[0]+500));
  A(arrow,{transform:'translate('+L(40+a[1]*64,40+b[1]*64,k)+' 70)'});
  A(hl,{y:L(a[2]*32,b[2]*32,k)});
  valPos.textContent=b[3].posicao;valTok.textContent=b[3].token;
}
```

- Cor do código: palavra-chave em negrito, nome de função num destaque, string no
  outro destaque, comentário apagado. As mesmas cores no deck inteiro.
- Um valor que muda dá um `pop` de 300 ms. Um erro faz a linha tremer e ficar na cor
  de erro, com a mensagem ao lado.

## 5. Janela de terminal

```js
function term(par,x,y,w,h,title){var g=mk('g',{transform:'translate('+x+' '+y+')'},null,par);
  mk('rect',{width:w,height:h,rx:14,fill:'#141614',stroke:'#2E322B'},null,g);
  [0,1,2].forEach(function(i){mk('circle',{cx:22+i*20,cy:22,r:6,fill:'#3A3F37'},null,g)});
  mk('text',{x:90,y:30,'font-family':'ui-monospace,Menlo,monospace','font-size':24,fill:'#8E9686'},title,g);
  return g}
/* linhas: cada uma aparece digitada; a última leva um cursor que pisca 3 vezes e fica */
var LINES=[['$ ','/goal Termine o que está aberto no milestone 1','#F4EFE3'],
           ['','Not satisfied: open issues remain in milestone 1','#E39A7E']];
function type(el,s,k){el.textContent=s.slice(0,Math.round(s.length*cl(k)))}
```

Mostre o texto real, limpo do que for sensível. O texto do terminal fica no idioma
em que a ferramenta escreveu.

## 6. Foto real com crédito (Wikimedia Commons)

Busque com a API pública, com uma pausa entre pedidos (o Commons devolve 429 se a
busca for rápida demais):

```bash
curl -s -A "class-slide/1.0 (slides de aula)" \
 "https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch=filetype:bitmap%20magnifying%20glass&gsrnamespace=6&gsrlimit=5&prop=imageinfo&iiprop=url|extmetadata&iiurlwidth=640&format=json"
```

- De cada resultado: `thumburl` (a imagem em 640 px),
  `extmetadata.Artist.value` (tire o HTML) e `extmetadata.LicenseShortName.value`.
- Fique só com licença livre: CC0, domínio público, CC BY, CC BY-SA. O crédito vai no
  rodapé do slide: `foto: <autor> · <licença>`.
- Recorte em 4:3 (500×376) e mostre pequeno, no canto superior direito do slide
  (250×188, cantos de 12 px), sem sombra.
- Escolha a foto pela metáfora concreta, e olhe a imagem antes de usar: o primeiro
  resultado da busca muitas vezes é outra coisa.

## 7. Ícones das marcas

Os paths oficiais estão no pacote simple-icons (viewBox 24×24):

```bash
curl -sL https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/github.svg
# slugs: github, linear, slack, figma, googledrive, notion, claude, anthropic, whatsapp
```

```js
function ico(d,x,y,size,color,par){
  return mk('path',{d:d,transform:'translate('+x+' '+y+') scale('+size/24+')',fill:color},null,par)}
```

Monocromático na cor do texto; a cor da marca só quando o ícone é o símbolo dela (o
laranja do Claude, por exemplo).

## 8. Reações com personalidade

| Efeito | Como | Quando |
|---|---|---|
| Carimbo | escala 1,4 → 1 com `pop`, rotação de -8°, borda grossa | algo foi aprovado ou decidido |
| Tremida | `translateX(sin(k·π·6)·6·(1-k))` por 600 ms | erro, recusa, "duas coisas numa frase" |
| Check | círculo cresce com `pop` e o traço se desenha depois | um passo terminou |
| Contador | o número sobe junto com os elementos que conta, nunca sozinho | um fato com número |
| Virar cartão | `scaleX(|cos(k·π)|)` e troca a face na metade | problema → o que fazer |
| Partir | o bloco ganha rachaduras desenhadas e os pedaços viajam | quebrar uma ideia |
| Montar | pontos ou nós chegam um a um até formar a figura | capa, árvore, estrutura |

Toda reação acontece uma vez, no seu beat, e deixa o quadro parado em seguida.
