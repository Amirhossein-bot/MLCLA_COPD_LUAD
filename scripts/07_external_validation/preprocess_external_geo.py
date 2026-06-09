"""
Preprocess an external GEO validation expression matrix.
"""

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

import argparse
from _utils import read_table, write_table, collapse_by_symbol, log2_transform, LOGGER


def main():
    parser = argparse.ArgumentParser(description="Preprocess external GEO expression data.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--annotation", default=None)
    parser.add_argument("--probe-col", default="probe_id")
    parser.add_argument("--symbol-col", default="gene_symbol")
    parser.add_argument("--index-col", default=0)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    expr = read_table(args.input).set_index(read_table(args.input).columns[int(args.index_col)])
    if args.annotation:
        ann = read_table(args.annotation)
        expr = collapse_by_symbol(expr, ann, args.probe_col, args.symbol_col)
    expr = log2_transform(expr)
    write_table(expr.reset_index().rename(columns={"index": "gene"}), args.output)
    LOGGER.info("Saved processed external GEO matrix: %s", args.output)


if __name__ == "__main__":
    main()
