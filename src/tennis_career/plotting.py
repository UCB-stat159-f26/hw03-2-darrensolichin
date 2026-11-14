
import math

import matplotlib.pyplot as plt
import numpy as np


def _plot_matches(ax, df, surname):
    """Plot wins and losses using NYT-style colors."""
    for result, color, label in [
        ("W", "#43C6E8", f"Match {surname} won"),
        ("L", "#96358C", "Match lost")
    ]:
        subset = df[df["result"] == result]
        ax.scatter(
            subset["player_age"],
            subset["age_difference"],
            color=color,
            s=22,
            alpha=0.9,
            label=label,
            edgecolors="none",
            zorder=3
        )


def _format_axes(ax, min_age, max_age):
    """Set axis limits, ticks, gridlines, and reference line."""
    ax.set_xlim(min_age - 0.5, max_age + 1)
    ax.set_ylim(-20, 22)
    ax.set_xticks(np.arange(min_age, max_age + 1, 2))
    ax.set_yticks(np.arange(-20, 21, 10))
    ax.set_yticklabels(["−20", "−10", "Same age", "+10", "+20 years"])
    ax.xaxis.tick_top()
    ax.grid(True, color="#E6E6E6", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.axhline(0, color="#999999", linewidth=1.2, zorder=2)
    ax.set_xlabel("")
    ax.set_ylabel("")


def _add_side_labels(ax):
    """Add descriptive labels beside the y-axis."""
    ax.text(
        -0.04, 0.82, "Older\nthan\nopponent",
        transform=ax.transAxes,
        ha="right", va="center",
        color="gray", fontsize=11
    )
    ax.text(
        -0.04, 0.12, "Younger\nthan\nopponent",
        transform=ax.transAxes,
        ha="right", va="center",
        color="gray", fontsize=11
    )


def _add_age_label(ax, surname):
    """Add the player's age label above the x-axis."""
    ax.text(
        0.01, 1.10, f"{surname}’s\nage:",
        transform=ax.transAxes,
        ha="left", va="bottom",
        color="gray", fontsize=11
    )


def _format_title_legend(ax, player_name, min_age, max_age):
    """Format the title and legend."""
    ax.set_title(
        f"{player_name}’s Professional Matches, Age {min_age} to {max_age}",
        fontsize=17, fontweight="bold", pad=85
    )
    ax.legend(
        loc="lower center",
        bbox_to_anchor=(0.5, 1.09),
        ncol=2, frameon=False, fontsize=11
    )


def _finalize_plot(fig, ax):
    """Remove borders and adjust figure spacing."""
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(
        axis="both", length=0,
        colors="gray", labelsize=11, pad=8
    )
    fig.subplots_adjust(
        left=0.20, right=0.95,
        top=0.72, bottom=0.10
    )


def plot_age_difference(df, player_name="Player"):
    """
    Create a NYT-style scatter plot of tennis match age differences.

    Parameters
    ----------
    df : pandas.DataFrame
        Match data returned by get_player_matches().
    player_name : str
        Name of the tennis player.

    Returns
    -------
    fig, ax : matplotlib Figure and Axes
        The generated scatter plot.
    """
    surname = player_name.split()[-1]
    min_age = math.floor(df["player_age"].min())
    max_age = math.ceil(df["player_age"].max())

    fig, ax = plt.subplots(figsize=(14, 8))

    _plot_matches(ax, df, surname)
    _format_axes(ax, min_age, max_age)
    _add_side_labels(ax)
    _add_age_label(ax, surname)
    _format_title_legend(ax, player_name, min_age, max_age)
    _finalize_plot(fig, ax)

    return fig, ax
