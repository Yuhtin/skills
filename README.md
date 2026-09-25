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
/plugin install yuhtin-skills@yuhtin
```

The marketplace only has to be added once; after that, new skills I publish show
up in `/plugin` and updates arrive with them.

</details>

<details>
<summary><strong>Codex</strong></summary>

```bash
npx skills@latest add yuhtin/skills
```

It asks which agent and whether to install globally. Add `-g` to skip the second
prompt and go straight to `~/.codex/skills/`.

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

- **[security-review](./skills/security-review/SKILL.md)**: A full pre-release
  audit of an application across six fixed dimensions — security and data
  exposure, concurrency and state integrity, reliability and failure handling,
  accessibility, visual consistency, responsive edge cases.

  Every finding carries severity, category, exact location, real-world impact,
  evidence, reproduction steps, a specific fix, and a confidence level. The audit
  changes no code: the report comes first, then a prioritised remediation plan,
  the quick wins, the things needing architectural work, and a release verdict —
  **ship**, **ship with known risks**, or **do not ship**.

  ```
  /security-review
  /security-review da pra lancar isso?
  ```

  Where `adversarial` forbids a catalogue so the personas find what nobody was
  looking for, this one *is* the catalogue: the goal is coverage, not depth. Run
  `adversarial` before merging, `security-review` before shipping.

- **[animated-deck](./skills/animated-deck/SKILL.md)**: Prepares an animated
  slide deck that explains a project — an architecture, a product flow, a pitch.
  It researches the project first (the subject's code and docs, the brand's own
  color tokens and fonts, the build tools on the machine), then grills you one
  question at a time — each with a recommendation drawn from that research — until
  every placeholder of the brief is filled: audience, story, facts with sources,
  palette by role, fonts, and each slide's scene in beats.

  The output is a prompt to paste into a fresh chat. That chat follows the skill's
  build guide: it writes the cover as the exemplar, fans out one author and one
  adversarial reviewer per slide, and ships motion-design scenes (SVG and canvas)
  that play once and rest on a frame that explains the slide alone — plus an MP4
  recorded frame by frame and a single offline HTML file.

  ```
  /animated-deck explica a arquitetura do agente pra equipe amanhã
  ```

  Built for Claude's Slides artifacts; without them the build still ships the HTML
  player and the MP4. The build needs Chrome, Python with Pillow and Node; ffmpeg
  and puppeteer for video.

## License

MIT
