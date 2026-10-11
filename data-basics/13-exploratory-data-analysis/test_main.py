"""Unit tests for EDAExplorer (Day 13 - Exploratory Data Analysis)."""

import pandas as pd
import pytest

from generate_data import generate_dataset
from main import EDAExplorer


@pytest.fixture
def explorer(tmp_path) -> EDAExplorer:
    csv_path = tmp_path / "employee_performance.csv"
    generate_dataset(n_rows=150, seed=5).to_csv(csv_path, index=False)
    return EDAExplorer(csv_path=csv_path)


def test_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        EDAExplorer(csv_path=tmp_path / "does_not_exist.csv")


def test_shape_and_dtypes(explorer):
    shape = explorer.shape_and_dtypes()
    assert shape["rows"] == 150
    assert shape["columns"] == 10
    assert "department" in shape["dtypes"]


def test_missing_value_summary_all_zero(explorer):
    summary = explorer.missing_value_summary()
    assert (summary == 0).all()


def test_numeric_columns_excludes_categoricals(explorer):
    numeric = explorer.numeric_columns()
    assert "department" not in numeric
    assert "region" not in numeric
    assert "performance_rating" in numeric


def test_descriptive_stats_shape(explorer):
    stats = explorer.descriptive_stats()
    assert "mean" in stats.index
    assert "std" in stats.index
    assert set(stats.columns) == set(explorer.numeric_columns())


def test_correlation_matrix_is_symmetric_and_diagonal_ones(explorer):
    corr = explorer.correlation_matrix()
    assert (corr.values.diagonal() == 1.0).all()
    assert (corr.values == corr.values.T).all()


def test_top_correlations_with_returns_n_rows(explorer):
    top = explorer.top_correlations_with("performance_rating", n=2)
    assert len(top) == 2
    assert "performance_rating" not in top.index


def test_group_comparison_sorted_descending(explorer):
    result = explorer.group_comparison("department", "performance_rating")
    assert list(result) == sorted(result, reverse=True)


def test_detect_outliers_iqr_returns_subset(explorer):
    outliers = explorer.detect_outliers_iqr("monthly_sales")
    assert isinstance(outliers, pd.DataFrame)
    assert len(outliers) <= len(explorer.df)


def test_key_insights_returns_nonempty_strings(explorer):
    insights = explorer.key_insights()
    assert len(insights) == 4
    assert all(isinstance(i, str) and len(i) > 0 for i in insights)


def test_key_insights_mentions_real_department(explorer):
    insights = explorer.key_insights()
    real_departments = set(explorer.df["department"].unique())
    assert any(dept in insights[0] for dept in real_departments)
