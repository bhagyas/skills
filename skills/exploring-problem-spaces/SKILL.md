---
name: exploring-problem-spaces
description: Explore-and-verify loop for problems whose shape is not yet known — map what is known versus assumed, pick actions that discriminate between hypotheses, backtrack when evidence contradicts, and verify explicit exit tests before claiming success. Use when solving ambiguous, unfamiliar, multi-step, diagnostic, research, planning, architecture, or design problems where important facts, constraints, causes, available actions, or success criteria are not yet known, including unknown root-cause investigations, unfamiliar codebases, and decisions with missing requirements. Do not use for trivial, fully specified, single-step tasks such as mechanical edits, formatting, or running a named command.
---

# Exploring problem spaces

## The mental model

Treat an unfamiliar problem as a graph that is revealed as you move through it, not as a
puzzle you can see from above:

| Concept | Meaning here |
|---|---|
| State | Your current decision-relevant understanding |
| Transition | An action available from that state |
| Exploratory action | Primarily reveals information about the graph |
| Instrumental action | Primarily changes the system or advances toward the goal |
| Observation | Evidence that updates your model |
| Dead end | A disproven hypothesis, invalid route, or failed approach |
| Backtracking | Revising the plan after new evidence |
| The exit | Explicit, evidence-backed success conditions |

The value of the metaphor is the discipline it imposes: you cannot see the whole maze, so
you spend moves either to reveal structure or to advance, and you check that you actually
walked out rather than assuming the corridor led somewhere.

Keep the metaphor internal. Real problems are not rectangular grids, and users want
findings, not talk of corridors and walls. Write "the token is missing the `write` scope"
rather than "this branch of the maze is a dead end."

## Trigger check (do this first)

Run one honest check before building anything: **is the shape of this problem actually
unknown?**

Use the loop when several of these hold:

- The cause, the correct approach, or the right requirements are genuinely unclear.
- More than one plausible explanation or route exists, and they imply different work.
- Acting on the wrong guess would be expensive, destructive, or hard to reverse.
- The system, codebase, domain, or data is unfamiliar.
- Success criteria are vague or unstated.

Skip it, and just do the task, when the request is fully specified and low-risk: a
mechanical rename, a formatting change, a named command, a direct factual lookup, a small
edit whose correctness is obvious once done. For these, do the work and verify it — that
verification *is* the entire loop at this scale. Producing a problem map for a two-line
change wastes the user's time and reads as ceremony.

Between those poles, scale the machinery to the uncertainty. A short task may need nothing
more than two sentences naming the leading hypotheses and the check that separates them.

## Relationship to other skills

This is an orchestration skill. It decides *which* action is worth taking next and keeps
the map honest; it does not replace specialist skills.

When a chosen action falls into a domain covered by another skill — systematic debugging,
code review, research, architecture design, testing, implementation planning, a
document-format skill — invoke or follow that skill for the action itself, then return
here to record what was observed and re-pick the frontier. If a specialist skill is
mandatory for the task, it wins; this loop wraps around it rather than competing with it.

Do not restate detailed specialist workflows here.

## Core principles

**1. Map before committing.** When material uncertainty remains, resist the first
plausible explanation. Establish what is known, what is merely assumed, what is unknown,
which unknowns could change the route, and what evidence would separate the leading
explanations. The first plausible story is often right — but the cost of checking is
usually far lower than the cost of building on a wrong one.

**2. Explore only when exploration changes a decision.** An exploratory action earns its
cost only if its possible results could change the next action, the selected hypothesis,
the implementation, the risk assessment, or whether the goal is already met. If every
outcome leads to the same next move, skip it and move.

**3. Prefer discriminating experiments.** Favor actions whose outcome splits the hypothesis
set. Inspecting a token's scopes separates "expired token" from "missing permission"
faster and more cheaply than rewriting the auth layer, and it tells you which fix to write.

