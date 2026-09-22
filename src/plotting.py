"""Visualization helpers for the before/after NDVI comparison."""
import matplotlib.pyplot as plt
import numpy as np


def plot_before_after_diff(pre_ndvi, post_ndvi, diff, titles=None, out_path=None):
    titles = titles or ("Pre-Helene NDVI", "Post-Helene NDVI", "NDVI Change (post - pre)")
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    for ax, data, title in zip(axes[:2], (pre_ndvi, post_ndvi), titles[:2]):
        im = ax.imshow(data, cmap="RdYlGn", vmin=-0.2, vmax=0.9)
        ax.set_title(title)
        ax.axis("off")
        fig.colorbar(im, ax=ax, fraction=0.04, label="NDVI")

    im = axes[2].imshow(diff, cmap="RdBu", vmin=-0.6, vmax=0.6)
    axes[2].set_title(titles[2])
    axes[2].axis("off")
    fig.colorbar(im, ax=axes[2], fraction=0.04, label="Δ NDVI")

    fig.tight_layout()
    if out_path:
        fig.savefig(out_path, dpi=200, bbox_inches="tight")
    return fig


def plot_change_histogram(diff, loss_threshold=-0.15, out_path=None):
    values = np.asarray(diff).ravel()
    values = values[~np.isnan(values)]
    loss_pct = (values < loss_threshold).mean() * 100

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(values, bins=100, color="#4a7c59")
    ax.axvline(loss_threshold, color="crimson", linestyle="--",
               label=f"Loss threshold ({loss_threshold})")
    ax.set_xlabel("Δ NDVI (post - pre)")
    ax.set_ylabel("Pixel count")
    ax.set_title(f"NDVI Change Distribution — {loss_pct:.1f}% of pixels show notable canopy loss")
    ax.legend()

    if out_path:
        fig.savefig(out_path, dpi=200, bbox_inches="tight")
    return fig, loss_pct
