from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

import argparse
import networkx as nx
import pandas as pd
from _utils import read_table, write_table, LOGGER

def load_graph(edge_file):
    edges = read_table(edge_file)
    graph = nx.Graph()
    for _, row in edges.iterrows():
        graph.add_edge(row["source"], row["target"], weight=abs(float(row.get("weight", 1.0))))
    return graph

import igraph as ig
import leidenalg

def main():
    parser = argparse.ArgumentParser(description="Run Leiden baseline.")
    parser.add_argument("--supra-edges", required=True)
    parser.add_argument("--output", default="results/baseline_comparison/leiden_assignments.csv")
    args = parser.parse_args()

    nx_graph = load_graph(args.supra_edges)
    nodes = list(nx_graph.nodes())
    idx = {n: i for i, n in enumerate(nodes)}
    edges = [(idx[u], idx[v]) for u, v in nx_graph.edges()]
    weights = [nx_graph[u][v].get("weight", 1.0) for u, v in nx_graph.edges()]
    graph = ig.Graph(n=len(nodes), edges=edges, directed=False)
    graph.es["weight"] = weights

    part = leidenalg.find_partition(graph, leidenalg.ModularityVertexPartition, weights="weight", seed=42)
    memberships = part.membership
    out = pd.DataFrame({"node": nodes, "community": ["Leiden_" + str(c) for c in memberships]})
    write_table(out, args.output)
    LOGGER.info("Saved Leiden assignments: %s", args.output)

if __name__ == "__main__":
    main()
