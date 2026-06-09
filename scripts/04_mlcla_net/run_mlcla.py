"""
Run a lightweight MLCLA-style adaptive label propagation routine.

This implementation is a reproducibility scaffold. If the manuscript used a
separate optimized implementation, replace this file with the exact final code.
"""

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

import argparse
import random
from collections import defaultdict, Counter

import numpy as np
import pandas as pd

from _utils import read_table, write_table, LOGGER


def base_identifier(node):
    return str(node).split("::", 1)[-1]


def build_adjacency(edges):
    adj = defaultdict(list)
    for _, row in edges.iterrows():
        s, t, w = row["source"], row["target"], abs(float(row.get("weight", 1.0)))
        adj[s].append((t, w))
        adj[t].append((s, w))
    return adj


def run_mlcla(edges, max_iter=1000, lam=0.1, patience=40, seed=42):
    random.seed(seed)
    np.random.seed(seed)

    nodes = sorted(set(edges["source"]).union(edges["target"]))
    adj = build_adjacency(edges)

    labels = {n: "BASE::" + base_identifier(n) for n in nodes}
    best_labels = labels.copy()
    best_objective = -np.inf
    stale = 0
    history = []

    same_base = defaultdict(list)
    for n in nodes:
        same_base[base_identifier(n)].append(n)

    for it in range(1, max_iter + 1):
        changes = 0
        for n in nodes:
            candidate_scores = Counter()
            for neigh, w in adj.get(n, []):
                candidate_scores[labels[neigh]] += w
            for counterpart in same_base[base_identifier(n)]:
                if counterpart != n:
                    candidate_scores[labels[counterpart]] += lam
            if not candidate_scores:
                continue
            new_label = candidate_scores.most_common(1)[0][0]
            if new_label != labels[n]:
                labels[n] = new_label
                changes += 1

        # Simple objective proxy: weighted edge agreement + same-base alignment.
        agree = 0.0
        total = 0.0
        for _, row in edges.iterrows():
            w = abs(float(row.get("weight", 1.0)))
            total += w
            if labels[row["source"]] == labels[row["target"]]:
                agree += w
        edge_agreement = agree / total if total else 0.0

        align_hits = 0
        align_total = 0
        for group in same_base.values():
            if len(group) > 1:
                align_total += len(group) - 1
                ref = labels[group[0]]
                align_hits += sum(labels[g] == ref for g in group[1:])
        alignment = align_hits / align_total if align_total else 0.0

        objective = edge_agreement + lam * alignment
        history.append({
            "iteration": it,
            "objective": objective,
            "edge_agreement": edge_agreement,
            "interlayer_alignment": alignment,
            "label_changes": changes
        })

        if objective > best_objective:
            best_objective = objective
            best_labels = labels.copy()
            stale = 0
        else:
            stale += 1

        if stale >= patience:
            break

    assignments = pd.DataFrame({"node": list(best_labels), "community": list(best_labels.values())})
    history = pd.DataFrame(history)
    return assignments, history


def main():
    parser = argparse.ArgumentParser(description="Run MLCLA-Net community detection.")
    parser.add_argument("--supra-edges", required=True)
    parser.add_argument("--max-iterations", type=int, default=1000)
    parser.add_argument("--lambda-value", type=float, default=0.1)
    parser.add_argument("--patience", type=int, default=40)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--assignments-output", default="results/mlcla_net/community_assignments.csv")
    parser.add_argument("--history-output", default="results/mlcla_net/optimization_history.csv")
    args = parser.parse_args()

    edges = read_table(args.supra_edges)
    assignments, history = run_mlcla(edges, args.max_iterations, args.lambda_value, args.patience, args.seed)
    write_table(assignments, args.assignments_output)
    write_table(history, args.history_output)
    LOGGER.info("Saved MLCLA assignments and optimization history.")


if __name__ == "__main__":
    main()
