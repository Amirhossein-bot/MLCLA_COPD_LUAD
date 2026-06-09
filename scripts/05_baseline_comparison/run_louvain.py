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

import community as community_louvain

def main():
    parser = argparse.ArgumentParser(description="Run Louvain baseline.")
    parser.add_argument("--supra-edges", required=True)
    parser.add_argument("--output", default="results/baseline_comparison/louvain_assignments.csv")
    args = parser.parse_args()
    graph = load_graph(args.supra_edges)
    partition = community_louvain.best_partition(graph, weight="weight", random_state=42)
    out = pd.DataFrame({"node": list(partition), "community": ["Louvain_" + str(v) for v in partition.values()]})
    write_table(out, args.output)
    LOGGER.info("Saved Louvain assignments: %s", args.output)

if __name__ == "__main__":
    main()
