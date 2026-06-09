"""
Run Enrichr/GSEApy enrichment for MLCLA-derived mRNA/gene candidates.
"""

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

import argparse
import gseapy as gp
import pandas as pd
from _utils import read_table, write_table, LOGGER


def main():
    parser = argparse.ArgumentParser(description="Run enrichment for MLCLA candidates.")
    parser.add_argument("--candidates", required=True)
    parser.add_argument("--gene-col", default="gene")
    parser.add_argument("--output", default="results/enrichment/mlcla_enrichment_results.csv")
    parser.add_argument("--libraries", nargs="+", default=["GO_Biological_Process_2023", "KEGG_2021_Human", "Reactome_2022"])
    args = parser.parse_args()

    genes = read_table(args.candidates)[args.gene_col].dropna().astype(str).unique().tolist()
    all_results = []
    for library in args.libraries:
        enr = gp.enrichr(gene_list=genes, gene_sets=library, organism="human", outdir=None)
        res = enr.results
        res["library"] = library
        all_results.append(res)
    out = pd.concat(all_results, ignore_index=True)
    write_table(out, args.output)
    LOGGER.info("Saved MLCLA enrichment results: %s", args.output)


if __name__ == "__main__":
    main()
