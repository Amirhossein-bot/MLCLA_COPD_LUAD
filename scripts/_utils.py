"""
Shared utility functions for the MLCLA-Net reproducibility workflow.

These helpers are intentionally lightweight and path-based so that each analysis
script can be run from the repository root after local data paths are configured.
"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
from typing import Iterable, Optional

import numpy as np
import pandas as pd
import yaml


def setup_logger(name: str = "MLCLA-Net") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("[%(levelname)s] %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


LOGGER = setup_logger()


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_yaml(path: str | Path) -> dict:
    path = Path(path)
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def ensure_parent(path: str | Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def read_table(path: str | Path, sheet_name: Optional[str] = None) -> pd.DataFrame:
    path = Path(path)
    if path.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(path, sheet_name=sheet_name)
    return pd.read_csv(path)


def write_table(df: pd.DataFrame, path: str | Path, index: bool = False) -> None:
    path = ensure_parent(path)
    if path.suffix.lower() in {".xlsx", ".xls"}:
        df.to_excel(path, index=index)
    else:
        df.to_csv(path, index=index)


def log2_transform(df: pd.DataFrame, pseudo_count: float = 1.0) -> pd.DataFrame:
    return np.log2(df.astype(float) + pseudo_count)


def quantile_normalize(df: pd.DataFrame) -> pd.DataFrame:
    """Quantile normalize columns of an expression matrix."""
    values = df.to_numpy(dtype=float)
    sorted_idx = np.argsort(values, axis=0)
    sorted_values = np.sort(values, axis=0)
    mean_ranks = sorted_values.mean(axis=1)
    normalized = np.zeros(values.shape, dtype=float)
    for col in range(values.shape[1]):
        normalized[sorted_idx[:, col], col] = mean_ranks
    return pd.DataFrame(normalized, index=df.index, columns=df.columns)


def collapse_by_symbol(
    expression: pd.DataFrame,
    annotation: pd.DataFrame,
    probe_col: str,
    symbol_col: str,
    agg: str = "mean",
) -> pd.DataFrame:
    """Map probe-level expression rows to gene/miRNA symbols and collapse duplicates."""
    ann = annotation[[probe_col, symbol_col]].dropna()
    ann[probe_col] = ann[probe_col].astype(str)
    ann[symbol_col] = ann[symbol_col].astype(str)

    expr = expression.copy()
    expr.index = expr.index.astype(str)
    expr = expr.loc[expr.index.intersection(ann[probe_col])]
    mapper = ann.set_index(probe_col)[symbol_col].to_dict()
    expr.index = expr.index.map(mapper)
    expr = expr[expr.index.notna()]
    expr = expr[expr.index.astype(str).str.strip() != ""]

    if agg == "median":
        return expr.groupby(expr.index).median()
    return expr.groupby(expr.index).mean()


def benjamini_hochberg(p_values: Iterable[float]) -> np.ndarray:
    p = np.asarray(list(p_values), dtype=float)
    n = len(p)
    order = np.argsort(p)
    ranked = p[order]
    adjusted = ranked * n / (np.arange(n) + 1)
    adjusted = np.minimum.accumulate(adjusted[::-1])[::-1]
    adjusted = np.clip(adjusted, 0, 1)
    out = np.empty(n, dtype=float)
    out[order] = adjusted
    return out


def parse_args(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--config", default="config/config.yaml", help="Path to project config YAML.")
    return parser
