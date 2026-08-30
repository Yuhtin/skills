# Modo DECIDE — steelman cruzado

Entrada: 2+ opções já nomeadas.
Saída: recomendação · o que a mudaria · custo de reverter.

Se as opções ainda precisam ser inventadas, o modo é DEBATE, não este.

## 1. Fixar as opções

Escreva cada opção em uma frase e confirme com o usuário antes de lançar.
Opção mal enunciada gera steelman da opção errada, e o erro só aparece no fim.

Se "não fazer nada" é possível, ela **entra como opção**, com agente e tudo. É a
que mais ganha com steelman e a que menos costuma receber.

## 2. Steelman — um agente por opção

Mandato: **construa a melhor versão possível desta opção.**

```
Você vai defender UMA opção. Seu mandato é construir a versão mais forte dela.

DECISÃO: [a escolha, em uma frase]
SUA OPÇÃO: [uma só]
CONTEXTO: [restrições, o que já existe, prazo]

1. Apresente a opção na sua forma mais forte. Fraqueza óbvia você CONSERTA em
   vez de admitir — se ela tem um jeito melhor de ser feita, é esse o jeito que
   você apresenta.
2. Nomeie o mundo em que ela é claramente a escolha certa.
3. Nomeie a única coisa que precisaria ser verdade para ela ganhar.
4. Cite evidência concreta: custo, prazo, file:line do que já existe e favorece
   essa opção.

PROIBIDO comparar com as outras opções. Comparação aqui produz defesa morna;
quem compara é o juiz, depois, com os dois lados na mão.
```

## 3. Ataque — um agente por opção

Mandato: **mate esta opção.** Agente diferente do que fez o steelman dela.

```
Você vai matar UMA opção. Seu mandato é encontrar o que a inviabiliza.

DECISÃO: [a escolha]
OPÇÃO A MATAR: [uma só]

1. A entrada concreta, o volume ou o caso de borda que a quebra. Mecanismo, não
   desconforto.
2. O custo escondido: operação, migração, contratação, licença, treinamento — o
   que ninguém coloca na planilha.
3. O que ela vira em 6 meses e em 2 anos.
4. A saída de emergência: se der errado, quanto custa sair? Existe saída?

Verifique empiricamente o que der para verificar. "Eu acho que fica lento" não é
ataque; a medição é.
```

Steelman e ataque podem rodar em paralelo, desde que cada agente veja só a opção
dele.

## 4. Juízo

Um agente que não escreveu steelman nem ataque recebe os dois lados de cada
opção. Ele é **obrigado a nomear três coisas**:

1. **O critério que decidiu**, em uma frase. Se ele não consegue nomear um
   critério, a decisão é indiferente — diga isso ao usuário. Opções equivalentes
   se resolvem tirando par ou ímpar, não com mais uma rodada de análise.
2. **O que mudaria a decisão** — o fato que, se fosse outro, viraria o veredicto.
   É isso que o usuário vai monitorar depois.
3. **O custo de estar errado**, por opção, e o custo de reverter.

**Reversibilidade pesa mais que qualidade.** Entre uma opção melhor e
irreversível e uma pior e barata de desfazer, a segunda ganha por padrão. O juiz
pode decidir contra esse padrão, mas precisa dizer que decidiu e por quê.

## 5. Entregar

| Opção | Ganha quando | Morre com | Custo de reverter |
|---|---|---|---|

Sem suspense: **recomendação primeiro, motivo depois**, e em seguida a linha
*"isto muda se ___"*.

Decisão cuja alternativa não se sustenta não é decisão: escolha, diga que
escolheu e por quê, e siga.
