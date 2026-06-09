"""
Summarize enrichment outputs for supplementary tables and figures.
"""

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

import argparse
from _utils import read_table, write_table, LOGGER


def main():
    parser = argparse.ArgumentParser(description="Summarize enrichment results.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--fdr-col", default="Adjusted P-value")
    parser.add_argument("--top-n", type=int, default=20)
    parser.add_argument("--output", default="results/enrichment/enrichment_summary.csv")
    args = parser.parse_args()

    df = read_table(args.input)
    df = df.sort_values(args.fdr_col).head(args.top_n)
    write_table(df, args.output)
    LOGGER.info("Saved enrichment summary: %s", args.output)


if __name__ == "__main__":
    main()
