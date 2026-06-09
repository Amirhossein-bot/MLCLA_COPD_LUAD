"""
Run Welch differential-expression analysis for COPD versus control.

Expression input:
- first column = feature ID
- remaining columns = samples

Metadata input:
- sample column
- group column with case/control labels
"""

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

import numpy as np
import pandas as pd
from scipy.stats import ttest_ind
from _utils import parse_args, read_table, write_table, benjamini_hochberg, LOGGER


def run_de(expr, meta, sample_col, group_col, case_label, control_label):
    expr = expr.set_index(expr.columns[0])
    case_samples = meta.loc[meta[group_col] == case_label, sample_col].astype(str).tolist()
    control_samples = meta.loc[meta[group_col] == control_label, sample_col].astype(str).tolist()
    case_samples = [s for s in case_samples if s in expr.columns]
    control_samples = [s for s in control_samples if s in expr.columns]

    rows = []
    for feature, values in expr.iterrows():
        x = values[case_samples].astype(float).dropna()
        y = values[control_samples].astype(float).dropna()
        if len(x) < 2 or len(y) < 2:
            continue
        stat, p = ttest_ind(x, y, equal_var=False, nan_policy="omit")
        rows.append({
            "feature": feature,
            "case_mean": x.mean(),
            "control_mean": y.mean(),
            "log2FC": x.mean() - y.mean(),
            "p_value": p
        })
    out = pd.DataFrame(rows)
    out["FDR"] = benjamini_hochberg(out["p_value"])
    return out.sort_values(["FDR", "p_value"])


def main():
    parser = parse_args("Differential expression for COPD.")
    parser.add_argument("--expression", required=True)
    parser.add_argument("--metadata", required=True)
    parser.add_argument("--sample-col", default="sample")
    parser.add_argument("--group-col", default="group")
    parser.add_argument("--case-label", default="COPD")
    parser.add_argument("--control-label", default="control")
    parser.add_argument("--output", default="results/differential_expression/COPD_DE_results.csv")
    args = parser.parse_args()

    expr = read_table(args.expression)
    meta = read_table(args.metadata)
    result = run_de(expr, meta, args.sample_col, args.group_col, args.case_label, args.control_label)
    write_table(result, args.output)
    LOGGER.info("Saved COPD DE results: %s", args.output)


if __name__ == "__main__":
    main()
