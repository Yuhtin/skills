---
name: pr-review
description: >
  Use para revisar um pull request de ponta a ponta. Estuda o PR, monta um plano
  de revisão (escolhe as skills pelo risco do que ele toca) e executa sem pedir
  aprovação, tudo no próprio contexto. Vê cada tela mudada, comenta no PR e, no
  fim, pergunta se aplica as mudanças sugeridas ou se o comentário basta.
  Triggers: "revisa esse PR", "review do #123", "dá uma olhada nesse PR",
  "pr review", /pr-review
---

# PR review

Uma revisão tem um **objetivo** próprio por PR: o que precisa ser verdade para você dizer "pronto para merge". Você escreve esse objetivo antes de ler o diff a fundo e o persegue até o fim. O plano é auto-aprovado: ele organiza o seu trabalho, não espera ninguém.

A revisão inteira roda **no seu contexto, uma lente depois da outra**. Você lê, roda e conclui cada lente você mesmo: subagente e workflow gastam token sem melhorar a revisão.

## 1. Estudar (rápido)

Leia o PR por cima, sem revisar ainda:

- `gh pr view <n> --json title,author,body,comments,reviews,statusCheckRollup,mergeable,mergeStateStatus,additions,deletions,changedFiles`
- `gh api --paginate repos/<owner>/<repo>/pulls/<n>/files` dividido por tipo: código de tela, código de pacotes, testes, migrações, docs/specs, mockups, gerados/lock, fixtures.
- O que ele **toca**: telas e rotas, jobs, migrações, permissões, integrações, dinheiro, nota fiscal, dado pessoal ou de saúde, envio para fora (WhatsApp, e-mail, webhook).

**Pronto quando** você consegue dizer em duas frases do que o PR trata e tem a lista do que ele toca, separando o escopo declarado do que veio junto.

## 2. Planejar

Escreva o plano numa nota curta, com:

1. **Objetivo:** as 3 a 6 afirmações que têm de ser verdade para o PR estar pronto. Exemplos: "nenhum documento de uma paciente chega à conversa de outra", "as outras cidades emitem igual antes".
2. **Alertas de cara**, que já entram na revisão sem precisar de skill:
   - **Mais de um problema no PR.** Um PR deve resolver um problema nomeado e dar para revisar lendo. Quando há várias entregas, proponha a divisão: qual sai primeiro e o que fica para os PRs seguintes.
   - Mockups, prints ou artifacts commitados.
   - Conflito com a main.
   - Número de migração que colide com a main.
   - CI que não rodou de verdade (só checks pulados).
   - PR empilhado que leva outro PR junto.
3. **As lentes:** uma skill por risco presente, tirada do catálogo abaixo. Use só as que o PR pede.

**Pronto quando** cada afirmação do objetivo tem a lente que vai verificá-la, e você conferiu que cada skill escolhida está instalada (veja "Quando falta uma skill").

## 3. Executar

- Rode cada lente do plano sobre o diff, uma de cada vez.
- **Veja cada tela mudada:** suba o app local com dados de demonstração, pela skill ou pelo comando de desenvolvimento do repositório. Tire prints de cada tela e estado tocados, em desktop e em 390 px. Nada em produção. Se a máquina estiver sem memória, pare só servidores de desenvolvimento ociosos e desligue tudo ao terminar.
- **Confira as afirmações do corpo do PR:** o teste citado existe e cobre o que diz, a permissão é checada no servidor, a migração é aditiva.
- Classifique cada achado em **bloqueia**, **deve mudar** ou **detalhe**. Cada um leva `arquivo:linha`, o porquê e uma correção concreta.

**Pronto quando** cada afirmação do objetivo tem um veredito (vale, não vale ou não deu para checar, com o motivo) e cada tela tocada tem print.

## 4. Comentar no PR

Poste uma revisão de comentário: `gh pr review <n> --comment --body-file <arquivo>`. Aprovar ou pedir mudanças só quando o dono do repositório pedir. Escreva no idioma e no tom do repositório:

