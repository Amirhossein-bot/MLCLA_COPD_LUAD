"""
Preprocess COPD miRNA microarray expression data.

Expected input:
- rows = probes or miRNA IDs
- columns = samples
- optional platform annotation mapping probe IDs to miRNA symbols

Example:
python scripts/01_preprocessing/preprocess_COPD_miRNA.py \
  --input data/raw/COPD_miRNA_expression.csv \
  --annotation data/raw/GPL7723_annotation.csv \
  --probe-col ProbeID --symbol-col miRNA_symbol \
  --output data/processed/COPD_miRNA_expression_normalized.csv
"""

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

from _utils import parse_args, read_table, write_table, quantile_normalize, log2_transform, collapse_by_symbol, LOGGER


def main():
    parser = parse_args("Preprocess COPD miRNA expression data.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--annotation", default=None)
    parser.add_argument("--probe-col", default="probe_id")
    parser.add_argument("--symbol-col", default="symbol")
    parser.add_argument("--output", default="data/processed/COPD_miRNA_expression_normalized.csv")
    parser.add_argument("--index-col", default=0)
    parser.add_argument("--log2", action="store_true", default=True)
    parser.add_argument("--quantile", action="store_true", default=True)
    args = parser.parse_args()

    expr = read_table(args.input)
    expr = expr.set_index(expr.columns[int(args.index_col)])

    if args.annotation:
        ann = read_table(args.annotation)
        expr = collapse_by_symbol(expr, ann, args.probe_col, args.symbol_col)

    if args.log2:
        expr = log2_transform(expr)
    if args.quantile:
        expr = quantile_normalize(expr)

    write_table(expr.reset_index().rename(columns={"index": "miRNA"}), args.output)
    LOGGER.info("Saved normalized COPD miRNA matrix: %s", args.output)


if __name__ == "__main__":
    main()
