---
name: adversarial
description: >
  Use quando existir algo para atacar antes de se comprometer com ele: plano
  escrito antes de executar, spec fechada antes de virar plano, feature pronta
  para merge, diff, refactor que toca lógica de negócio. Use também quando a
  pergunta ainda está em aberto e nada foi escrito, quando há duas ou mais
  opções na mesa esperando escolha, quando o autor já revisou o próprio
  trabalho e isso não bastou, ou quando a decisão é cara de reverter.
  Triggers: "adversarial", "adversarial review", "revisar plano", "revisar
  spec", "revisar implementação", "review adversarial", "ataca essa ideia",
  "debate isso", "me ajuda a decidir entre", /adversarial
---

# Adversarial

Agentes em paralelo com mandato de **encontrar falhas**, nunca de validar.
Três modos, um núcleo.

## Fase 0 — Modo

| O que existe agora | Modo | Leia |
|---|---|---|
| Artefato pronto: código, diff, spec, plano | REVIEW | `references/review.md` |
| Pergunta em aberto, nada escrito ainda | DEBATE | `references/debate.md` |
| 2+ opções já nomeadas, falta escolher | DECIDE | `references/decide.md` |

Confirme em uma linha antes de gastar agente — *"Modo REVIEW sobre
`docs/plan.md`, 7 personas. Vou?"* — e espere o ok.

Ambíguo de verdade (existe um rascunho, mas a pergunta ainda está aberta):
pergunte qual modo, com uma frase do que cada um faria **neste** alvo. Nunca
rode dois modos "por garantia".

**Não rode nada disto** em: bugfix de 1-2 linhas, estilo, typo, doc.

## Núcleo — vale nos três modos

1. **Postura derivada do alvo, nunca de catálogo.** Lista fixa de dimensões faz
   todo agente olhar com o mesmo olho, e o lote inteiro devolve a mesma coisa.
   Cada modo tem seu método de derivar — está no arquivo do modo.
2. **Evidência ou silêncio.** Toda afirmação carrega `file:line` lido nesta
   sessão, ou um fato do mundo que o agente mesmo produziu. Fato descobrível —
   no filesystem, na doc oficial, rodando alguma coisa — é descoberto, nunca
   reportado como "não está claro se X".
3. **Quem verifica tem mandato de refutar.** Achado é hipótese gerada sob
   pressão de achar algo. Na dúvida, refuta. Sobrevive só o que tem entrada
   concreta que quebra.
4. **Saída em três baldes, nunca misturados:** o que eu corrijo · o que você
   decide · o que não se sustentou. O terceiro fica registrado, nunca apagado —
   é o que impede o achado morto de voltar na próxima rodada.
5. **Convergência é sinal.** Mesma conclusão por caminhos independentes é causa
   raiz, não coincidência: conserte ali e vários achados somem juntos.

## Lançamento

Todos os agentes numa única mensagem, com nome descritivo cada um
(`adv-authz`, `adv-minimalista`, `adv-steelman-B`).

Se o usuário pediu um número de agentes, respeite o número dele.

**Agente que altera o repositório** — teste de mutação, migration de teste,
`git stash`, arquivo de rascunho — recebe `isolation: "worktree"`. Sem isso ele
suja a árvore que os outros estão lendo, e alguém reporta como achado a sujeira
que não é dele.

**Confira o estado final com git de verdade:** `/usr/bin/git status --porcelain`.
Wrapper que filtra saída (o `rtk`) já reportou "clean" sobre árvore suja.

## Regras que o alvo não te conta

- **Autor não enxerga o próprio erro.** Self-review não substitui isto, e
  correção aplicada pelo autor é alvo — não terreno já conferido.
- **Verifique empiricamente quando der.** Instale o pacote e rode. Suba o banco
  e meça. Olhe o EXPLAIN. Cite versão e data. Doc descreve intenção;
  comportamento só a execução mostra.
- **Truthy engana.** Função que passou a devolver objeto (`{valid:false}`)
  continua passando em `if (verify())`.
- **Zero falso positivo significa verificação frouxa**, não lote perfeito.

---

Escolhido o modo, leia `references/<modo>.md` **agora** e siga de lá.
