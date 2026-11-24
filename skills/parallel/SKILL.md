---
name: parallel
description: >
  Use quando o usuário tem várias coisas para fazer (as issues de um milestone,
  os entregáveis de uma meta, uma lista solta de tarefas) e quer saber quais
  podem rodar ao mesmo tempo, em chats, worktrees ou sessões separadas, sem uma
  pisar na outra. Lê o que cada item vai tocar no código, acha as colisões e as
  dependências, agrupa em levas que rodam juntas e entrega um prompt pronto por
  item. Use também quando ele perguntar "o que dá pra paralelizar", "o que roda
  junto", "quais dessas não dependem uma da outra", ou quiser soltar vários
  agentes de uma vez. Triggers: "paraleliza", "o que roda em paralelo", "monta as
  levas", "divide entre agentes", "quais posso fazer ao mesmo tempo", /parallel
---

# Parallel

Os itens a dividir são o argumento da invocação: um milestone, uma lista de
issues, uma meta já quebrada em entregáveis. Sem argumento, são os entregáveis
da conversa atual. Se o argumento é uma meta ainda não quebrada, quebre primeiro
em entregáveis que caibam numa frase cada e confirme a lista com o usuário em uma
mensagem antes de seguir.

O objetivo não é rodar o máximo possível ao mesmo tempo. É rodar junto só o que
não vai colidir, porque uma colisão custa mais que a espera: dois PRs que mexem no
mesmo lugar viram conflito, retrabalho e uma revisão a mais.

## 1. Descubra o que cada item toca

Para cada item, leia a issue e depois o código, nunca só o título. Um título como
"filtro na lista de pacientes" não diz se vai precisar de coluna nova. Anote:

- **Arquivos e módulos** que ele vai escrever (não os que só lê).
- **Banco:** tabela, coluna ou migração nova. Duas migrações em paralelo disputam
  o número da sequência mesmo em tabelas diferentes.
- **Contratos compartilhados:** um tipo, schema, rota de API, componente do kit,
  enum ou config que outro item também usa.
- **Arquivos gerados ou centrais:** lockfile, mapas e índices gerados, rotas
  registradas num arquivo só, traduções, snapshots.
- **Resultado que outro item precisa:** o item B lê a tabela, a função ou a tela
  que o item A cria.

Quando não der para saber sem começar a implementar, escreva "incerto" e diga o
que falta saber. Não chute.

## 2. Ache as colisões

Dois itens **colidem** quando escrevem o mesmo arquivo, a mesma tabela, o mesmo
contrato ou o mesmo arquivo central, ou quando os dois criam migração. Um item
**depende** de outro quando precisa do resultado dele para começar.

Ler o mesmo arquivo não é colisão. Mexer em pontas diferentes de um arquivo
grande é colisão mesmo assim: o merge pode passar e o comportamento quebrar.

Na dúvida, trate como colisão. Esperar uma leva custa pouco; desfazer um conflito
entre dois PRs prontos custa caro.

## 3. Monte as levas

- **Leva 1:** os itens que não dependem de nada e não colidem entre si.
- **Leva seguinte:** o que dependia da anterior, ou colidia com algo dela.
- Itens que colidem ficam em levas diferentes, o menor e mais fundacional antes.
- Prefira três levas folgadas a uma leva lotada: cada item a mais na mesma leva é
  um PR a mais para revisar no mesmo dia.

Se uma leva inteira depende de uma decisão do usuário (produto, gasto, desenho),
diga qual decisão e deixe a leva parada até ele responder.

## 4. Entregue

Uma tabela por leva:

| Item | Toca | Por que roda junto (ou espera) |
|---|---|---|

Uma linha por item, e o porquê em uma frase: "só mexe na tela de agenda e não cria
migração", "espera a leva 1 porque lê a coluna que o NIM-12 cria".

Depois, um prompt por item da leva 1, pronto para colar numa sessão nova, com:

- a meta do item numa frase e como saber que terminou;
- onde começar (arquivos, issue, desenho aprovado se houver);
- o que **não** tocar, porque outro item da mesma leva está mexendo ali;
- quando parar e perguntar (gasto, produção, decisão de produto);
- abrir um PR próprio, pequeno, que resolve só esse item.

O prompt dá a meta e os limites, não um plano em passos: o agente que implementa
lê o código no momento e decide o caminho. Um plano escrito antes envelhece assim
que a leva anterior entra.

## 5. Rodar (só se o usuário pedir)

Por padrão, entregue as levas e os prompts e pare. Se o usuário pedir para soltar:

- **Na mesma máquina:** um git worktree por item (`git worktree add`), uma sessão
  em cada. Duas sessões no mesmo checkout se atropelam mesmo em arquivos
  diferentes.
- **Com subagentes disponíveis:** um subagente por item, com isolamento de
  worktree quando a ferramenta oferecer.
- **Com o computador desligado:** uma sessão do Claude Code na nuvem
  (claude.ai/code) por item.

Ao fim de cada leva, confira se os PRs dela entraram e se algum mudou o que a
próxima leva assumia; refaça a próxima se mudou.
