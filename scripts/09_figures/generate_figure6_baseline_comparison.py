"""
Generate baseline comparison summary figure.
"""

from pathlib import Path
import argparse
import matplotlib.pyplot as plt
import pandas as pd


def main():
    parser = argparse.ArgumentParser(description="Generate baseline comparison summary figure.")
    parser.add_argument("--input", default=None, help="Input table for figure generation.")
    parser.add_argument("--output", default="results/figures/generate_figure6_baseline_comparison.png")
    args = parser.parse_args()

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)

    if args.input is None:
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.text(0.5, 0.5, "Generate baseline comparison summary figure.\nProvide --input to generate the final figure.", ha="center", va="center")
        ax.axis("off")
        fig.savefig(args.output, dpi=300, bbox_inches="tight")
        return

    df = pd.read_csv(args.input) if not args.input.endswith(".xlsx") else pd.read_excel(args.input)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.text(0.5, 0.5, "Figure-generation template\nCustomize plotting logic for manuscript figure.", ha="center", va="center")
    ax.axis("off")
    fig.savefig(args.output, dpi=300, bbox_inches="tight")


if __name__ == "__main__":
    main()
