"""
Preprocess COPD mRNA microarray expression data and map probes to gene symbols.

Example:
python scripts/01_preprocessing/preprocess_COPD_mRNA.py \
  --input data/raw/COPD_mRNA_expression.csv \
  --annotation data/raw/GPL4133_annotation.csv \
  --probe-col ProbeID --symbol-col GeneSymbol \
  --output data/processed/COPD_mRNA_expression_normalized.csv
"""

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

from _utils import parse_args, read_table, write_table, quantile_normalize, log2_transform, collapse_by_symbol, LOGGER


def main():
    parser = parse_args("Preprocess COPD mRNA expression data.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--annotation", required=True)
    parser.add_argument("--probe-col", default="probe_id")
    parser.add_argument("--symbol-col", default="symbol")
    parser.add_argument("--output", default="data/processed/COPD_mRNA_expression_normalized.csv")
    parser.add_argument("--index-col", default=0)
    args = parser.parse_args()

    expr = read_table(args.input)
    expr = expr.set_index(expr.columns[int(args.index_col)])
    ann = read_table(args.annotation)

    expr = collapse_by_symbol(expr, ann, args.probe_col, args.symbol_col)
    expr = log2_transform(expr)
    expr = quantile_normalize(expr)

    write_table(expr.reset_index().rename(columns={"index": "gene"}), args.output)
    LOGGER.info("Saved normalized COPD mRNA-derived gene matrix: %s", args.output)


if __name__ == "__main__":
    main()
