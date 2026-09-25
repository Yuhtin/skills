# Modelo do `ROOT/DESIGN.md`

O `DESIGN.md` é o contrato que todo agente lê antes de escrever um slide. Preencha cada seção; o que
estiver entre `<>` é seu.

```markdown
# <Título do deck> — sistema, fatos e briefs

Plateia: <quem, o que já sabe>. Ocasião: <ao vivo / vídeo / PDF, data>. Idioma: <pt-BR>.
Mensagem que fica: "<uma frase>".
ROOT = esta pasta. Slides em `ROOT/project/slides/<id>.html`. Regras do runtime:
<caminho desta skill>/references/runtime.md; kit de movimento: <…>/references/motion-kit.md.
Exemplar: `ROOT/project/slides/<capa>.html`.

## 1. Palavras
| Diga | Nunca diga |
|---|---|
| <termo do dia a dia> | <jargão que ele substitui> |
Tom: <frases curtas, verbos de ação>. Títulos apresentam o slide; sem drama ("não é X, é Y").
Exemplos fictícios, os mesmos em todo o deck: <nomes, números, data>.

## 2. Paleta por papel (tokens de <arquivo do tema>)
| Papel | Hex | Uso |
|---|---|---|
| fundo | | slide e página da cena |
| card / painel | | |
| borda fina | | |
| tinta | | títulos, texto forte, voz (serifa) |
| texto secundário | | corpo, legendas (contraste ≥ 4,5:1 no fundo) |
| acento | | a escolha/ação principal; como texto: <variante escura> |
| recusa | | só com a palavra |
`deck.config.json`: `backgrounds` = [fundo]; `bannedColors` = cores que não podem aparecer.

## 3. Tipos
Faces do slide (Google Fonts, `deck.json` → `faces`): <display>, <texto>, <mono>.
Escala única: 128 (capa/fecho) · 80 (título) · 44 (destaque) · 32 (lede) · 24 (rótulo). Nada menor que 24.
Dentro da cena: fontes do sistema (runtime.md).

## 4. Moldes
STAGE (slide de conteúdo — o título nunca pula de lugar):
<section id="ID" data-transition="fade" style="background:<fundo>; color:<tinta>; font-family:'<texto>', Helvetica, Arial, sans-serif; padding:128px; display:flex; flex-direction:column; gap:20px">
  <x-embed style="position:absolute; left:128px; top:400px; width:1664px; height:552px">…cena…</x-embed>
  <p style="font-family:'<mono>', 'Courier New', monospace; font-size:24px; letter-spacing:4px; text-transform:uppercase; color:<secundário>"><span style="color:<acento-texto>">NN</span> · RÓTULO</p>
  <h2 style="font-family:'<display>', Georgia, serif; font-size:80px; font-weight:400; line-height:1.05; letter-spacing:-1px; color:<tinta>">Título</h2>
  <p style="font-size:32px; line-height:1.4; color:<secundário>; width:1280px">Lede de até duas linhas.</p>
</section>
(cena listada primeiro, caixa 128/400/1664×552; título ≤ ~40 caracteres; lede ≤ ~140.)
STATEMENT (capa, fecho): cena de página inteira (0/0/1920×1080) primeiro, texto por cima,
`justify-content:center`.
Futuro/proposta: o rótulo do eyebrow ganha "· PROPOSTA".

## 5. Movimento
Kit, contrato, ritmo e cor por papel: motion-kit.md. Deste deck: <ritmo escolhido no grilling>;
movimento ambiente só em <capa, fecho>; o que cada cena repousa mostrando está no brief (§7).

## 6. Fatos (só estes; cada um com fonte)
- <fato> — <arquivo:linha / doc / métrica>

## 7. Slides (id · molde · brief)
NN **<id>** — <molde>. Eyebrow "NN · …". Título "…". Lede "…".
CENA: <beats, na ordem: o que entra, o que se move, o que é lido, onde repousa (o pôster)>.
```
