from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

import argparse
import pandas as pd
from lifelines import CoxPHFitter
from lifelines.statistics import logrank_test
from _utils import read_table, write_table, benjamini_hochberg, LOGGER


def run_survival(expression, clinical, candidates, feature_col):
    expr = read_table(expression).set_index(read_table(expression).columns[0])
    clin = read_table(clinical)
    candidates = read_table(candidates)[feature_col].dropna().astype(str).tolist()
    rows = []
    for gene in candidates:
        if gene not in expr.index:
            continue
        values = expr.loc[gene].astype(float)
        df = clin.copy()
        df["expression"] = df["patient_id"].map(values.to_dict())
        df = df.dropna(subset=["expression", "OS_time", "OS_event"])
        if df.shape[0] < 10:
            continue
        median = df["expression"].median()
        df["high_expression"] = (df["expression"] >= median).astype(int)

        cph = CoxPHFitter()
        cph.fit(df[["OS_time", "OS_event", "high_expression"]], duration_col="OS_time", event_col="OS_event")
        hr = float(cph.hazard_ratios_["high_expression"])
        p_cox = float(cph.summary.loc["high_expression", "p"])

        high = df[df["high_expression"] == 1]
        low = df[df["high_expression"] == 0]
        lr = logrank_test(high["OS_time"], low["OS_time"], high["OS_event"], low["OS_event"])

        rows.append({"feature": gene, "n": len(df), "hazard_ratio": hr, "cox_p": p_cox, "logrank_p": lr.p_value})
    out = pd.DataFrame(rows)
    out["cox_FDR"] = benjamini_hochberg(out["cox_p"])
    out["logrank_FDR"] = benjamini_hochberg(out["logrank_p"])
    return out

def main():
    parser = argparse.ArgumentParser(description="Run mRNA/gene survival analysis.")
    parser.add_argument("--expression", required=True)
    parser.add_argument("--clinical", required=True)
    parser.add_argument("--candidates", required=True)
    parser.add_argument("--gene-col", default="gene")
    parser.add_argument("--output", default="results/survival/mrna_survival_results.csv")
    args = parser.parse_args()
    out = run_survival(args.expression, args.clinical, args.candidates, args.gene_col)
    write_table(out, args.output)
    LOGGER.info("Saved mRNA survival results: %s", args.output)

if __name__ == "__main__":
    main()
