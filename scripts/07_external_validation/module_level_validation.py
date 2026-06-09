"""
Module-level external validation using Fisher's exact test.
"""

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

import argparse
import pandas as pd
from scipy.stats import fisher_exact
from _utils import read_table, write_table, benjamini_hochberg, LOGGER


def main():
    parser = argparse.ArgumentParser(description="Run module-level external validation.")
    parser.add_argument("--module-candidates", required=True, help="Columns: module,gene")
    parser.add_argument("--validation-results", required=True, help="Columns: gene,FDR")
    parser.add_argument("--universe", required=True, help="One-column gene universe file")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    mods = read_table(args.module_candidates)
    val = read_table(args.validation_results)
    universe = set(read_table(args.universe).iloc[:, 0].astype(str))
    supported = set(val.loc[val["FDR"] < 0.05, "gene"].astype(str))

    rows = []
    for module, sub in mods.groupby("module"):
        genes = set(sub["gene"].astype(str)) & universe
        a = len(genes & supported)
        b = len(genes - supported)
        c = len((supported & universe) - genes)
        d = len(universe - genes - supported)
        _, p = fisher_exact([[a, b], [c, d]], alternative="greater")
        rows.append({"module": module, "module_genes": len(genes), "supported_genes": a, "p_value": p})
    out = pd.DataFrame(rows)
    out["FDR"] = benjamini_hochberg(out["p_value"])
    write_table(out.sort_values(["FDR", "p_value"]), args.output)
    LOGGER.info("Saved module-level validation results: %s", args.output)


if __name__ == "__main__":
    main()
