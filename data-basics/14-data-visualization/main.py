"""
Day 14 - Data Visualization

Turns the sales-performance dataset into a small set of
story-driven charts (not just "a plot of the data"): a trend,
a category comparison, a distribution comparison, a relationship,
and an overview correlation heatmap. Each chart is built to answer
one specific question, styled to be presentation-ready.

Run directly to generate and save every chart as a PNG:
    python main.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # headless-safe backend

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_style("whitegrid")


class SalesVisualizer:
    """Builds a set of business-relevant charts from a sales dataset."""

    def __init__(self, csv_path: str | Path = "data/sales_performance.csv") -> None:
        self.csv_path = Path(csv_path)
        self.df: pd.DataFrame = self._load()

    # ------------------------------------------------------------------
    # Loading
    # ------------------------------------------------------------------
    def _load(self) -> pd.DataFrame:
        if not self.csv_path.exists():
            raise FileNotFoundError(
                f"Dataset not found at {self.csv_path}. "
                "Run `python generate_data.py` first."
            )
        return pd.read_csv(self.csv_path, parse_dates=["order_date"])

    # ------------------------------------------------------------------
    # Charts
    # ------------------------------------------------------------------
    def plot_revenue_trend(self) -> plt.Figure:
        """Monthly revenue trend — is the business growing?"""
        monthly = self.df.set_index("order_date")["revenue"].resample("ME").sum()

        fig, ax = plt.subplots(figsize=(9, 5))
        ax.plot(monthly.index, monthly.values, marker="o", color="#2E5EAA", linewidth=2)
        ax.set_title("Monthly Revenue Trend", fontsize=14, fontweight="bold")
        ax.set_xlabel("Month")
        ax.set_ylabel("Total Revenue ($)")
        fig.autofmt_xdate()
        fig.tight_layout()
        return fig

    def plot_revenue_by_category(self) -> plt.Figure:
        """Which product category drives the most revenue?"""
        by_category = (
            self.df.groupby("product_category")["revenue"].sum().sort_values()
        )

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.barh(by_category.index, by_category.values, color="#4C956C")
        ax.set_title("Total Revenue by Product Category", fontsize=14, fontweight="bold")
        ax.set_xlabel("Total Revenue ($)")
        fig.tight_layout()
        return fig

    def plot_order_value_distribution(self) -> plt.Figure:
        """How does order value vary across customer segments?"""
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.boxplot(
            data=self.df, x="customer_segment", y="revenue",
            hue="customer_segment", palette="Set2", legend=False, ax=ax,
        )
        ax.set_title("Order Value Distribution by Customer Segment", fontsize=14, fontweight="bold")
        ax.set_xlabel("Customer Segment")
        ax.set_ylabel("Revenue ($)")
        fig.tight_layout()
        return fig

    def plot_experience_vs_revenue(self) -> plt.Figure:
        """Does sales-rep experience relate to order revenue?"""
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.regplot(
            data=self.df, x="sales_rep_experience", y="revenue",
            ax=ax, scatter_kws={"alpha": 0.3, "s": 20}, line_kws={"color": "#D62828"},
        )
        ax.set_title("Sales Rep Experience vs. Order Revenue", fontsize=14, fontweight="bold")
        ax.set_xlabel("Sales Rep Experience (years)")
        ax.set_ylabel("Revenue ($)")
        fig.tight_layout()
        return fig

    def plot_correlation_heatmap(self) -> plt.Figure:
        """Overview of how all numeric variables relate to each other."""
        numeric_df = self.df.select_dtypes(include="number")

        fig, ax = plt.subplots(figsize=(6, 5))
        sns.heatmap(numeric_df.corr(), annot=True, fmt=".2f", cmap="coolwarm", center=0, ax=ax)
        ax.set_title("Correlation Heatmap", fontsize=14, fontweight="bold")
        fig.tight_layout()
        return fig

    # ------------------------------------------------------------------
    # Save everything
    # ------------------------------------------------------------------
    def save_all(self, output_dir: str | Path = "charts") -> list[Path]:
        """Generate every chart and save it as a PNG. Returns the saved paths."""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        charts = {
            "revenue_trend.png": self.plot_revenue_trend,
            "revenue_by_category.png": self.plot_revenue_by_category,
            "order_value_distribution.png": self.plot_order_value_distribution,
            "experience_vs_revenue.png": self.plot_experience_vs_revenue,
            "correlation_heatmap.png": self.plot_correlation_heatmap,
        }

        saved_paths = []
        for filename, chart_fn in charts.items():
            fig = chart_fn()
            path = output_dir / filename
            fig.savefig(path, dpi=150)
            plt.close(fig)
            saved_paths.append(path)

        return saved_paths


if __name__ == "__main__":
    visualizer = SalesVisualizer()
    paths = visualizer.save_all()
    print("Saved charts:")
    for path in paths:
        print(f"  - {path}")
