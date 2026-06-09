"""
Candidate-level external validation using Welch's t-test.
"""

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

import pandas as pd
from scipy.stats import ttest_ind
import argparse

from _utils import read_table, write_table, benjamini_hochberg, LOGGER


def main():
    parser = argparse.ArgumentParser(description="Validate MLCLA candidates in an external dataset.")
    parser.add_argument("--expression", required=True)
    parser.add_argument("--metadata", required=True)
    parser.add_argument("--candidates", required=True)
    parser.add_argument("--gene-col", default="gene")
    parser.add_argument("--sample-col", default="sample")
    parser.add_argument("--group-col", default="group")
    parser.add_argument("--case-label", required=True)
    parser.add_argument("--control-label", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    expr = read_table(args.expression).set_index(read_table(args.expression).columns[0])
    meta = read_table(args.metadata)
    candidates = read_table(args.candidates)[args.gene_col].dropna().astype(str).tolist()
    candidates = [g for g in candidates if g in expr.index]

    case_samples = meta.loc[meta[args.group_col] == args.case_label, args.sample_col].astype(str).tolist()
    control_samples = meta.loc[meta[args.group_col] == args.control_label, args.sample_col].astype(str).tolist()
    case_samples = [s for s in case_samples if s in expr.columns]
    control_samples = [s for s in control_samples if s in expr.columns]

    rows = []
    for gene in candidates:
        x = expr.loc[gene, case_samples].astype(float).dropna()
        y = expr.loc[gene, control_samples].astype(float).dropna()
        if len(x) < 2 or len(y) < 2:
            continue
        stat, p = ttest_ind(x, y, equal_var=False)
        rows.append({"gene": gene, "log2FC": x.mean() - y.mean(), "p_value": p})
    out = pd.DataFrame(rows)
    out["FDR"] = benjamini_hochberg(out["p_value"])
    out["support"] = out.apply(lambda r: "FDR-supported" if r["FDR"] < 0.05 else ("nominal" if r["p_value"] < 0.05 else "not_supported"), axis=1)
    write_table(out.sort_values(["FDR", "p_value"]), args.output)
    LOGGER.info("Saved external validation results: %s", args.output)


if __name__ == "__main__":
    main()
