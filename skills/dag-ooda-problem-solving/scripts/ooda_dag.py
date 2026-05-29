#!/usr/bin/env -S uv run --with networkx --
"""
DAG + OODA helper: read nodes/edges (JSON), optional weights and node_types (and/or); output order, sources, sinks, layers, longest path, recommended first.
Input: stdin or file. JSON: {"nodes": [...], "edges": [[a,b],...], "weights": {...}, "node_types": {"id": "and"|"or"}}
"""
import json
import sys
from pathlib import Path

import networkx as nx

DEFAULT_IMPACT = 3
DEFAULT_EFFORT = 3
DEFAULT_NODE_TYPE = "and"


def score(impact: int | float, effort: int | float) -> float:
    """Priority score: impact / effort. Effort 0 treated as 1."""
    e = effort if effort >= 1 else 1
    return impact / e


def ready_nodes(G: nx.DiGraph, done: set[str], node_types: dict[str, str]) -> set[str]:
    """Nodes that are ready to execute: all predecessors done (AND) or any predecessor done (OR)."""
    result = set()
    for n in G.nodes():
        preds = set(G.predecessors(n))
        if not preds:
            result.add(n)
            continue
        node_type = node_types.get(n, DEFAULT_NODE_TYPE)
        if node_type == "and":
            if preds <= done:
                result.add(n)
        else:  # or
            if preds & done:
                result.add(n)
    return result


def satisfied_nodes(G: nx.DiGraph, done: set[str], node_types: dict[str, str]) -> set[str]:
    """Nodes that are satisfied (done or reachable under AND/OR): fixpoint of done + (AND: all preds satisfied, OR: any pred satisfied)."""
    sat = set(done)
    order = list(nx.topological_sort(G))
    changed = True
    while changed:
        changed = False
        for n in order:
            if n in sat:
                continue
            preds = set(G.predecessors(n))
            if not preds:
                continue
            node_type = node_types.get(n, DEFAULT_NODE_TYPE)
            if node_type == "and" and preds <= sat:
                sat.add(n)
                changed = True
            elif node_type == "or" and (preds & sat):
                sat.add(n)
                changed = True
    return sat


def main() -> None:
    if len(sys.argv) > 1:
        path = Path(sys.argv[1])
        data = json.loads(path.read_text())
    else:
        data = json.load(sys.stdin)

    nodes = data.get("nodes", [])
    edges = [tuple(e) for e in data.get("edges", [])]
    weights_map = data.get("weights", {})
    raw_types = data.get("node_types", {})
    node_types = {n: (raw_types.get(n, DEFAULT_NODE_TYPE).lower() or DEFAULT_NODE_TYPE) for n in nodes}
    for n in node_types:
        if node_types[n] not in ("and", "or"):
            node_types[n] = DEFAULT_NODE_TYPE
    done_set = set(data.get("done", []))

    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    if not nx.is_directed_acyclic_graph(G):
        print("ERROR: Graph has a cycle. Break cycles before proceeding.", file=sys.stderr)
        sys.exit(1)

    order = list(nx.topological_sort(G))
    sources = [n for n in G.nodes() if G.in_degree(n) == 0]
    sinks = [n for n in G.nodes() if G.out_degree(n) == 0]
    try:
        layers = list(nx.topological_generations(G))
    except Exception:
        layers = []
    try:
        longest = nx.dag_longest_path(G)
    except Exception:
        longest = []

    def get_impact_effort(node: str) -> tuple[float, float]:
        w = weights_map.get(node, {})
        imp = w.get("impact", DEFAULT_IMPACT)
        eff = w.get("effort", DEFAULT_EFFORT)
        return float(imp), float(eff)

    source_scores = []
    for n in sources:
        imp, eff = get_impact_effort(n)
        source_scores.append((n, imp, eff, score(imp, eff)))
    recommended = max(source_scores, key=lambda x: x[3])[0] if source_scores else ""

    print("TOPOLOGICAL_ORDER")
    for n in order:
        print(n)
    print("SOURCES")
    for n in sources:
        print(n)
    print("SINKS")
    for n in sinks:
        print(n)
    print("NODE_TYPES")
    for n in order:
        print(f"{n}\t{node_types.get(n, DEFAULT_NODE_TYPE)}")
    initial_ready = ready_nodes(G, set(), node_types)
    print("READY_INITIAL")
    for n in sorted(initial_ready):
        print(n)
    if done_set:
        ready_now = ready_nodes(G, done_set, node_types) - done_set
        print("READY_NOW")
        for n in sorted(ready_now):
            print(n)
        # Recommend next: score READY_NOW nodes (same impact/effort), pick best
        ready_scores = []
        for n in ready_now:
            imp, eff = get_impact_effort(n)
            ready_scores.append((n, imp, eff, score(imp, eff)))
        recommended_next = max(ready_scores, key=lambda x: x[3])[0] if ready_scores else ""
        print("RECOMMENDED_NEXT")
        print(recommended_next)
        # Goal reached when all sinks are satisfied (done or reachable under AND/OR)
        satisfied = satisfied_nodes(G, done_set, node_types)
        if sinks and set(sinks) <= satisfied:
            print("GOAL_REACHED")
            print("yes")
        else:
            print("GOAL_REACHED")
            print("no")
    print("LAYERS")
    for i, layer in enumerate(layers):
        print(f"layer_{i}\t" + "\t".join(sorted(layer)))
    print("LONGEST_PATH")
    for n in longest:
        print(n)
    print("SOURCE_SCORES")
    for n, imp, eff, sc in source_scores:
        print(f"{n}\timpact={imp}\teffort={eff}\tscore={sc:.2f}")
    print("RECOMMENDED_FIRST")
    print(recommended)


if __name__ == "__main__":
    main()
