# skills

Agent skills I use daily. Installable in Claude Code, Codex, Cursor, and any
runtime that reads `SKILL.md` directories.

> Skill content is written in **Portuguese**. The structure is runtime-agnostic;
> the prompts are not translated.

## Install

**Any agent** — via the [`skills`](https://github.com/vercel-labs/skills) CLI:

```bash
npx skills add yuhtin/skills                      # pick interactively
npx skills add yuhtin/skills -a claude-code -a codex -g
```

`-g` installs globally (`~/.claude/skills/`, `~/.codex/skills/`); without it,
the skill lands in the current project.

**Claude Code** — natively, with updates:

```
/plugin marketplace add yuhtin/skills
/plugin install adversarial@yuhtin
```

**Manually** — symlink, so `git pull` updates the skill in place:

```bash
git clone https://github.com/yuhtin/skills ~/src/skills
ln -s ~/src/skills/skills/adversarial ~/.agents/skills/adversarial
```

`~/.agents/skills/` is the cross-runtime directory read by Codex, Copilot CLI,
and Gemini CLI. Claude Code reads `~/.claude/skills/` instead.

## Skills

### `adversarial`

Parallel agents whose mandate is to **find flaws**, never to validate. Three
modes, one core.

| Situation | Mode | What runs |
|---|---|---|
| A finished artifact: code, diff, spec, plan | `REVIEW` | Personas derived from the artifact — each one is whoever gets hurt if a given part is wrong — attack it, then two skeptical verifiers try to refute every finding: one against the artifact, one against the real world (installing the package, booting the database, reading current docs). |
| An open question, nothing written yet | `DEBATE` | 3-6 agents with genuinely incompatible stances propose in isolation, then attack each other's proposals. A judge who proposed nothing reports what survived, what the killing mechanism was, and which premise every proposal shared without noticing. |
| Two or more named options | `DECIDE` | One agent steelmans each option (forbidden from comparing), another kills each one, and a third judge names the deciding criterion, what would flip it, and the cost of reverting. |

Output separates **defects** (fixed) from **decisions** (asked, one at a time)
from **investigated false positives** (recorded, never deleted — that is what
stops a dead finding from coming back next round).

The mode is inferred from what you ask and confirmed in one line before any
agent is spawned.

```
/adversarial revisa esse plano
/adversarial como estruturar o billing
/adversarial postgres ou sqlite pra isso
```

**Do not run it on** 1-2 line bugfixes, style, typos, or docs.

## License

MIT
