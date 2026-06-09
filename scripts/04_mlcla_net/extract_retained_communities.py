"""
Extract retained MLCLA communities containing all three layers and at least a
minimum number of shared base identifiers.
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


def main():
    parser = argparse.ArgumentParser(description="Extract retained MLCLA communities.")
    parser.add_argument("--assignments", required=True)
    parser.add_argument("--min-shared", type=int, default=5)
    parser.add_argument("--required-layers", type=int, default=3)
    parser.add_argument("--output", default="results/mlcla_net/retained_communities.csv")
    args = parser.parse_args()

    df = read_table(args.assignments)
    df["layer"] = df["node"].map(layer_of)
    df["base_identifier"] = df["node"].map(base_identifier)

    summaries = []
    for comm, sub in df.groupby("community"):
        layers = sorted(sub["layer"].unique())
        base_layer_counts = sub.groupby("base_identifier")["layer"].nunique()
        shared_ids = base_layer_counts[base_layer_counts >= args.required_layers].index.tolist()
        if len(layers) >= args.required_layers and len(shared_ids) >= args.min_shared:
            summaries.append({
                "community": comm,
                "total_nodes": len(sub),
                "layers": ";".join(layers),
                "shared_identifier_count": len(shared_ids),
                "shared_identifiers": ";".join(shared_ids)
            })

    out = pd.DataFrame(summaries).sort_values("total_nodes", ascending=False)
    write_table(out, args.output)
    LOGGER.info("Saved retained communities: %s", args.output)


if __name__ == "__main__":
    main()
