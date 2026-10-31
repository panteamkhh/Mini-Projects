"""Unit tests for SalesVisualizer (Day 14 - Data Visualization)."""

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pytest

from generate_data import generate_dataset
from main import SalesVisualizer


@pytest.fixture
def visualizer(tmp_path) -> SalesVisualizer:
    csv_path = tmp_path / "sales_performance.csv"
    generate_dataset(n_rows=120, seed=3).to_csv(csv_path, index=False)
    return SalesVisualizer(csv_path=csv_path)


def test_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        SalesVisualizer(csv_path=tmp_path / "nope.csv")


def test_plot_revenue_trend_returns_figure(visualizer):
    fig = visualizer.plot_revenue_trend()
    assert isinstance(fig, plt.Figure)
    plt.close(fig)


def test_plot_revenue_by_category_returns_figure(visualizer):
    fig = visualizer.plot_revenue_by_category()
    assert isinstance(fig, plt.Figure)
    plt.close(fig)


def test_plot_order_value_distribution_returns_figure(visualizer):
    fig = visualizer.plot_order_value_distribution()
    assert isinstance(fig, plt.Figure)
    plt.close(fig)


def test_plot_experience_vs_revenue_returns_figure(visualizer):
    fig = visualizer.plot_experience_vs_revenue()
    assert isinstance(fig, plt.Figure)
    plt.close(fig)


def test_plot_correlation_heatmap_returns_figure(visualizer):
    fig = visualizer.plot_correlation_heatmap()
    assert isinstance(fig, plt.Figure)
    plt.close(fig)


def test_save_all_creates_all_files(visualizer, tmp_path):
    output_dir = tmp_path / "charts"
    paths = visualizer.save_all(output_dir=output_dir)

    assert len(paths) == 5
    for path in paths:
        assert path.exists()
        assert path.stat().st_size > 0


def test_save_all_creates_output_dir_if_missing(visualizer, tmp_path):
    output_dir = tmp_path / "nested" / "charts"
    assert not output_dir.exists()

    visualizer.save_all(output_dir=output_dir)
    assert output_dir.exists()
