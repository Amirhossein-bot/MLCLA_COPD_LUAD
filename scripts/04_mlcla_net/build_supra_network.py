"""
Build a three-layer supra-network edge list from disease-specific network edge tables.
"""

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

import argparse
import pandas as pd
from _utils import read_table, write_table, LOGGER


def prefix_edges(df, prefix, layer_name):
    out = df.copy()
    out["source"] = prefix + "::" + out["source"].astype(str)
    out["target"] = prefix + "::" + out["target"].astype(str)
    out["layer"] = layer_name
    if "weight" not in out.columns:
        out["weight"] = out.get("spearman_r", 1.0)
    return out[["source", "target", "weight", "layer"]]


def main():
    parser = argparse.ArgumentParser(description="Build MLCLA-Net supra-network.")
    parser.add_argument("--copd-gene", required=True)
    parser.add_argument("--mirna-cross", required=True)
    parser.add_argument("--luad-gene", required=True)
    parser.add_argument("--output", default="results/mlcla_net/supra_edges.csv")
    args = parser.parse_args()

    copd = prefix_edges(read_table(args.copd_gene), "COPD_gene", "COPD_gene_coexpression")
    cross = prefix_edges(read_table(args.mirna_cross), "miRNA_cross", "miRNA_associated_cross_regulatory")
    luad = prefix_edges(read_table(args.luad_gene), "LUAD_gene", "LUAD_gene_coexpression")

    supra = pd.concat([copd, cross, luad], ignore_index=True)
    write_table(supra, args.output)
    LOGGER.info("Saved supra-network edge list: %s", args.output)


if __name__ == "__main__":
    main()
