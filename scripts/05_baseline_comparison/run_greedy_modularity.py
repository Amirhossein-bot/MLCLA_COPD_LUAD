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

def main():
    parser = argparse.ArgumentParser(description="Run Greedy Modularity baseline.")
    parser.add_argument("--supra-edges", required=True)
    parser.add_argument("--output", default="results/baseline_comparison/greedy_modularity_assignments.csv")
    args = parser.parse_args()

    graph = load_graph(args.supra_edges)
    communities = nx.algorithms.community.greedy_modularity_communities(graph, weight="weight")
    rows = []
    for i, comm in enumerate(communities):
        for node in comm:
            rows.append({"node": node, "community": f"Greedy_{i}"})
    write_table(pd.DataFrame(rows), args.output)
    LOGGER.info("Saved Greedy Modularity assignments: %s", args.output)

if __name__ == "__main__":
    main()
