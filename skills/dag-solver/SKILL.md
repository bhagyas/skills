---
name: dag-solver
description: Solve complex tasks by decomposing them into a directed acyclic graph of independently verifiable work nodes. Use when a task has dependencies, can be split into testable subproblems, benefits from topological ordering, or can safely delegate independent branches to subagents without overlap or direct dependency.
---

# DAG Solver

Use a directed acyclic graph (DAG) to turn a complex task into independently verifiable work nodes, execute them in dependency order, and delegate only when branches are genuinely independent.

## Core Rule

Every node must be small enough to verify on its own.

The solver should keep at least a three-step lookahead from the current frontier toward the final outcome. At any point, be able to explain:
- The current node or frontier.
- The next dependency that unlocks.
- The downstream integration or decision point it is moving toward.

If new evidence changes any of those three steps, update the DAG immediately instead of continuing with the stale plan.

A valid node has:
- **Goal**: one concrete outcome.
- **Inputs**: files, data, decisions, or prior nodes it depends on.
- **Output**: the artifact or state it produces.
- **Verification**: a command, inspection, test, assertion, or acceptance check that proves the node is done.
- **Verification cost**: cheap, moderate, or expensive.
- **Blast radius**: files, systems, or concepts it may touch.

If a node cannot be verified independently, split it.

## Build the DAG

1. List the final outcome.
2. Work backward into prerequisite nodes.
3. Add edges as `A -> B`, meaning "A must complete before B."
4. Validate that the graph has no cycles.
5. Group nodes into topological layers.

Use NetworkX for non-trivial graphs:

```python
import networkx as nx

G = nx.DiGraph()
G.add_edges_from([
    ("inspect current behavior", "define node plan"),
    ("define node plan", "implement isolated fixes"),
    ("implement isolated fixes", "run integrated verification"),
])
assert nx.is_directed_acyclic_graph(G)
layers = [list(layer) for layer in nx.topological_generations(G)]
```

## Node Template

Use this compact shape while planning or executing:

```text
Node: <short imperative name>
Depends on: <node ids or none>
Touches: <files/modules/systems>
Output: <artifact/state>
Verification: <specific check>
Verification cost: <cheap/moderate/expensive>
Delegate: yes/no, with reason
```

## Verification Cost

Prefer the cheapest verification that is strong enough for the node. Expensive test runs are not mandatory at every node when the change is clearly outside their coverage, cannot affect the tested behavior, or has already been covered by a more targeted check.

When skipping an expensive run, record why it is safe to defer and add it as an explicit downstream verification node, usually at the end of the goal or at the relevant conjunction. That node should list the deferred command and the completed nodes it is meant to cover.

Do not skip expensive verification when the change touches shared behavior, public contracts, build configuration, data migrations, concurrency, security, payments, persistence, or any area where the blast radius is uncertain.

## Source Control Boundaries

Before starting DAG work, protect the starting state:
- If policy allows autonomous git operations, commit all current work first with a message that clearly describes the baseline.
- If autonomous git operations are not clearly allowed, ask whether to commit before starting.

After the DAG goal is complete, publish the finished state:
- If policy allows autonomous git operations, commit the completed work and push it.
- If autonomous git operations are not clearly allowed, ask whether to commit and push before ending.

Do not silently mix unrelated user changes into DAG work. If unrelated changes are present, either commit them as the baseline before starting or ask how to handle them.

## Delegation Rules

Delegate a node to a subagent only when all are true:
- It has no direct dependency on another in-flight node.
- It does not write the same files, records, schemas, shared state, or public API surface as another in-flight node.
- Its verification can be performed independently before integration.
- The expected output can be summarized or patched back without relying on hidden context.
- Failure in the delegated node will not invalidate work already started elsewhere except through an explicit downstream edge.

Do not delegate:
- Cross-cutting refactors.
- Shared API or schema changes.
- Nodes that need continuous coordination with other active nodes.
- Final integration, final review, or release decisions.
- Tasks where the verification depends on another in-flight node finishing first.

When delegating, give the subagent only the node contract: goal, inputs, allowed files, forbidden overlap, expected output, and verification command. Do not pass the entire DAG unless it is needed.

