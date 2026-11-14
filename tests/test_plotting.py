
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import pytest
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.colors import to_hex

from tennis_career import plot_age_difference


@pytest.fixture
def sample_df():
    """Create sample tennis match data without network requests."""
    return pd.DataFrame({
        "player_age": [20.0, 21.0, 22.0, 23.0],
        "age_difference": [-5.0, 2.0, -3.0, 4.0],
        "result": ["W", "L", "W", "L"]
    })


def test_plot_returns_figure_and_axes(sample_df):
    """Check that the function returns Matplotlib objects."""
    fig, ax = plot_age_difference(sample_df, "Serena Williams")

    try:
        assert isinstance(fig, Figure)
        assert isinstance(ax, Axes)
    finally:
        plt.close(fig)


def test_plot_contains_wins_and_losses(sample_df):
    """Check that wins and losses are plotted separately."""
    fig, ax = plot_age_difference(sample_df, "Serena Williams")

    try:
        assert len(ax.collections) == 2
        assert len(ax.collections[0].get_offsets()) == 2
        assert len(ax.collections[1].get_offsets()) == 2
    finally:
        plt.close(fig)


def test_plot_uses_correct_coordinates(sample_df):
    """Check that x is player age and y is age difference."""
    fig, ax = plot_age_difference(sample_df, "Serena Williams")

    try:
        win_points = ax.collections[0].get_offsets()
        loss_points = ax.collections[1].get_offsets()

        assert win_points.tolist() == [
            [20.0, -5.0], [22.0, -3.0]
        ]
        assert loss_points.tolist() == [
            [21.0, 2.0], [23.0, 4.0]
        ]
    finally:
        plt.close(fig)


def test_plot_uses_correct_colors(sample_df):
    """Check that wins are cyan and losses are purple."""
    fig, ax = plot_age_difference(sample_df, "Serena Williams")

    try:
        win_color = to_hex(ax.collections[0].get_facecolors()[0])
        loss_color = to_hex(ax.collections[1].get_facecolors()[0])

        assert win_color == "#43c6e8"
        assert loss_color == "#96358c"
    finally:
        plt.close(fig)


def test_plot_title(sample_df):
    """Check that the title includes the player and age range."""
    fig, ax = plot_age_difference(sample_df, "Serena Williams")

    try:
        assert ax.get_title() == (
            "Serena Williams’s Professional Matches, Age 20 to 23"
        )
    finally:
        plt.close(fig)


def test_plot_reference_line(sample_df):
    """Check that the plot has a horizontal line at zero."""
    fig, ax = plot_age_difference(sample_df, "Serena Williams")

    try:
        zero_lines = [
            line for line in ax.lines
            if all(y == 0 for y in line.get_ydata())
        ]

        assert len(zero_lines) >= 1
    finally:
        plt.close(fig)


def test_plot_legend(sample_df):
    """Check that the legend identifies wins and losses."""
    fig, ax = plot_age_difference(sample_df, "Serena Williams")

    try:
        legend = ax.get_legend()
        labels = [text.get_text() for text in legend.get_texts()]

        assert "Match Williams won" in labels
        assert "Match lost" in labels
    finally:
        plt.close(fig)


def test_plot_axis_formatting(sample_df):
    """Check that the plot uses the intended axis formatting."""
    fig, ax = plot_age_difference(sample_df, "Serena Williams")

    try:
        assert ax.get_ylim() == (-20, 22)
        assert ax.xaxis.get_ticks_position() == "top"
        assert "Same age" in [
            tick.get_text() for tick in ax.get_yticklabels()
        ]
    finally:
        plt.close(fig)
