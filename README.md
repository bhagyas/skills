# Agent Skills

Consolidated skill repository for Bhagyas.

## Skills

- `dag-thinking` - model dependency-heavy problems as directed acyclic graphs.
- `dag-ooda-problem-solving` - combine OODA loops with NetworkX DAG planning and a helper script.
- `map-reduce` - process many similar inputs with a map step and deterministic reduce step.

## Install

Install a single skill with `npx skills`:

```bash
npx skills add bhagyas/skills --skill dag-thinking
npx skills add bhagyas/skills --skill dag-ooda-problem-solving
npx skills add bhagyas/skills --skill map-reduce
```

List skills in this repo:

```bash
npx skills add bhagyas/skills --list
```

## Layout

```text
skills/
  dag-thinking/
    SKILL.md
  dag-ooda-problem-solving/
    SKILL.md
    scripts/ooda_dag.py
  map-reduce/
    SKILL.md
```

## Source Repositories

This repo combines these previous standalone skill repos:

- `bhagyas/dag-thinking-skill`
- `bhagyas/dag-ooda-problem-solving`
- `bhagyas/map-reduce-skill`

`bhagyas/awesome-agent-skills` is intentionally not included; it is an index repo, not a skill source.
