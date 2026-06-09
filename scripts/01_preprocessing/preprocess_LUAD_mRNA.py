"""
Preprocess TCGA-LUAD mRNA expression matrix and optionally map Ensembl IDs to symbols.

Example:
python scripts/01_preprocessing/preprocess_LUAD_mRNA.py \
  --input data/raw/TCGA_LUAD_mRNA_counts.csv \
  --annotation data/raw/gencode_symbol_map.csv \
  --id-col ensembl_id --symbol-col gene_symbol \
  --output data/processed/LUAD_mRNA_log2cpm_symbols.csv
"""

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

import pandas as pd
from _utils import parse_args, read_table, write_table, collapse_by_symbol, log2_transform, LOGGER


def counts_to_cpm(df: pd.DataFrame) -> pd.DataFrame:
    col_sums = df.sum(axis=0).replace(0, pd.NA)
    return df.div(col_sums, axis=1) * 1_000_000


def main():
    parser = parse_args("Preprocess TCGA-LUAD mRNA expression data.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--annotation", default=None)
    parser.add_argument("--id-col", default="ensembl_id")
    parser.add_argument("--symbol-col", default="gene_symbol")
    parser.add_argument("--output", default="data/processed/LUAD_mRNA_log2cpm_symbols.csv")
    parser.add_argument("--index-col", default=0)
    parser.add_argument("--input-is-counts", action="store_true", default=True)
    args = parser.parse_args()

    expr = read_table(args.input)
    expr = expr.set_index(expr.columns[int(args.index_col)])

    if args.annotation:
        ann = read_table(args.annotation)
        expr = collapse_by_symbol(expr, ann, args.id_col, args.symbol_col)

    if args.input_is_counts:
        expr = counts_to_cpm(expr.astype(float))

    expr = log2_transform(expr)
    write_table(expr.reset_index().rename(columns={"index": "gene"}), args.output)
    LOGGER.info("Saved LUAD mRNA-derived gene matrix: %s", args.output)


if __name__ == "__main__":
    main()
