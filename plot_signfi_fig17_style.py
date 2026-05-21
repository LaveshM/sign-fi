#!/usr/bin/env python3
"""Plot SignFi CNN results in a style similar to Fig. 17(a) and 17(c)."""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt


def load_metrics(csv_path: Path) -> dict[str, float]:
    metrics: dict[str, float] = {}
    with csv_path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            metrics[row["Metric"]] = float(row["Value"])
    return metrics


def main() -> None:
    csv_path = Path("signfi_cnn_results.csv")
    out_png_path = Path("signfi_fig17a_17c_like.png")
    out_pdf_path = Path("signfi_fig17a_17c_like.pdf")

    metrics = load_metrics(csv_path)

    users = ["1", "2", "3", "4", "5"]
    within_vals = [
        metrics["within_user1_5fold_mean"],
        metrics["within_user2_5fold_mean"],
        metrics["within_user3_5fold_mean"],
        metrics["within_user4_5fold_mean"],
        metrics["within_user5_5fold_mean"],
    ]
    loso_vals = [
        metrics["loso_user1_out"],
        metrics["loso_user2_out"],
        metrics["loso_user3_out"],
        metrics["loso_user4_out"],
        metrics["loso_user5_out"],
    ]

    mixed_mean = metrics["mixed_5fold_mean"]
    loso_mean = metrics["loso_mean"]

    plt.rcParams.update(
        {
            "font.size": 11,
            "axes.titlesize": 12,
            "axes.labelsize": 11,
            "xtick.labelsize": 10,
            "ytick.labelsize": 10,
        }
    )

    fig, axes = plt.subplots(1, 2, figsize=(6.6, 2.5), dpi=220, sharey=True)

    # Fig. 17(a)-like: per-user within-user accuracy + overall bars.
    ax = axes[0]
    labels_a = users + ["Mean"]
    vals_a = within_vals + [mixed_mean]
    colors_a = ["#c62828"] * 5 + ["#f2c230"]
    bars_a = ax.bar(labels_a, vals_a, color=colors_a)
    ax.set_title("Within-subject and 5-fold CV Mean")
    ax.set_xlabel("Subject")
    ax.set_ylabel("Accuracy")
    ax.set_ylim(0, 1.0)
    ax.grid(axis="y", linestyle="--", linewidth=0.8, alpha=0.35)
    ax.tick_params(axis="x", rotation=0)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Fig. 17(c)-like: LOSO per-user accuracy + mean.
    ax = axes[1]
    labels_c = users + ["Mean"]
    vals_c = loso_vals + [loso_mean]
    colors_c = ["#c62828"] * 5 + ["#f2c230"]
    bars_c = ax.bar(labels_c, vals_c, color=colors_c)
    ax.set_title("LOSO Accuracy")
    ax.set_xlabel("Subject")
    ax.set_ylabel("")
    ax.set_ylim(0, 1.0)
    ax.grid(axis="y", linestyle="--", linewidth=0.8, alpha=0.35)
    ax.tick_params(axis="x", rotation=0)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout(pad=0.5, w_pad=0.8)
    fig.savefig(out_png_path, bbox_inches="tight")
    fig.savefig(out_pdf_path, bbox_inches="tight")
    print(f"Saved plot to {out_png_path.resolve()}")
    print(f"Saved plot to {out_pdf_path.resolve()}")


if __name__ == "__main__":
    main()
