"""
Preprocess TCGA-LUAD miRNA expression matrix.

Expected input:
- rows = miRNAs
- columns = TCGA samples
- values = raw counts, RPM, or already normalized values depending on source

Example:
python scripts/01_preprocessing/preprocess_LUAD_miRNA.py \
  --input data/raw/TCGA_LUAD_miRNA_counts.csv \
  --output data/processed/LUAD_miRNA_log2rpm.csv
"""

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

import pandas as pd
from _utils import parse_args, read_table, write_table, log2_transform, LOGGER


def counts_to_rpm(df: pd.DataFrame) -> pd.DataFrame:
    col_sums = df.sum(axis=0).replace(0, pd.NA)
    return df.div(col_sums, axis=1) * 1_000_000


def main():
    parser = parse_args("Preprocess TCGA-LUAD miRNA expression data.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", default="data/processed/LUAD_miRNA_log2rpm.csv")
    parser.add_argument("--index-col", default=0)
    parser.add_argument("--input-is-counts", action="store_true", default=True)
    args = parser.parse_args()

    expr = read_table(args.input)
    expr = expr.set_index(expr.columns[int(args.index_col)])

    if args.input_is_counts:
        expr = counts_to_rpm(expr.astype(float))

    expr = log2_transform(expr)
    write_table(expr.reset_index().rename(columns={"index": "miRNA"}), args.output)
    LOGGER.info("Saved LUAD miRNA log2RPM matrix: %s", args.output)


if __name__ == "__main__":
    main()
