---
name: map-reduce
description: Apply a Map→Reduce workflow to agent tasks. Use when the user asks to process many similar items (emails, files, links, tickets, candidates, notes) and produce an aggregated result (summary, ranking, dedupe, action list). Prefer parallel tool calls for the map step and a deterministic reduce step that outputs a clear final artifact.
---

# Map→Reduce Workflow (Agent)

## Goal
Turn “many similar items” into a single high-quality output with minimal back-and-forth.

## Step 0 — Define the reducer (the final artifact)
Before touching tools, write down:
- **Output shape:** e.g. top 10 + why, CSV/JSON, bullet summary, decision + next actions
- **Scoring/ranking rules:** what matters most
- **Stop condition:** how many items to map (N) and when to expand

If unclear, ask *one* question: “What do you want as the final deliverable?”

## Step 1 — Map (collect + normalize)
### 1A) Decide the unit of work
Pick one item type:
- Email thread, file, PR, URL, calendar event, etc.

### 1B) Use parallelization by default
- If tool calls are independent, use `multi_tool_use.parallel`.
- If the task is heavy, spawn sub-agents for batches using `sessions_spawn`.

### 1C) Produce a stable per-item record
For each item, extract only what the reducer needs:
- `id` (message id / path / url)
- `title` (subject / filename / page title)
- `timestamp`
- `key_fields` (sender/company/status/etc.)
- `evidence` (1–2 quotes/snippets)
- `confidence` + `next_needed` (if ambiguous)

Keep records machine-friendly (JSONL-ish) even if you present in bullets.

## Step 2 — Reduce (aggregate + decide)
### 2A) Dedupe + cluster
- Group by canonical key (domain/company/thread-id/topic)
- Merge obvious duplicates; keep strongest evidence

### 2B) Rank + summarize
- Apply scoring rules consistently
- Produce:
  - **Top results**
  - **Outliers / uncertainties**
  - **Recommended next actions**

### 2C) Emit a single final artifact
Prefer:
- Bullets with clear headers
- Or a compact JSON/CSV block (when user likely wants copy/paste)

## Step 3 — Expand only if needed
If confidence is low, do a second map pass targeted at gaps:
- “Fetch full body for the top 3 threads”
- “Open only the candidate pages missing salary/location”

## Safety / UX rules
- Don’t take irreversible external actions (send/delete/publish) without explicit confirmation.
- Don’t paste secrets (OAuth codes, tokens) back to chat.
- When browsing or inbox work: report **what you found** and **what you’re about to do**.

## Quick templates
### Per-item record (suggested)
- `id:` …
- `title:` …
- `when:` …
- `summary:` 1 line
- `evidence:` “…”
- `tags:` …

### Reduce output (suggested)
- **Top N**
- **Duplicates merged**
- **Unknowns / needs confirmation**
- **Next actions**
