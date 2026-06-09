"""
Generate MLCLA convergence figure from optimization history.
"""

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

import argparse
import pandas as pd
import matplotlib.pyplot as plt
from _utils import read_table, LOGGER


def main():
    parser = argparse.ArgumentParser(description="Plot MLCLA convergence profile.")
    parser.add_argument("--history", required=True)
    parser.add_argument("--iteration-col", default="iteration")
    parser.add_argument("--objective-col", default="objective")
    parser.add_argument("--best-iteration", type=int, default=282)
    parser.add_argument("--output", default="results/figures/Figure5_MLCLA_convergence_profile.png")
    args = parser.parse_args()

    hist = read_table(args.history)
    best_row = hist.loc[hist[args.iteration_col].sub(args.best_iteration).abs().idxmin()]

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    ax.plot(hist[args.iteration_col], hist[args.objective_col], linewidth=2)
    ax.axvline(args.best_iteration, linestyle="--", linewidth=1.4)
    ax.scatter([best_row[args.iteration_col]], [best_row[args.objective_col]], s=65, zorder=5)
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Global objective score")
    ax.set_title("MLCLA-Net convergence profile", loc="left", fontweight="bold")
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.savefig(args.output, dpi=600, bbox_inches="tight")
    LOGGER.info("Saved convergence figure: %s", args.output)


if __name__ == "__main__":
    main()
