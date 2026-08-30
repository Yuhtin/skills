# Skills I Actually Use

Agent skills for Claude Code, Codex, Cursor, and anything else that reads
`SKILL.md`. Small set, kept because they earn their place — not a catalogue.

> **Heads up:** the skills are written in **Portuguese**. The structure is
> runtime-agnostic; the prompts are not translated.

## Installation (30-second setup)

Two ways in, two philosophies. **The Claude Code plugin** installs the set as a
managed bundle that updates when I ship, so you subscribe rather than fork.
**The [`skills` CLI](https://github.com/vercel-labs/skills)** copies editable
files into your project or home directory, so you can hack on them and make them
your own. Pick one — installing both leaves you with every skill twice.

<details>
<summary><strong>Claude Code</strong></summary>

From inside a session:

```
/plugin marketplace add yuhtin/skills
```

```
/plugin install adversarial@yuhtin
```

The marketplace only has to be added once; after that, new skills I publish show
up in `/plugin` and updates arrive with them.

</details>

<details>
<summary><strong>Codex</strong></summary>

```bash
npx skills@latest add yuhtin/skills -a codex -g
```

`-g` installs to `~/.codex/skills/`. Drop it to install into the current project
instead.

</details>

<details>
<summary><strong>Cursor, Copilot CLI, Gemini CLI</strong></summary>

```bash
npx skills@latest add yuhtin/skills -a cursor -g
```

Swap `-a cursor` for your agent, or pass several at once:
`-a claude-code -a codex -a cursor`. Run it with no `-a` flag to pick
interactively.

</details>

<details>
<summary><strong>Manually, with updates</strong></summary>

Symlink instead of copy, so `git pull` updates the skill in place:

```bash
git clone https://github.com/yuhtin/skills ~/src/skills
ln -s ~/src/skills/skills/adversarial ~/.agents/skills/adversarial
```

`~/.agents/skills/` is the cross-runtime directory read by Codex, Copilot CLI,
and Gemini CLI. Claude Code reads `~/.claude/skills/` instead.

</details>

## Why These Skills Exist

Because the author of a thing cannot see what is wrong with it. Self-review
finds typos and misses the migration that drops a column. The way around that is
not more care — it is a second reader with no stake in the thing being right.

These skills buy that reader, several of them, in parallel, and then make them
argue.

## Reference

- **[adversarial](./skills/adversarial/SKILL.md)**: Parallel agents mandated to
  find flaws, never to validate. Picks one of three modes from what you ask and
  confirms it in one line before spawning anything.

  | You have | Mode | What happens |
  |---|---|---|
  | A finished artifact — code, diff, spec, plan | `REVIEW` | Personas derived from the artifact (each one is whoever gets hurt if a given part is wrong) attack it. Two skeptical verifiers then try to refute every finding: one against the artifact, one against the real world — installing the package, booting the database, reading current docs. |
  | An open question, nothing written yet | `DEBATE` | Agents with genuinely incompatible stances propose in isolation, then attack each other's proposals. A judge who proposed nothing reports what survived, the exact mechanism that killed the rest, and the premise every proposal shared without noticing. |
  | Two or more named options | `DECIDE` | One agent steelmans each option and is forbidden from comparing; another kills each one; a judge names the deciding criterion, what would flip it, and the cost of reverting. |

  Output separates **defects** (fixed) from **decisions** (asked one at a time)
  from **investigated false positives** — recorded, never deleted, which is what
  stops a dead finding from coming back next round.

  ```
  /adversarial revisa esse plano
  /adversarial como estruturar o billing
  /adversarial postgres ou sqlite pra isso
  ```

  Don't run it on 1-2 line bugfixes, style, typos, or docs.

## License

MIT
