# Skills I Actually Use

Agent skills for Claude Code, Codex, Cursor, and anything else that reads
`SKILL.md`. Small set, kept because they earn their place, not a catalogue.

> **Heads up:** the skills are written in **Portuguese**. The structure is
> runtime-agnostic; the prompts are not translated.

## The skills

| Skill | What you get | Try it |
|---|---|---|
| [**animated-deck**](#animated-deck) | Researches a project, grills you, and returns a prompt that builds an animated deck in one shot. | `/animated-deck explica a arquitetura do agente` |
| [**class-slide**](#class-slide) | Gives a class or talk deck personality: drawn cover, real code running, photos, motion everywhere. | `/class-slide deixa esse deck mais vivo` |
| [**pr-deck**](#pr-deck) | Turns your open PRs into the research for an animated deck, one slide per change. | `/pr-deck` |
| [**adversarial**](#adversarial) | Parallel agents that attack a plan, a diff, an open question, or a choice between options. | `/adversarial revisa esse plano` |
| [**pr-review**](#pr-review) | Reviews a pull request end to end: a self-approved plan, the right skill per risk, every changed screen seen, a comment on the PR. | `/pr-review #2818` |
| [**security-review**](#security-review) | A full pre-release audit across six fixed dimensions, ending in a ship verdict. | `/security-review da pra lancar isso?` |
| [**eval-guidelines**](#eval-guidelines) | The rules for building the eval of a harness, agent, or LLM app. | `/eval-guidelines` |
| [**guardrail-guidelines**](#guardrail-guidelines) | The defenses to weigh, layer by layer, when an LLM gets tools. | `/guardrail-guidelines` |
| [**skill-eval-guidelines**](#skill-eval-guidelines) | How to tell whether a skill actually works, before you write, keep, or install it. | `/skill-eval-guidelines` |
| [**parallel**](#parallel) | Splits a list of work into waves that run at the same time without colliding. | `/parallel as issues do milestone 2` |
| [**deeper-version**](#deeper-version) | Rewrites a task as a deeper version of itself, not a bigger one. | `/deeper-version analisa o churn` |
| [**optimize-app**](#optimize-app) | Finds the real performance gap, fixes it, and measures before and after each fix. | `/optimize-app` |

## Presentations

Decks that explain a project, a class, or a week of work.

### animated-deck

[`skills/animated-deck/SKILL.md`](./skills/animated-deck/SKILL.md)

Prepares an animated
slide deck that explains a project — an architecture, a product flow, a pitch.
It researches the project first (the subject's code and docs, the brand's own
color tokens and fonts, the build tools on the machine), then grills you one
question at a time — each with a recommendation drawn from that research — until
every placeholder of the brief is filled: audience, story, facts with sources,
palette by role, fonts, and each slide's scene in beats.

The output is a prompt to paste into a fresh chat. That chat follows the skill's
build guide: it writes the cover as the exemplar, then every other slide itself, one
at a time in a single context (no subagents), each rendered and re-read
adversarially, and ships motion-design scenes (SVG and canvas) that play once and rest on a frame that explains the slide alone — plus a single
offline HTML file where a click finishes a playing scene before moving on, and an
MP4 recorded frame by frame if you ask for one.

```
/animated-deck explica a arquitetura do agente pra equipe amanhã
```

Built for Claude's Slides artifacts; without them the build still ships the HTML
player. The build needs Chrome, Python with Pillow and Node; ffmpeg and puppeteer
only for video.

### class-slide

[`skills/class-slide/SKILL.md`](./skills/class-slide/SKILL.md)

The style layer for a class, workshop, or talk that needs personality. It
decides the thesis, the chapters, and a color-role table before the first slide,
then holds every slide to the rules that make a class feel alive: a cover that
draws the subject itself in halftone dots that assemble once, the real thing
(code, terminal, screen, PR) running step by step instead of a mockup, one real
photo per concept with its credit in the footer, brand icons for the tools, dark
backgrounds only where the machine is working, and at least one exercise for the
audience. Motion is everywhere and still readable: things assemble, execute,
react, and transform, then rest on a frame that explains the slide alone.

Everything it needs ships with it: `references/recipes.md` has runnable code for
the scene kit, a complete one-file HTML deck, the halftone cover, the
step-through, the terminal window, Wikimedia Commons photos with credits, and
brand icons. It works alone or as the style for `animated-deck`.

```
/class-slide aula sobre análise sintática para a turma
/class-slide deixa esse deck mais vivo
```

### pr-deck

[`skills/pr-deck/SKILL.md`](./skills/pr-deck/SKILL.md)

Turns your open pull requests into
the research for an animated deck. It lists every open PR of yours with `gh`,
whatever the base branch, reads each diff, and files one card per PR — what changed, in
the words of whoever uses the product, before and after, every fact sourced to
the diff. Then it decides each PR's slide:

| The PR is | It becomes |
|---|---|
| A bug fix or a small change | One line on a shared slide, three to five per slide, grouped by product area. |
| A new feature | A slide of its own, where the motion is the explanation and the text stays short. |
| A change you can see on a screen | Where → what → before/after: a small map of the page, a zoom into the region that changed, the old state giving way to the new one. Never a full screenshot. |

It hands all of that to `animated-deck`, with most of its grilling
already answered. Two questions it always asks and waits on: who the audience
is, and — once it knows — whether the slide-by-slide outline is right.

```
/pr-deck
/pr-deck só o 412 e o 418
```

Needs `animated-deck` and an authenticated `gh`, run from the repository the
PRs belong to.

## Review and decide

A second reader with no stake in the thing being right.

### pr-review

[`skills/pr-review/SKILL.md`](./skills/pr-review/SKILL.md)

Reviews a pull request end to end, in one context and without subagents. It
studies the PR first (what it is about, its size by file type, everything it
touches) and writes its own **goal**: the three to six claims that must hold for
the PR to be ready to merge. Then it plans the review without waiting for
approval: the red flags it checks on sight (more than one problem in the PR,
committed mockups, conflicts, a migration number that collides with main, CI that
never really ran, a stacked PR riding along) and one lens per risk the PR
carries, picked from a catalogue of skills by Matt Pocock, Emil Kowalski and this
repo. When a lens is missing it names the skill, why this PR needs it, and the
`npx skills` command that installs it.

It runs the app locally to see every changed screen on desktop and at 390 px,
checks the claims in the PR body, posts a comment review (never an approval),
and ends by asking whether to apply the suggested changes on the PR, in a
separate PR, or leave the comment.

```
/pr-review https://github.com/owner/repo/pull/123
```

### adversarial

[`skills/adversarial/SKILL.md`](./skills/adversarial/SKILL.md)

Parallel agents mandated to
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

### security-review

[`skills/security-review/SKILL.md`](./skills/security-review/SKILL.md)

A full pre-release
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

## Building with AI

The rules for agents, evals, guardrails, and skills themselves.

### eval-guidelines

[`skills/eval-guidelines/SKILL.md`](./skills/eval-guidelines/SKILL.md)

The rules to follow
whenever you create or improve the eval of a harness, custom agent, or anything
else built on an LLM: real failures as cases and error analysis before any grader,
the cheapest grader that catches each failure, the grader itself checked against
human labels, an error bar and a detection floor on every number, and what to run
on each commit, on each prompt change, and after shipping.

It ends on four numbers: pass rate with its error bar, grader vs human agreement,
detection floor, and the share of cases that got worse in the last change.

```
/eval-guidelines
/eval-guidelines melhora o eval do agente de suporte
```

### guardrail-guidelines

[`skills/guardrail-guidelines/SKILL.md`](./skills/guardrail-guidelines/SKILL.md)

The defenses
to weigh whenever you create or improve the guardrails of a harness, custom agent,
or anything else that gives an LLM tools, layer by layer: before the model, inside
it, between it and the tool, around the tool, after it, and across the design.

Each defense is marked. Guardrails that read text are useful filters, but an attacker
who keeps adjusting gets past them; structural ones can't be talked out of a decision,
and the ones that held up against that attacker are all in the design layer. It ends
on a table: every harmful action the agent can take, what stops it with the model
fooled, the gap that rule still leaves, and the actions nothing stops yet.

```
/guardrail-guidelines
/guardrail-guidelines protege o agente de suporte contra prompt injection
```

### skill-eval-guidelines

[`skills/skill-eval-guidelines/SKILL.md`](./skills/skill-eval-guidelines/SKILL.md)

The rules to
follow whenever you write a skill, judge one, or decide whether to install it: core
points before text, adherence and effect scored as a pair, real tasks run against a
no-skill arm and an unrelated-text control of the same length, and what each result
says to rewrite, drop, or keep.

It ends on four questions for anyone who says a skill works: which model, which
version, what baseline, and what length control.

```
/skill-eval-guidelines
/skill-eval-guidelines vale instalar essa skill de code review?
```

## Getting work done

Smaller tools for the daily loop.

### parallel

[`skills/parallel/SKILL.md`](./skills/parallel/SKILL.md)

Splits a list of work — a
milestone's issues, a goal's deliverables — into waves that can run at the same
time in separate sessions or worktrees without stepping on each other. It reads
what each item will actually write (files, tables, migrations, shared contracts,
generated files) instead of trusting the title, marks what collides and what
depends on what, and puts colliding items in different waves: waiting a wave is
cheap, untangling two finished PRs is not. It ends with one table per wave, the
reason in a sentence for each item, and a self-contained prompt per item that
gives the goal and the limits, not a step-by-step plan. It only launches the
sessions if you ask.

```
/parallel as issues abertas do milestone 2
/parallel o que dessa lista dá pra rodar junto?
```

### deeper-version

[`skills/deeper-version/SKILL.md`](./skills/deeper-version/SKILL.md)

Turns a task into a
deeper version of itself, not a bigger one. Before rewriting the prompt it
answers four questions: what a top professional in the field would do that you
didn't ask for, the rawest material they would start from instead of what has
already been digested, the specific methods and tools they would use, and what
— other than you or the model — would show the result is right. Then it
rewrites the prompt to ask for exactly that.

```
/deeper-version analisa o churn dos últimos 6 meses
```

### optimize-app

[`skills/optimize-app/SKILL.md`](./skills/optimize-app/SKILL.md)

Makes an app faster — startup
time, how fast each screen opens, how fast content loads, scrolling, and how
quickly older content comes in. It finds where the real performance gap is
before touching anything, applies the fixes, and benchmarks before and after
each one to see whether it actually worked. The baseline comes from the rawest
data the project has (production traces before local runs), before and after
are measured under the same conditions over several runs, any fix that didn't
beat the noise is reverted, and the real flows are re-run to show nothing broke.
It ends with a before/after table, one row per fix, reverted ones included.
Measurement rules adapted from a checklist based on
[@santtiagom_'s post](https://x.com/santtiagom_/status/2111589281282077045).

```
/optimize-app
/optimize-app a tela de listagem demora pra abrir
```

## Install

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

## License

MIT