**4. Prefer cheap, reversible, low-risk actions.** Among actions with similar value, take
the one that is cheaper, faster, safer, easier to undo, and more likely to yield
unambiguous evidence. Read before write; copy before overwrite; staging before production.

**5. Separate facts from hypotheses.** Never silently promote an assumption to a fact. Each
important item is one of: observed fact, user-provided fact, inferred conclusion, working
hypothesis, assumption, constraint, or unresolved unknown. Most bad debugging comes from an
assumption that quietly became a premise.

The user's framing needs this treatment most. When someone says "it broke after the
deploy," the symptom is a user-provided fact and the cause is a hypothesis about
correlation — one they had good reason to form, and one that is frequently wrong, because
the change that revealed a problem is not always the change that caused it. If it is cheap
to test the premise, test it: confirming that the pre-change state actually worked can save
a rollback that fixes nothing, and disconfirming it redirects the whole investigation.

**6. Preserve provenance.** Tie important claims to their source: user statement, source
file and line, command output, test result, log entry, documentation, API response,
external source. Never fabricate an observation, and never describe a command, test, or
tool call as having been run when it was not — a false observation corrupts every later
decision and destroys the user's ability to trust the rest.

**7. Avoid exhaustive search.** Do not enumerate the state space. Build an implicit,
task-relevant map and expand only decision-critical branches. Keep roughly three to five
live hypotheses and a small frontier; if the list grows past that, you are probably
listing possibilities rather than discriminating between them.

**8. Backtrack explicitly.** When evidence contradicts the current route, say so, record
what was disproven and by what evidence, and choose a new frontier action. Do not defend a
dying hypothesis, and do not re-walk a rejected route without materially new evidence.

**9. Verify the real exit.** A plausible explanation, a compiling change, or a written
document is not a solved problem. Define observable exit tests early — for diagnostic and
implementation work, ideally the user's original symptom, reproduced and then shown gone —
and run them before reporting success.

For decision, design, and recommendation work the exit is different in kind but not in
rigor: the deliverable is a specific recommendation whose load-bearing claims each trace to
a stated constraint or observation, with the conditions that would reverse it named. A
recommendation nobody can audit or overturn has not passed anything.

**10. Stop at the right time.** Stop when the exit tests pass, when remaining uncertainty
cannot materially change the result, when the budget is spent, when a required capability
is unavailable, or when the next action needs approval. If blocked, name the exact blocker
and the cheapest next observation or action that would unblock it.

If asked to keep looking after the exit tests pass, say that they pass and that further
searching has no decision value — but listen for what prompted the request. A specific
worry ("I don't trust the retry path") is a new goal deserving its own exit test, and that
is real work. Unbounded searching is not; offer a bounded check instead.

**11. A destructive request is a proposed route, not a decision.** When the user asks for
something irreversible, it still has to survive the evidence test that any other candidate
action would face. Before it happens: say concretely what would be lost, check whether the
evidence actually supports that route, and offer the safer route you would take instead.
Then wait for explicit approval. Users propose drastic actions when they are frustrated and
out of ideas — often the diagnosis shows the drastic action would not even have worked.

## The loop

**1. Frame.** Identify the requested outcome, the starting situation, explicit constraints,
available tools and permissions, budget (time, tokens, cost, calls), risks, and concrete
exit tests. If success criteria are vague, derive provisional ones and label them as
provisional so the user can correct them.

**2. Build the map.** Assemble goal, exit tests, known facts with evidence, assumptions,
constraints, leading hypotheses, important unknowns, actions taken, observations, rejected
routes, remaining budget, and the current frontier. Include everything from the past that
could still affect a future decision; omit history that cannot. See
`references/problem-map-template.md` for the full template and a compact inline form.

**3. Rank the unknowns.** Order unknowns by how much resolving them would change the route.
Missing information that cannot change any decision is not worth pursuing, however
conspicuous the gap.

