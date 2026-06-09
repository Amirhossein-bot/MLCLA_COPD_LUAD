"""
Summarize community-detection outputs across MLCLA-Net and baseline methods.
"""

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

import argparse
import pandas as pd
from _utils import read_table, write_table, LOGGER


def layer_of(node):
    return str(node).split("::", 1)[0]


def base_identifier(node):
    return str(node).split("::", 1)[-1]


def summarize(assignments, method):
    df = assignments.copy()
    df["layer"] = df["node"].map(layer_of)
    df["base_identifier"] = df["node"].map(base_identifier)
    total_communities = df["community"].nunique()
    largest = df.groupby("community").size().max()
    retained = 0
    shared = set()

    for _, sub in df.groupby("community"):
        base_layer_counts = sub.groupby("base_identifier")["layer"].nunique()
        shared_ids = base_layer_counts[base_layer_counts >= 3].index.tolist()
        if sub["layer"].nunique() >= 3 and len(shared_ids) >= 5:
            retained += 1
            shared.update(shared_ids)

    return {
        "method": method,
        "total_communities": total_communities,
        "largest_community_size": largest,
        "retained_communities": retained,
        "unique_shared_identifiers": len(shared),
    }


def main():
    parser = argparse.ArgumentParser(description="Compare community-detection methods.")
    parser.add_argument("--assignments", nargs="+", required=True, help="Assignment CSV files.")
    parser.add_argument("--methods", nargs="+", required=True, help="Method names.")
    parser.add_argument("--output", default="results/baseline_comparison/method_summary.csv")
    args = parser.parse_args()

    rows = []
    for path, method in zip(args.assignments, args.methods):
        rows.append(summarize(read_table(path), method))
    write_table(pd.DataFrame(rows), args.output)
    LOGGER.info("Saved method comparison summary: %s", args.output)


if __name__ == "__main__":
    main()
