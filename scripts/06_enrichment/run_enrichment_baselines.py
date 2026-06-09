"""
Run enrichment for candidate sets extracted from baseline community-detection methods.
"""

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

import argparse
import pandas as pd
from run_enrichment_mlcla import gp
from _utils import read_table, write_table, LOGGER


def main():
    parser = argparse.ArgumentParser(description="Run enrichment for baseline candidate sets.")
    parser.add_argument("--candidate-files", nargs="+", required=True)
    parser.add_argument("--methods", nargs="+", required=True)
    parser.add_argument("--gene-col", default="gene")
    parser.add_argument("--output", default="results/enrichment/baseline_enrichment_results.csv")
    parser.add_argument("--libraries", nargs="+", default=["GO_Biological_Process_2023", "KEGG_2021_Human", "Reactome_2022"])
    args = parser.parse_args()

    all_results = []
    for file_path, method in zip(args.candidate_files, args.methods):
        genes = read_table(file_path)[args.gene_col].dropna().astype(str).unique().tolist()
        for library in args.libraries:
            enr = gp.enrichr(gene_list=genes, gene_sets=library, organism="human", outdir=None)
            res = enr.results
            res["library"] = library
            res["method"] = method
            all_results.append(res)
    out = pd.concat(all_results, ignore_index=True)
    write_table(out, args.output)
    LOGGER.info("Saved baseline enrichment results: %s", args.output)


if __name__ == "__main__":
    main()