Use branches for independent delegated paths. A branch is a set of one or more nodes a subagent can execute without depending on another active branch. Keep branch outputs separate until a conjunction node explicitly requires them together.

Name branches after the purpose of the DAG task or branch path, using a short conventional prefix and a concrete slug. Examples:
- `feature/new-feature`
- `bug/discovered-bug`
- `refactor/extract-shared-parser`
- `docs/update-release-notes`
- `test/add-regression-coverage`
- `investigate/payment-timeout`

The branch name should make the work's intent obvious at a glance. Prefer the final outcome when one branch owns the goal, and prefer the branch-specific purpose when several subagents are exploring independent paths inside the same larger goal.

A conjunction node is the merge point for branches. It must define:
- Which branch outputs are required.
- Which branch names are being merged.
- The compatibility checks between those outputs.
- The integration work that combines them.
- The verification proving the merged state works.

Do not merge branches opportunistically. Merge only when the DAG has an explicit conjunction node whose prerequisites are complete.

## Execution Workflow

1. **Protect baseline**: Commit the current state before work begins, or ask whether to commit if permission is unclear.
2. **Plan**: Build the node list and edges. Mark each node with verification, verification cost, and blast radius.
3. **Validate**: Check for cycles and unresolved dependencies.
4. **Select frontier**: Work only on nodes whose prerequisites are complete.
5. **Look ahead**: Confirm the current frontier, the next unlock, and the downstream conjunction or decision point.
6. **Parallelize carefully**: Delegate or run in parallel only among frontier nodes with disjoint blast radius, treating each independent path as a branch.
7. **Verify per node**: Run the node's verification before marking it complete, using targeted checks when they prove the node.
8. **Integrate at conjunctions**: Merge branches only after all prerequisite branch outputs are verified.
9. **Defer expensive checks deliberately**: If an expensive run is unnecessary now, add it as a later verification node with the reason for deferral.
10. **Update graph**: Add, split, reorder, or remove nodes as new facts appear.
11. **Final verify**: Run end-to-end checks that prove the final outcome, not just the individual nodes.
12. **Publish result**: Commit and push the completed work, or ask whether to commit and push if permission is unclear.

## Handling Cycles

If you find a cycle, the task is not ready to execute as a DAG.

Resolve it by:
- Clarifying which edge is a real prerequisite versus a preference.
- Collapsing tightly coupled nodes into one node with a single verification check.
- Time-slicing feedback into stages, such as `design v1 -> implement v1 -> evaluate -> design v2`.

## Output Format

When applying this skill, produce:

1. **Nodes**: Each node with goal, output, verification, verification cost, and blast radius.
2. **Edges**: `A -> B` dependencies.
3. **Cycle check**: `acyclic: yes/no`.
4. **Layers**: Topological execution layers.
5. **Delegation plan**: Which nodes can run in subagents and why; which must stay local and why.
6. **Branch plan**: Independent subagent branches, their purpose-based names, and their conjunction nodes.
7. **Lookahead**: Current frontier, next unlock, and downstream conjunction or decision point.
8. **Deferred expensive checks**: Commands intentionally postponed, with the reason and the node where they will run.
9. **Source control plan**: Baseline commit status, final commit plan, and push expectation.
10. **Execution status**: Pending, in progress, verified, blocked.
11. **Final verification**: The integrated checks required before calling the task done.

## Quality Bar

- Prefer fewer, verifiable nodes over many vague tasks.
- Make verification concrete before implementation starts.
- Match verification cost to risk; do not spend expensive test runs when a targeted check is sufficient.
- Add skipped expensive runs as explicit downstream verification nodes, not as vague follow-up notes.
- Treat "no overlap" as a file/API/state constraint, not just a conceptual difference.
- Re-run the DAG after discoveries that change dependencies.
- Keep a live three-step lookahead and revise it when reality changes.
- Make branch merges explicit conjunction nodes with their own verification.
- Name branches by purpose, such as `feature/<slug>`, `bug/<slug>`, `refactor/<slug>`, `docs/<slug>`, `test/<slug>`, or `investigate/<slug>`.
- Commit before starting DAG work and commit plus push after finishing, or ask for both decisions when permission is unclear.
- Never mark a node complete from implementation alone; completion requires verification.