**4. Generate candidate actions.** Separate exploratory (reveals information), instrumental
(advances or changes the system), and mixed actions. Naming the kind prevents the common
failure of "researching" when the decision is already made, or "fixing" before knowing what
is broken.

**5. Evaluate the frontier.** Rate candidates qualitatively on expected goal progress,
expected decision-relevant information, ability to discriminate between hypotheses, cost,
risk, reversibility, permissions required, and evidence reliability. A useful shorthand:

```
value ≈ expected goal progress
      + expected decision-relevant information
      + reversibility
      − cost
      − risk
```

High / medium / low is normally enough. Do not invent numeric probabilities unless real
data supports them; false precision is worse than an honest ranking.

**6. Act.** Take the highest-value action, or a small batch of genuinely independent
actions. Change one variable at a time when you intend to measure the effect — parallel
changes destroy the attribution you were trying to buy.

Before an action that is irreversible, destructive, expensive, privacy-sensitive,
externally visible, or otherwise high-impact, get the user's approval first, and offer the
safer alternative you would take instead. Prefer reading available context and tools over
questioning the user; ask one focused question only when the answer is genuinely
unavailable and could change the route.

**7. Observe and update.** Record what was actually done, what was actually observed, which
hypotheses gained or lost support, which branches are pruned, which new unknowns appeared,
and whether the route changes.

**8. Repeat or backtrack** until an exit or stopping condition is reached.

**9. Verify and report.** Run the exit tests. Then report, keeping these distinct: the
verified result, the evidence supporting it, decisions that shaped the outcome, remaining
uncertainty that could still matter, risks or limitations, and — if blocked — the exact
blocker and the precise next step.

## Communication

The map is a decision record, not a transcript of reasoning. Store and share conclusions,
evidence, hypotheses with their status, unknowns, chosen actions, observations, test
results, and open risks. Do not persist verbose internal deliberation, do not narrate every
step, and do not ask the user to supply their private reasoning.

Update the user when there is something worth their attention: a meaningful discovery, a
route change, a blocker, a request for approval, or a completed verification. When
explaining a choice, give a one-line rationale ("checking the token scopes first because it
separates the two leading causes and costs nothing") rather than a reasoning trace.

Working state stays in context for short tasks. For long-running, multi-session, or
multi-agent work, persist it to a task-specific working file, and say where. Do not commit
these files or reorganize the repository for bookkeeping unless the user asks.

## Failure modes to avoid

| Failure | Instead |
|---|---|
| Implementing the first plausible fix | Name the competing explanations; run the cheap check that separates them |
| Asking the user broad questions up front | Read the code, logs, config, and context first; ask one focused question about what remains |
| Gathering information that changes nothing | Drop the unknown, or state why it matters to the decision |
| Re-exploring a branch already ruled out | Keep a rejected-routes list; require new evidence to revisit |
| Treating an assumption as observed | Label every item by type and record its source |
| Accepting the user's stated cause as the cause | Symptom is fact, cause is hypothesis; test the premise when it is cheap |
| Doing something destructive because it was requested | Price the loss, check the evidence supports it, offer the safer route, wait for approval |
| Building a huge exhaustive graph | Keep 3–5 live hypotheses and a small frontier |
| Continuing research after the decision is clear | Stop; report the recommendation and the residual uncertainty |
| Changing several variables at once | One change per measurement when attribution matters |
| Declaring success without exit tests | Run the tests; quote the actual output |
| Claiming a command or test ran when it did not | Report only what was really executed and observed |
| Persisting verbose reasoning traces | Keep facts, evidence, decisions, and results |
| Running this loop on a trivial task | Do the task, verify it, move on |

## References

Load these only when they help:

- `references/problem-map-template.md` — full problem-map template, a compact form for
  short tasks, and a worked example.
- `references/evaluation-scenarios.md` — scenarios that define correct behavior at the
  boundaries, including when *not* to use this skill. Useful when calibrating or editing
  this skill.