1. Uma ou duas frases de elogio concreto (o que o PR acertou).
2. **Bloqueia**, **Deve mudar** e **Detalhes**, com `arquivo:linha` e a correção.
3. Os alertas do passo 2 que se confirmaram, como "quebrar em PRs" ou "tirar os mockups".
4. As perguntas que só o autor responde.

Os prints ficam com quem pediu a revisão; cite no comentário o que foi visto.

## 5. Fechar com quem pediu

Responda com o resumo, o link do comentário e uma pergunta com recomendação: **"Aplico as mudanças sugeridas ou o comentário basta?"** As opções:

- aplicar no próprio PR, em commits na branch dele;
- aplicar num PR separado;
- só o comentário.

Recomende a primeira quando as mudanças são pequenas e o autor está ausente; a última, quando o autor está ativo. Aplicando, faça uma mudança por commit, rode os testes afetados e faça push. O merge é sempre de quem pediu.

## Catálogo de lentes

Prefira as skills do próprio repositório (`.claude/skills`, `.agents/skills`, `.claude/rules`) às globais quando as duas cobrirem o mesmo assunto.

| Se o PR toca… | Lente | De onde vem |
|---|---|---|
| qualquer código | `code-review` (padrões do repo e aderência à spec/issue) | mattpocock/skills |
| conserto de bug | `diagnosing-bugs` (o bug se reproduz antes e some depois?) | mattpocock/skills |
| testes novos ou o PR alega cobertura | `tdd` (o teste falha sem a mudança?) | mattpocock/skills |
| módulos, fronteiras, nomes de domínio | `codebase-design` e `domain-modeling` | mattpocock/skills |
| conflito com a main | `resolving-merge-conflicts` | mattpocock/skills |
| `AGENTS.md`, `CLAUDE.md` ou skills | `writing-for-agents` | mattpocock/skills |
| permissão, dado pessoal, envio para fora, rota nova, upload ou arquivo | `security-review`, focada no fluxo do PR | yuhtin/skills |
| rota pesada, imagem, cache, query, bundle, renders | `optimize-app` | yuhtin/skills |
| agente de IA, prompt, tools | `eval-guidelines` e `guardrail-guidelines` | yuhtin/skills |
| uma skill nova ou alterada | `skill-eval-guidelines` | yuhtin/skills |
| tela, componente, texto de interface | `emil-design-eng` | emilkowalski/skills |
| formulário, lista, estado vazio, dado longo | `break-ui` | emilkowalski/skills |
| gesto, arrastar, zoom, folha/sheet | `apple-design` e `gestures` | emilkowalski/skills |
| animação ou transição | `review-animations` e `animation-performance` | emilkowalski/skills |
| layout no celular | `mobile-native` | emilkowalski/skills |
| interface com cara de gerada por IA | `unslop-ui` | felipebasurto/unslop-ui |
| crítica de design e acessibilidade | `design:design-critique` e `design:accessibility-review` | plugin `design` da Anthropic, no Claude Code |
| subir e fotografar | a skill local do repositório (dev, QA ou equivalente) | o próprio repositório |

### Quando falta uma skill

Antes de executar, confira que cada lente escolhida está disponível: ela aparece na lista de skills da sessão ou existe em `~/.claude/skills/`, `~/.agents/skills/` ou nas pastas de skills do repositório. Para cada uma que falta, diga a quem pediu a revisão qual é, para que serve neste PR e o comando que instala:

```bash
npx skills@latest add mattpocock/skills
npx skills@latest add emilkowalski/skills
npx skills@latest add yuhtin/skills
npx skills@latest add felipebasurto/unslop-ui
```

O plugin `design` se instala pelo `/plugin` do Claude Code.

Siga a revisão com as lentes disponíveis. A que falta entra no comentário como "não revisado por falta da skill X", e não vira um palpite com o nome dela.
