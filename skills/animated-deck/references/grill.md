# Árvore do grilling — o que fechar antes de desenhar

Uma pergunta por vez, na ordem abaixo (cada uma destrava as seguintes). Cada pergunta preenche
placeholders de `prompt-template.md` e chega com a **resposta recomendada** tirada do research da
Fase 1; espere a resposta. O que está marcado **[descubra]** você procura no ambiente e só
confirma em uma linha — nunca vira pergunta aberta.

## 1. Plateia e ocasião
- Quem assiste (equipe técnica, liderança, cliente, investidor, time misto) e o que já sabe.
- Como vai ser visto: apresentado ao vivo, enviado como vídeo, lido sozinho em PDF. Muda tudo:
  ao vivo o apresentador fala por cima da cena; vídeo/PDF, a cena e o texto têm que se explicar.
- Quando é, e quanto tempo de fala. **Recomende** 12–18 slides para ~15 min.

## 2. A mensagem
- A frase que a plateia leva embora. Se o usuário não tiver, proponha uma — ela vira o último slide.

## 3. O roteiro
- Os tópicos que o usuário listou → proponha a sequência de títulos (uma ideia por slide, na
  gramática de tópico curto) e peça cortes/acréscimos. Esse é o §7 do `DESIGN.md` só com títulos.
- Em cada tópico técnico, o *caminho* que a plateia deve ver (ex.: "da pergunta à resposta").

## 4. Fontes da verdade [descubra]
- Onde moram os fatos: código, docs, ADRs, métricas, dashboards. Leia; pergunte só qual vale
  quando duas fontes divergem.
- O que é **presente** e o que é **proposta/futuro** — tudo que ainda não existe ganha rótulo no slide.

## 5. Linguagem
- Idioma, nível de jargão (**recomende** "sem jargão": termos do produto sim, termos de engenharia
  traduzidos em palavras do dia a dia), e a tabela "diga / nunca diga" (§1 do `DESIGN.md`).
- Nomes e dados de exemplo: fictícios e consistentes no deck inteiro (mesma pessoa, mesmo número,
  mesma data em todos os slides). Nunca dado real de pessoa.

## 6. Identidade visual [descubra primeiro]
- Leia os tokens da marca: tema CSS / Tailwind / design system do projeto, landing page, favicon,
  logo, fontes. Mostre o que achou (fundo, tinta, acento, fontes) e **recomende**: fundo e cores da
  marca, **um** acento, fundo claro se a marca é clara (slide escuro numa marca clara parece de outra
  empresa).
- Um motivo visual da marca que a capa possa usar (um anel, uma textura, um padrão da landing).
  Peça um print/URL da landing se não achar no repo.
- Quando a regra de design do projeto e o gosto das skills de design divergirem em algo que muda o
  sistema (paleta, escala, densidade), mostre as duas versões lado a lado e deixe o usuário decidir.

## 7. Movimento
- **Recomende** o padrão: cada cena toca uma vez e repousa no estado final (só recomeça ao voltar
  ao slide); ritmo de leitura médio (`motion-kit.md` § Ritmo); capa e fim podem ter um movimento
  ambiente contínuo e calmo.
- Acessibilidade: movimento reduzido mostra o pôster.

## 8. Saídas
- Deck (Artifact de slides — padrão quando a ferramenta existe), MP4, HTML standalone, PDF.
  **Recomende** oferecer o MP4 no fim mesmo se não pedido.
- Onde salvar o MP4 (padrão `~/Downloads/<slug>.mp4`).

## 9. Cenas
Para cada slide do roteiro, proponha a cena em beats (o que entra, o que se move, onde repousa) com
uma metáfora de `motion-kit.md` § A régua de criatividade, e peça ok ou ajuste — um slide por vez.

## Fechamento
Mostre o brief inteiro preenchido e pergunte se fechou. Só gere o prompt com o "sim".
