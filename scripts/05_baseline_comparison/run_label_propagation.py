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
    parser = argparse.ArgumentParser(description="Run Label Propagation baseline.")
    parser.add_argument("--supra-edges", required=True)
    parser.add_argument("--output", default="results/baseline_comparison/label_propagation_assignments.csv")
    args = parser.parse_args()

    graph = load_graph(args.supra_edges)
    communities = list(nx.algorithms.community.asyn_lpa_communities(graph, weight="weight", seed=42))
    rows = []
    for i, comm in enumerate(communities):
        for node in comm:
            rows.append({"node": node, "community": f"LabelPropagation_{i}"})
    write_table(pd.DataFrame(rows), args.output)
    LOGGER.info("Saved Label Propagation assignments: %s", args.output)

if __name__ == "__main__":
    main()
