# Modelo do prompt de saída

Preencha todo `{{…}}` e entregue o bloco abaixo inteiro. Tudo que está fora de `{{}}` fica como está.
O chat novo grava a parte "Brief" como `ROOT/DESIGN.md` — os números de seção (§1–§7) são os que os
prompts dos agentes citam; mantenha-os.

````markdown
Use a skill `animated-deck` e siga `references/build.md` dela para construir este deck
(se não estiver instalada: https://github.com/yuhtin/skills → skills/animated-deck).
O brief abaixo está fechado com o dono; não reabra decisões dele.

# Brief — {{título do deck}}

Plateia: {{quem assiste e o que já sabe}}. Ocasião: {{ao vivo / vídeo / PDF}}, {{data}}.
Idioma: {{idioma}}. Duração da fala: {{min}}. Mensagem que fica: "{{uma frase}}".
Projeto de origem: {{caminho do repo / URL}}. Saídas: {{deck Artifact · MP4 em <caminho> · HTML}}.

## deck.config
```json
{
  "title": "{{título}}",
  "fontsHref": "{{URL css2 do Google Fonts com as 2–3 famílias}}",
  "backgrounds": ["{{hex do fundo}}"],
  "bannedColors": [{{hex que não podem aparecer, ou vazio}}],
  "bannedRgb": [],
  "minFontPx": 24,
  "holdMs": 2500,
  "ambientMs": { "{{id da capa}}": 8000 },
  "ambientTailMs": { "{{id do fecho}}": 4000 },
  "chrome": "{{caminho do Chrome, ou vazio}}",
  "puppeteer": "{{caminho de um puppeteer existente, ou vazio}}"
}
```

## 1. Palavras
| Diga | Nunca diga |
|---|---|
{{uma linha por termo: palavra do dia a dia | jargão que ela substitui}}
Tom: {{tom}}. Títulos apresentam o slide, sem drama.
Exemplos fictícios, os mesmos em todo o deck: {{nomes, números, data de exemplo}}.

## 2. Paleta por papel (fonte: {{arquivo dos tokens}})
| Papel | Hex |
|---|---|
| fundo (slide e página da cena) | {{hex}} |
| card / painel | {{hex}} |
| borda fina | {{hex}} |
| tinta (títulos, voz em serifa) | {{hex}} |
| texto secundário (≥ 4,5:1 no fundo) | {{hex}} |
| acento — {{o que ele significa na história}} | {{hex}} · como texto {{hex}} |
| recusa (só com a palavra) | {{hex}} |

## 3. Tipos
Display {{família}}, texto {{família}}, mono {{família}}. Escala: 128 · 80 · 44 · 32 · 24.
Motivo visual da marca para a capa: {{ex.: anel granulado da landing, padrão do logo}}.

## 4. Moldes
STAGE (conteúdo): cena em 128/400/1664×552, eyebrow "NN · RÓTULO", título 80, lede 32.
STATEMENT (capa e fecho): cena de página inteira atrás do texto. Futuro/proposta: eyebrow com "· PROPOSTA".

## 5. Movimento
Cada cena toca uma vez e repousa no pôster. Ritmo: {{médio (650 ms + 200 ms/palavra) | lento (900 + 280)}}.
Movimento ambiente só em: {{capa, fecho}}.

## 6. Fatos (só estes)
{{uma linha por fato: fato — fonte (arquivo:linha / doc / métrica)}}

## 7. Slides
{{para cada slide, na ordem:
NN **id** — STAGE|STATEMENT. Eyebrow "NN · …". Título "…" (≤ 40 caracteres). Lede "…" (≤ 140).
CENA: beats em ordem — o que entra, o que se move, o que é lido, onde repousa.}}
````
