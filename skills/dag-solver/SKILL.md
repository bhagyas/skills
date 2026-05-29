---
name: dag-solver
description: Solve complex tasks by decomposing them into a directed acyclic graph of independently verifiable work nodes. Use when a task has dependencies, can be split into testable subproblems, benefits from topological ordering, or can safely delegate independent branches to subagents without overlap or direct dependency.
---

# DAG Solver

Use a directed acyclic graph (DAG) to turn a complex task into independently verifiable work nodes, execute them in dependency order, and delegate only when branches are genuinely independent.

## Core Rule

Every node must be small enough to verify on its own.

A valid node has:
- **Goal**: one concrete outcome.
- **Inputs**: files, data, decisions, or prior nodes it depends on.
- **Output**: the artifact or state it produces.
- **Verification**: a command, inspection, test, assertion, or acceptance check that proves the node is done.
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
Delegate: yes/no, with reason
```

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

## Execution Workflow

1. **Plan**: Build the node list and edges. Mark each node with verification and blast radius.
2. **Validate**: Check for cycles and unresolved dependencies.
3. **Select frontier**: Work only on nodes whose prerequisites are complete.
4. **Parallelize carefully**: Delegate or run in parallel only among frontier nodes with disjoint blast radius.
5. **Verify per node**: Run the node's verification before marking it complete.
6. **Integrate**: After a layer completes, run checks that cover interactions between completed nodes.
7. **Update graph**: Add, split, or remove nodes as new facts appear.
8. **Final verify**: Run end-to-end checks that prove the final outcome, not just the individual nodes.

## Handling Cycles

If you find a cycle, the task is not ready to execute as a DAG.

Resolve it by:
- Clarifying which edge is a real prerequisite versus a preference.
- Collapsing tightly coupled nodes into one node with a single verification check.
- Time-slicing feedback into stages, such as `design v1 -> implement v1 -> evaluate -> design v2`.

## Output Format

When applying this skill, produce:

1. **Nodes**: Each node with goal, output, verification, and blast radius.
2. **Edges**: `A -> B` dependencies.
3. **Cycle check**: `acyclic: yes/no`.
4. **Layers**: Topological execution layers.
5. **Delegation plan**: Which nodes can run in subagents and why; which must stay local and why.
6. **Execution status**: Pending, in progress, verified, blocked.
7. **Final verification**: The integrated checks required before calling the task done.

## Quality Bar

- Prefer fewer, verifiable nodes over many vague tasks.
- Make verification concrete before implementation starts.
- Treat "no overlap" as a file/API/state constraint, not just a conceptual difference.
- Re-run the DAG after discoveries that change dependencies.
- Never mark a node complete from implementation alone; completion requires verification.
