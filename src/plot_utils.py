"""
plot_utils.py
─────────────
Shared plotting helpers — consistent style across all notebooks.
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import numpy as np

# ── Global style ────────────────────────────────────────────────────────────
PALETTE = {
    "sj": "#E63946",   # vibrant red
    "iq": "#457B9D",   # teal blue
    "accent": "#F4A261",
    "bg": "#1A1A2E",
    "grid": "#2A2A4A",
    "text": "#E0E0E0",
}

def set_project_style():
    """Apply a consistent dark-theme style to all plots."""
    plt.rcParams.update({
        "figure.facecolor": PALETTE["bg"],
        "axes.facecolor": PALETTE["bg"],
        "axes.edgecolor": PALETTE["grid"],
        "axes.labelcolor": PALETTE["text"],
        "text.color": PALETTE["text"],
        "xtick.color": PALETTE["text"],
        "ytick.color": PALETTE["text"],
        "grid.color": PALETTE["grid"],
        "grid.alpha": 0.4,
        "font.family": "sans-serif",
        "font.size": 11,
        "axes.titlesize": 14,
        "axes.titleweight": "bold",
        "figure.titlesize": 16,
        "figure.titleweight": "bold",
        "legend.facecolor": PALETTE["bg"],
        "legend.edgecolor": PALETTE["grid"],
        "legend.fontsize": 10,
        "figure.dpi": 120,
    })
    sns.set_palette([PALETTE["sj"], PALETTE["iq"], PALETTE["accent"]])


def city_label(code):
    return {"sj": "San Juan", "iq": "Iquitos"}.get(code, code)


def city_color(code):
    return PALETTE.get(code, PALETTE["accent"])


def save_fig(fig, name, figures_dir=None):
    """Save figure to the project-level figures/ directory as PNG."""
    from pathlib import Path
    if figures_dir is None:
        figures_dir = Path(__file__).resolve().parent.parent / "figures"
    out = Path(figures_dir)
    out.mkdir(exist_ok=True)
    fig.savefig(out / f"{name}.png", bbox_inches="tight", dpi=150,
                facecolor=fig.get_facecolor())
    print(f"  ✅ Saved → {out / name}.png")
