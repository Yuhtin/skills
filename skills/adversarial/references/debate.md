# Modo DEBATE — ideias concorrentes que se atacam

Entrada: uma pergunta em aberto, nada escrito ainda.
Saída: as 2-3 abordagens que sobreviveram, e o experimento mais barato que
decide entre elas.

## 1. Enquadrar — antes de lançar qualquer agente

Escreva e confirme com o usuário:

- **A pergunta, falsificável.** "Como fazer o billing" não é enquadramento.
  "Como cobrar assinatura mensal com trial de 14 dias, cancelamento no meio do
  ciclo e reembolso proporcional" é.
- **As restrições duras** — o que é inegociável: stack, prazo, regulatório, o que
  já está em produção. Restrição inventada mata a proposta boa; restrição omitida
  gera proposta impossível.
- **O critério de sucesso** — como saber, daqui a seis meses, que a escolha foi
  certa.

Enquadramento ruim é a causa número um de debate inútil. Se você não consegue
escrever a pergunta falsificável, **esse** é o trabalho — não lance agentes ainda.

## 2. Propostas isoladas

3 a 6 agentes. Cada um recebe **uma postura** e propõe **uma** solução, **sem ver
as dos outros**.

Postura não é a persona-vítima do modo REVIEW. É uma escola de pensamento, e
precisa ser genuinamente incompatível com as outras:

| Postura | Otimiza | Sempre pergunta |
|---|---|---|
| O minimalista | Menos peças | "E se simplesmente não fizermos isso?" |
| Quem mantém há 3 anos | Custo de operação | "Quem acorda quando isso quebra?" |
| Quem otimiza reversibilidade | Custo de estar errado | "Como desfaço na segunda-feira?" |
| Quem otimiza time-to-market | Tempo até o primeiro usuário | "O que entrega valor esta semana?" |
| Quem já viu isso falhar | Modos de falha conhecidos | "Onde isso deu errado da última vez?" |
| O purista do domínio | Corretude do modelo | "Isso mente sobre o negócio?" |

Escolha as posturas que **este** problema torna incompatíveis. Se duas
produziriam a mesma proposta aqui, troque uma — a tabela é ponto de partida, não
catálogo a preencher.

```
Você vai PROPOR uma solução. Não revise nada; não existe artefato ainda.

PROBLEMA: [a pergunta falsificável]
RESTRIÇÕES DURAS: [inegociáveis]
SUCESSO: [o critério, em uma frase]
SUA POSTURA: [uma frase — o que você otimiza acima de tudo]

Proponha UMA solução, a que a sua postura recomenda. Comprometa-se com ela.
Nada de "depende" nem de menu de opções.

Entregue:
1. A abordagem, em um parágrafo que um dev consiga executar
2. O mecanismo concreto da parte mais difícil — não o nome do padrão
3. O que ela CUSTA (o que você está sacrificando por ela — nomeie)
4. O que ela ASSUME sobre o mundo, e como conferir cada premissa
5. O ataque mais forte que você prevê contra ela, e sua resposta

Se algo é verificável agora — no repositório, na doc oficial, rodando — verifique
e cite. Proposta apoiada em premissa não conferida é proposta fraca.
```

## 3. Rodada de ataque

Cada agente recebe as propostas dos outros e dois mandatos:

1. **Matar cada uma das outras** — a entrada concreta que quebra, o custo
   escondido, o que ela vira em seis meses.
2. **Defender a sua** contra o ataque que ele mesmo previu.

Ataque sem mecanismo não conta. "Não escala" é ruído; "não escala porque cada
renovação faz um round-trip por item da assinatura" é achado.

**Anti-consenso:** se todas as propostas convergirem na rodada 1, o problema
estava mal enquadrado — a pergunta já continha a resposta. Reenquadre e relance.
Não celebre a concordância.

Uma rodada basta. Faça a segunda só se a primeira revelou uma restrição que
ninguém sabia.

## 4. Síntese cética

Um agente que **não propôs nada** lê tudo e devolve:

- **O que sobreviveu**, e o ataque mais forte que cada sobrevivente aguentou
- **O que morreu**, e o mecanismo exato que matou — não "foi rejeitada"
- **Onde concordaram sem perceber** — a premissa que todas as propostas
  compartilham e ninguém questionou. É o ponto mais perigoso do debate inteiro,
  porque nenhum agente tinha incentivo para atacá-lo.
- **A decisão real** que separa as sobreviventes. Quase sempre é uma só, e quase
  nunca é aquela que o debate parecia ser sobre.
- **O experimento mais barato** que resolve essa decisão: o spike de duas horas,
  a query no banco de produção, a pergunta para o cliente.

## 5. Entregar

2-3 abordagens vivas, cada uma com o que custa, o que assume, e o que a mataria.
Sua recomendação primeiro, com o motivo.

Não escolha em silêncio. Mas se a sobrevivente for única e óbvia, diga que é
óbvia e por quê, e siga — debate empatado artificialmente gasta a atenção do
usuário à toa.

Escolhida uma abordagem, o passo seguinte natural é modo REVIEW sobre o plano
que sair dela.
