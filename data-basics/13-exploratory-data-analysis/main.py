"""
Day 13 - Exploratory Data Analysis

Turns a raw employee-performance dataset into a structured EDA report:
shape and dtypes, missingness, descriptive statistics, correlations,
group comparisons, outlier detection, and a short list of plain-English
insights derived directly from the numbers.

Run directly for a full console EDA report:
    python main.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


class EDAExplorer:
    """Runs a structured exploratory analysis over a tabular dataset."""

    def __init__(self, csv_path: str | Path = "data/employee_performance.csv") -> None:
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
        return pd.read_csv(self.csv_path)

    # ------------------------------------------------------------------
    # Structure
    # ------------------------------------------------------------------
    def shape_and_dtypes(self) -> dict:
        """Row/column counts and a dtype breakdown."""
        return {
            "rows": self.df.shape[0],
            "columns": self.df.shape[1],
            "dtypes": self.df.dtypes.astype(str).to_dict(),
        }

    def missing_value_summary(self) -> pd.Series:
        """Count of missing values per column (zeros included, for transparency)."""
        return self.df.isna().sum()

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------
    def numeric_columns(self) -> list[str]:
        return self.df.select_dtypes(include="number").columns.tolist()

    def descriptive_stats(self) -> pd.DataFrame:
        """Standard descriptive statistics for all numeric columns."""
        return self.df[self.numeric_columns()].describe().round(2)

    def correlation_matrix(self) -> pd.DataFrame:
        """Pearson correlation matrix across numeric columns."""
        return self.df[self.numeric_columns()].corr().round(2)

    def top_correlations_with(self, target: str, n: int = 3) -> pd.Series:
        """The n strongest correlations (by absolute value) with a target column."""
        corr = self.correlation_matrix()[target].drop(target)
        return corr.reindex(corr.abs().sort_values(ascending=False).index).head(n)

    # ------------------------------------------------------------------
    # Group comparisons
    # ------------------------------------------------------------------
    def group_comparison(self, by: str, metric: str) -> pd.Series:
        """Mean of `metric` grouped by a categorical column, sorted descending."""
        return self.df.groupby(by)[metric].mean().sort_values(ascending=False).round(2)

    # ------------------------------------------------------------------
    # Outliers
    # ------------------------------------------------------------------
    def detect_outliers_iqr(self, column: str) -> pd.DataFrame:
        """Rows considered outliers in `column` via the 1.5 * IQR rule."""
        q1, q3 = self.df[column].quantile([0.25, 0.75])
        iqr = q3 - q1
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        return self.df[(self.df[column] < lower) | (self.df[column] > upper)]

    # ------------------------------------------------------------------
    # Insights
    # ------------------------------------------------------------------
    def key_insights(self) -> list[str]:
        """A short list of plain-English insights derived from the data."""
        insights = []

        by_dept = self.group_comparison("department", "performance_rating")
        insights.append(
            f"{by_dept.index[0]} has the highest average performance rating "
            f"({by_dept.iloc[0]})."
        )

        top_corr = self.top_correlations_with("performance_rating", n=1)
        feature, value = top_corr.index[0], top_corr.iloc[0]
        direction = "positively" if value > 0 else "negatively"
        insights.append(
            f"'{feature}' is the strongest driver of performance_rating, "
            f"correlated {direction} ({value})."
        )

        outliers = self.detect_outliers_iqr("monthly_sales")
        insights.append(
            f"{len(outliers)} employees are monthly_sales outliers "
            f"(1.5*IQR rule) and may warrant closer review."
        )

        remote_vs_office = self.df.groupby("remote_worker")["satisfaction_score"].mean().round(2)
        insights.append(
            f"Remote workers report an average satisfaction of "
            f"{remote_vs_office.get(True, float('nan'))}, versus "
            f"{remote_vs_office.get(False, float('nan'))} for office workers."
        )

        return insights

    # ------------------------------------------------------------------
    # Console report
    # ------------------------------------------------------------------
    def print_report(self) -> None:
        shape = self.shape_and_dtypes()

        print("=" * 60)
        print("EXPLORATORY DATA ANALYSIS REPORT")
        print("=" * 60)
        print(f"Rows x Columns: {shape['rows']} x {shape['columns']}")

        print("\nMissing values per column:")
        print(self.missing_value_summary().to_string())

        print("\nDescriptive statistics (numeric columns):")
        print(self.descriptive_stats().to_string())

        print("\nCorrelation matrix:")
        print(self.correlation_matrix().to_string())

        print("\nAverage performance_rating by department:")
        print(self.group_comparison("department", "performance_rating").to_string())

        print("\nKey insights:")
        for i, insight in enumerate(self.key_insights(), start=1):
            print(f"  {i}. {insight}")
        print("=" * 60)


if __name__ == "__main__":
    explorer = EDAExplorer()
    explorer.print_report()
