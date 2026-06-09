"""
Generate COPD heatmaps from processed COPD miRNA and gene expression matrices.
"""

from pathlib import Path
import argparse
import matplotlib.pyplot as plt
import pandas as pd


def main():
    parser = argparse.ArgumentParser(description="Generate COPD heatmaps from processed COPD miRNA and gene expression matrices.")
    parser.add_argument("--input", default=None, help="Input table for figure generation.")
    parser.add_argument("--output", default="results/figures/generate_figure2_COPD_heatmaps.png")
    args = parser.parse_args()

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)

    if args.input is None:
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.text(0.5, 0.5, "Generate COPD heatmaps from processed COPD miRNA and gene expression matrices.\nProvide --input to generate the final figure.", ha="center", va="center")
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
