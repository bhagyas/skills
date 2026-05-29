---
name: dag-thinking
description: Solve problems by modeling them as a directed acyclic graph (DAG). Use when tasks have dependencies, prerequisites, ordering constraints, pipelines, workflows, causal graphs, or when you need to detect cycles, find a topological order, identify critical paths, or simplify dependency structure.
---

# DAG Thinking (Directed Acyclic Graph)

Use a **directed acyclic graph (DAG)** as the core representation for any problem that involves *dependencies*.
Reference: https://grokipedia.com/page/Directed_acyclic_graph

## 0) Decide if DAG framing fits
Use this when you can phrase the problem as:
- “X must happen **before** Y”
- “Y depends on X”
- “If X changes, downstream things affected are …”

If there are **feedback loops** that matter, you may have cycles; handle them explicitly (see Cycle handling).

## 1) Build the graph
### 1A) Define nodes
Pick a consistent unit:
- tasks, steps, tickets, files, components, decisions, assumptions, people, etc.

### 1B) Define edges
Use one direction consistently:
- **X → Y** means “X is a prerequisite of Y” (Y depends on X)

### 1C) Capture metadata
For each node, store:
- owner, status, estimate/cost, risk, notes

## 2) Validate the DAG
### 2A) Detect cycles (must do)
If cycles exist, you don’t have a DAG yet.

Cycle handling (pick one):
- **Break the cycle** by clarifying dependency direction (often one edge is “nice-to-have”, not required)
- **Collapse** a strongly-connected set into a single “super-node” (treat as one unit)
- **Time-slice**: convert feedback into iterative stages (v1 → v2)

## NetworkX powers

When applying this skill, use NetworkX to implement the steps above:

| Power | API / approach | Use when |
|-------|----------------|----------|
| **Build DAG** | `nx.DiGraph()`, `add_nodes_from()`, `add_edges_from()` | Modeling nodes and dependencies (1A, 1B). |
| **Validate acyclic** | `nx.is_directed_acyclic_graph(G)` | Before any sort or path; break cycles if False (2A). |
| **Execution order** | `list(nx.topological_sort(G))` | Proposed order and phases (3). |
| **Frontier / next actions** | `[n for n in G.nodes() if G.in_degree(n) == 0]` | “What do we do next?” (6). |
| **Critical path** | `nx.dag_longest_path(G)` or with `weight="weight"` | Longest chain; critical path + slack (4, 5). |
| **In-degree / out-degree** | `G.in_degree(n)`, `G.out_degree(n)` | Prerequisites count, dependents count. |
| **Ancestors / descendants** | `nx.ancestors(G, n)`, `nx.descendants(G, n)` | “What blocks this?” / “What breaks if we change X?” (6). |
| **Transitive reduction** | `nx.transitive_reduction(G)` | Minimal edge set that preserves reachability (4A). |
| **Subgraph** | `G.subgraph(nodes)` or `nx.subgraph_view()` | Restrict to a subset; layers or phases. |
| **Weighted DAG** | Set edge or node `weight`; use in `dag_longest_path(G, weight="weight")` | Durations, cost, or impact along paths (5). |

**Minimal snippet (create, validate, order):**

```python
import networkx as nx
G = nx.DiGraph()
G.add_nodes_from(["a", "b", "c"])
G.add_edges_from([("a", "b"), ("b", "c")])
assert nx.is_directed_acyclic_graph(G)
order = list(nx.topological_sort(G))
sources = [n for n in G.nodes() if G.in_degree(n) == 0]
```

Run Python (e.g. `uv run --with networkx python -c "..."`) when the graph is non-trivial or the user wants concrete order, sources, or longest path.

## 3) Compute order (topological sorting)
Produce a valid execution order:
- pick any node with no remaining prerequisites (in-degree 0)
- execute/remove it
- repeat

If multiple nodes are available, choose by:
- shortest-first (unblock quickly)
- highest impact
- critical path urgency (see below)

## 4) Reduce graph complexity (optional but powerful)
### 4A) Transitive reduction mindset
If A→B and B→C exist, then A→C is often redundant. Prefer the **minimal** edge set that preserves reachability.

Practical heuristic:
- keep the edge only if removing it would change what’s reachable

### 4B) Cluster by layers
Group nodes by “distance from sources” to create phases:
- Phase 0: sources
- Phase 1: depends only on Phase 0
- …

## 5) Find the critical path (for planning)
If nodes have durations/estimates:
- compute the longest path from sources to sinks
- that path dictates the minimum completion time

Output:
- critical path nodes
- slack nodes (can be delayed without affecting finish)

## 6) Answer typical questions with DAG outputs
- **What do we do next?** → topological frontier (available nodes)
- **What blocks this task?** → ancestors of node
- **What breaks if we change X?** → descendants of node
- **How do we simplify?** → transitive reduction / merge nodes
- **Where are we stuck?** → cycle detection, no available nodes

## 7) Output format (default)
When you apply this skill, produce:
1) **Nodes** (with 1-line descriptions)
2) **Edges** (X → Y)
3) **Cycle check** result
4) **Proposed order** (phases or linear list)
5) (Optional) **Critical path** + slack
6) **Next actions**

## Quick prompts to ask the user (only if needed)
- “What counts as ‘done’ for each node?”
- “Is X truly required for Y, or just preferred?”
- “Do any dependencies create a loop?”
- “Do you care about fastest completion, lowest risk, or minimal context switching?”
