"""
Prepare TCGA-LUAD survival table with OS time and event.
"""

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

import argparse
from _utils import read_table, write_table, LOGGER


def main():
    parser = argparse.ArgumentParser(description="Prepare TCGA-LUAD survival table.")
    parser.add_argument("--clinical", required=True)
    parser.add_argument("--patient-col", default="patient_id")
    parser.add_argument("--time-col", default="OS_time")
    parser.add_argument("--event-col", default="OS_event")
    parser.add_argument("--output", default="results/survival/TCGA_LUAD_OS_prepared.csv")
    args = parser.parse_args()

    clin = read_table(args.clinical)
    out = clin[[args.patient_col, args.time_col, args.event_col]].copy()
    out = out.rename(columns={args.patient_col: "patient_id", args.time_col: "OS_time", args.event_col: "OS_event"})
    out = out.dropna()
    out = out[out["OS_time"] > 0]
    write_table(out, args.output)
    LOGGER.info("Saved prepared survival table: %s", args.output)


if __name__ == "__main__":
    main()
