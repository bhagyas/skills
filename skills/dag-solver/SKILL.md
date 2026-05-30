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

A conjunction node is the merge point for branches. It must define:
- Which branch outputs are required.
- The compatibility checks between those outputs.
- The integration work that combines them.
- The verification proving the merged state works.

Do not merge branches opportunistically. Merge only when the DAG has an explicit conjunction node whose prerequisites are complete.

## Execution Workflow

1. **Plan**: Build the node list and edges. Mark each node with verification, verification cost, and blast radius.
2. **Validate**: Check for cycles and unresolved dependencies.
3. **Select frontier**: Work only on nodes whose prerequisites are complete.
4. **Look ahead**: Confirm the current frontier, the next unlock, and the downstream conjunction or decision point.
5. **Parallelize carefully**: Delegate or run in parallel only among frontier nodes with disjoint blast radius, treating each independent path as a branch.
6. **Verify per node**: Run the node's verification before marking it complete, using targeted checks when they prove the node.
7. **Integrate at conjunctions**: Merge branches only after all prerequisite branch outputs are verified.
8. **Defer expensive checks deliberately**: If an expensive run is unnecessary now, add it as a later verification node with the reason for deferral.
9. **Update graph**: Add, split, reorder, or remove nodes as new facts appear.
10. **Final verify**: Run end-to-end checks that prove the final outcome, not just the individual nodes.

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
6. **Branch plan**: Independent subagent branches and their conjunction nodes.
7. **Lookahead**: Current frontier, next unlock, and downstream conjunction or decision point.
8. **Deferred expensive checks**: Commands intentionally postponed, with the reason and the node where they will run.
9. **Execution status**: Pending, in progress, verified, blocked.
10. **Final verification**: The integrated checks required before calling the task done.

## Quality Bar

- Prefer fewer, verifiable nodes over many vague tasks.
- Make verification concrete before implementation starts.
- Match verification cost to risk; do not spend expensive test runs when a targeted check is sufficient.
- Add skipped expensive runs as explicit downstream verification nodes, not as vague follow-up notes.
- Treat "no overlap" as a file/API/state constraint, not just a conceptual difference.
- Re-run the DAG after discoveries that change dependencies.
- Keep a live three-step lookahead and revise it when reality changes.
- Make branch merges explicit conjunction nodes with their own verification.
- Never mark a node complete from implementation alone; completion requires verification.
