# Problem map

The map is a compact decision record: enough state that a future decision (or a different
agent, or you after a context reset) can be made correctly without re-deriving everything,
and no more. Drop rows that can no longer affect a decision.

Three sizes, chosen by task:

- **Inline compact form** — short or moderate tasks. Two to six lines, kept in context.
- **Full template** — long, branching, or high-stakes tasks.
- **Persisted file** — long-running, multi-session, or multi-agent work. Write to a
  task-specific working file (for example `.notes/<task>-map.md` or a temp path) and say
  where it lives. Do not commit it or restructure the repo for bookkeeping unless asked.

---

## Compact inline form

```
Goal: 401 on all API requests after Friday's deploy → restored, verified by the user's own request
Exit test: `curl -s -o /dev/null -w '%{http_code}' $API/v1/orders` returns 200 with the prod token
Facts: 401 began at 14:02 UTC (observed, deploy log); auth code unchanged in this release (observed, git diff)
Hypotheses: [H1] token/secret rotated in env — medium · [H2] clock skew on new node — low · [H3] upstream IdP config change — medium
Next: decode the token from the running pod and compare `aud`/`exp`/scopes against the IdP config — read-only, separates H1 from H3
```

That is often all a real task needs. Expand only the sections that are carrying weight.

---

## Full template

# Problem Map

## Problem
One or two sentences: what must be solved, in the user's terms.

## Goal
The desired end state.

## Exit tests
Observable conditions that establish success. Prefer reproducing the user's original symptom
and showing it gone. Mark any test you derived yourself as *provisional* until confirmed.

| # | Exit test | How it is checked | Status |
|---|-----------|-------------------|--------|

## Known facts

| Fact | Type | Evidence / source | Confidence |
|------|------|-------------------|------------|

Type is one of: observed fact, user-provided fact, inferred conclusion, working hypothesis,
assumption, constraint, unknown. Confidence is a qualitative decision aid (high / medium /
low) unless it is genuinely calibrated — do not dress up a guess as a number.

## Assumptions

| Assumption | Why it is currently necessary | How it could be tested |
|------------|-------------------------------|------------------------|

Anything here that is load-bearing and cheap to test is usually the best next action.

## Constraints
Technical, legal, temporal, financial, safety, permission, and user constraints. Include
budget: time, cost, tool calls, tokens, review cycles.

## Hypotheses

| # | Hypothesis | Supporting evidence | Contradicting evidence | Status |
|---|------------|---------------------|------------------------|--------|

Status: leading, live, weakened, rejected, confirmed. Keep roughly 3–5 live at a time. When
one is rejected, record the evidence that killed it and move it to rejected routes.

## Important unknowns

| Unknown | Decision impact (what changes if resolved) | Possible observation |
|---------|--------------------------------------------|----------------------|

If the decision-impact cell is empty, delete the row.

## Frontier

| Candidate action | Kind | Expected progress | Info value | Cost | Risk | Reversible |
|------------------|------|-------------------|------------|------|------|------------|

Kind: exploratory, instrumental, or mixed. Flag any action needing user approval.

## Action and observation log

| # | Action actually performed | Actual observation | Map update |
|---|---------------------------|--------------------|------------|

Record only what really ran. If an action was planned but not executed, it belongs on the
frontier, not in this log.

## Rejected routes
Routes not to repeat without materially new evidence, each with the evidence that closed it.

## Current route
The present working plan, in one to three lines.

## Status
exploring · acting · verifying · solved · blocked · stopped

## Remaining uncertainty
Only uncertainty that could still change the outcome or matter to the user. If something is
unknown but immaterial, either say so in one line or drop it.

---

## Worked example (abbreviated)

**Problem** Requests return 401 after Friday's deploy.
**Exit test** The user's failing request returns 200 against production. *(confirmed with user)*

| Fact | Type | Source | Conf |
|---|---|---|---|
| 401s start 14:02 UTC, exactly at rollout | observed | deploy log + metrics dashboard | high |
| No change to auth middleware in this release | observed | `git diff v2.3.1..v2.3.2 -- src/auth/` | high |
| Gateway logs show `invalid_scope`, not `token_expired` | observed | `kubectl logs gw-7f9` line 442 | high |

| # | Hypothesis | Support | Contradiction | Status |
|---|---|---|---|---|
| H1 | Secret rotated, service token stale | timing | error is `invalid_scope`, not expiry | rejected |
| H2 | New IdP client config dropped a scope | error string, timing | — | leading |
| H3 | Auth code regression | timing | no auth diff in release | rejected |

**Rejected routes** Rewriting token refresh (H1 disproven by the error code — the gateway
received a valid, unexpired token). Do not revisit without evidence of expiry errors.

**Frontier**

| Action | Kind | Progress | Info | Cost | Risk | Reversible |
|---|---|---|---|---|---|---|
| Diff IdP client scopes against last known-good config | exploratory | low | high | low | none | n/a |
| Re-add `orders:write` to the client in staging, retest | mixed | high | high | low | low | yes |
| Roll back the deploy | instrumental | high | none | medium | medium | yes |

Chosen: the scope diff — it confirms or kills H2 for almost nothing, and a rollback that
fixes the symptom without explaining it leaves the same failure waiting for the next deploy.
