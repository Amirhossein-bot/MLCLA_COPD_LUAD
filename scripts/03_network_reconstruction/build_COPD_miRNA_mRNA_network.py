from __future__ import annotations

import itertools
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from _utils import read_table, write_table, benjamini_hochberg, LOGGER


def load_matrix(path):
    df = read_table(path)
    return df.set_index(df.columns[0])


def align_columns(a, b):
    common = [c for c in a.columns if c in set(b.columns)]
    if len(common) < 3:
        raise ValueError("Fewer than three matched samples are available.")
    return a[common], b[common]


def mirna_mrna_edges(mirna, mrna, abs_r=0.4, fdr=None):
    rows = []
    for mir, x in mirna.iterrows():
        xv = x.astype(float)
        for gene, y in mrna.iterrows():
            rho, p = spearmanr(xv, y.astype(float), nan_policy="omit")
            if np.isnan(rho):
                continue
            rows.append({"source": mir, "target": gene, "spearman_r": rho, "p_value": p})
    out = pd.DataFrame(rows)
    out["FDR"] = benjamini_hochberg(out["p_value"])
    keep = out["spearman_r"].abs() >= abs_r
    if fdr is not None:
        keep &= out["FDR"] <= fdr
    return out.loc[keep].sort_values(["FDR", "p_value"])


def gene_coexpression_edges(expr, abs_r=0.6, fdr=None):
    genes = list(expr.index)
    rows = []
    for i, j in itertools.combinations(range(len(genes)), 2):
        g1, g2 = genes[i], genes[j]
        rho, p = spearmanr(expr.iloc[i].astype(float), expr.iloc[j].astype(float), nan_policy="omit")
        if np.isnan(rho):
            continue
        rows.append({"source": g1, "target": g2, "spearman_r": rho, "p_value": p})
    out = pd.DataFrame(rows)
    out["FDR"] = benjamini_hochberg(out["p_value"])
    keep = out["spearman_r"].abs() >= abs_r
    if fdr is not None:
        keep &= out["FDR"] <= fdr
    return out.loc[keep].sort_values(["FDR", "p_value"])

import argparse

def main():
    parser = argparse.ArgumentParser(description="Build COPD miRNA-mRNA association network.")
    parser.add_argument("--mirna", required=True)
    parser.add_argument("--mrna", required=True)
    parser.add_argument("--abs-r", type=float, default=0.4)
    parser.add_argument("--fdr", type=float, default=None)
    parser.add_argument("--output", default="results/networks/COPD_miRNA_mRNA_edges.csv")
    args = parser.parse_args()

    mirna = load_matrix(args.mirna)
    mrna = load_matrix(args.mrna)
    mirna, mrna = align_columns(mirna, mrna)
    edges = mirna_mrna_edges(mirna, mrna, abs_r=args.abs_r, fdr=args.fdr)
    edges["network"] = "COPD_miRNA_mRNA_association"
    write_table(edges, args.output)
    LOGGER.info("Saved COPD miRNA-mRNA edges: %s", args.output)

if __name__ == "__main__":
    main()
