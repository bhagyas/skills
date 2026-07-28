---
name: exploring-problem-spaces
description: Use when solving ambiguous, unfamiliar, multi-step, diagnostic, research, planning, architecture, or design problems where important facts, constraints, causes, available actions, or success criteria are not yet known. Do not use for trivial, fully specified, single-step tasks.
---

# Exploring Problem Spaces

Treat an uncertain problem as a partially observable decision graph: a current state is the decision-relevant understanding; actions either reveal information, advance the goal, or both; observations update the map. Use the maze as an internal metaphor, not as user-facing jargon.

## Portable tooling

When this workflow needs a Python helper, run it with `uv run` and declare any non-standard dependency in that command (for example, `uv run --with package-name python tool.py`). Do not assume globally installed Python packages or mutate a project's dependency files merely to explore or validate a problem.

## Trigger check

Use this workflow only when uncertainty could materially change the route. For a fully specified, low-risk task, act directly and verify it. Prefer a specialist skill for a selected action (for example debugging, research, architecture, testing, code review, or implementation planning); retain this skill's compact problem map across that work.

## Frame before committing

1. State the requested outcome, initial situation, explicit constraints, tools and permissions, relevant budget, and risks.
2. Define observable exit tests. If success is vague, propose provisional tests and label them as such.
3. Separate each important item into: observed fact, user-provided fact, inferred conclusion, working hypothesis, assumption, constraint, or unresolved unknown. Preserve a concise source for important facts.
4. Create a compact map using [the problem-map template](references/problem-map-template.md). Keep three to five leading branches by default; do not exhaustively enumerate the space.
5. Rank unknowns by decision impact: prioritize only those whose outcome could change the next action, selected hypothesis, implementation, risk, or completion decision.

For short work, keep the map in working notes. For long-running, multi-agent, or multi-session work, persist a task-specific map only when it helps continuity; do not commit it or alter the repository merely for bookkeeping.

## Choose the frontier

Classify actions as exploratory, instrumental, or mixed. Compare promising actions qualitatively by expected goal progress, decision-relevant information, hypothesis discrimination, cost, risk, reversibility, permissions, and evidence reliability.

Prefer a discriminating experiment over a broad or speculative change. When value is similar, choose the cheaper, faster, safer, more reversible action that yields clearer evidence. A useful rule is: value = expected progress + decision-relevant information + reversibility - cost. Use high/medium/low ratings unless calibrated data exists.

Execute one coherent next action, or a small batch only when independent. Before an irreversible, destructive, costly, privacy-sensitive, externally visible, or high-impact action, obtain required approval. Do not ask for information safely available in the context or tools; ask one focused question only when it could materially change the route.

## Observe, update, and backtrack

After each action, record the actual observation, update support for hypotheses, prune disproven branches, and add any decision-critical unknowns. Never claim an observation, command, tool call, or test that did not occur.

When evidence contradicts the current route, explicitly record the rejected route, do not retry it without new evidence, and select a new discriminating frontier action. Avoid changing multiple variables before measuring their effect.

## Verify the exit and report

Stop when exit tests pass, remaining uncertainty cannot materially affect the result, the budget is exhausted, a required capability is unavailable, or the next action needs approval. Do not continue gathering evidence after the decision is clear merely because more is available.

Run the exit tests before claiming success. Report the verified result, supporting evidence, material decisions, remaining uncertainty or limitations, and—if blocked—the exact blocker plus cheapest useful next observation or action. Provide progress updates only for meaningful discoveries, route changes, blockers, or completed verification. Communicate concise decision records, never hidden reasoning traces.

## Guardrails

Do not immediately implement the first plausible answer; ask broad questions before inspecting available evidence; gather irrelevant facts; repeat a failed branch; conflate assumptions with observations; create a huge graph; over-explore after completion; or claim success without exit tests.

For representative behavior and boundary checks, consult [the evaluation scenarios](references/evaluation-scenarios.md).
