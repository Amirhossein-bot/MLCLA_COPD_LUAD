"""
Run Welch differential-expression analysis for LUAD tumor versus normal samples.

Expression input:
- first column = feature ID
- remaining columns = samples

Metadata input:
- sample column
- group column with tumor/normal labels
"""

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

from differential_expression_COPD import run_de
from _utils import parse_args, read_table, write_table, LOGGER


def main():
    parser = parse_args("Differential expression for LUAD.")
    parser.add_argument("--expression", required=True)
    parser.add_argument("--metadata", required=True)
    parser.add_argument("--sample-col", default="sample")
    parser.add_argument("--group-col", default="group")
    parser.add_argument("--case-label", default="Tumor")
    parser.add_argument("--control-label", default="Normal")
    parser.add_argument("--output", default="results/differential_expression/LUAD_DE_results.csv")
    args = parser.parse_args()

    expr = read_table(args.expression)
    meta = read_table(args.metadata)
    result = run_de(expr, meta, args.sample_col, args.group_col, args.case_label, args.control_label)
    write_table(result, args.output)
    LOGGER.info("Saved LUAD DE results: %s", args.output)


if __name__ == "__main__":
    main()
