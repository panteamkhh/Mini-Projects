"""Unit tests for StatisticalAnalyzer (Day 17 - Statistical Analysis)."""

import numpy as np
import pandas as pd
import pytest

from generate_data import generate_dataset
from main import StatisticalAnalyzer


@pytest.fixture
def analyzer(tmp_path) -> StatisticalAnalyzer:
    csv_path = tmp_path / "ab_test_results.csv"
    generate_dataset(n_per_group=300, seed=9).to_csv(csv_path, index=False)
    return StatisticalAnalyzer(csv_path=csv_path)


def test_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        StatisticalAnalyzer(csv_path=tmp_path / "nope.csv")


def test_invalid_groups_raises(tmp_path):
    bad_csv = tmp_path / "bad.csv"
    pd.DataFrame({
        "user_id": ["A-1", "B-1"],
        "group": ["control", "variant_b"],
        "session_duration": [100, 110],
        "converted": [0, 1],
        "revenue": [0, 20],
    }).to_csv(bad_csv, index=False)

    with pytest.raises(ValueError):
        StatisticalAnalyzer(csv_path=bad_csv)


def test_descriptive_stats_has_both_groups(analyzer):
    stats_df = analyzer.descriptive_stats_by_group()
    assert set(stats_df.index) == {"control", "treatment"}
    assert "conversion_rate" in stats_df.columns


def test_test_conversion_rate_keys(analyzer):
    result = analyzer.test_conversion_rate()
    expected_keys = {
        "control_rate", "treatment_rate", "absolute_lift", "relative_lift_pct",
        "z_statistic", "p_value", "significant_at_0_05",
    }
    assert set(result.keys()) == expected_keys
    assert isinstance(result["significant_at_0_05"], (bool, np.bool_))


def test_conversion_rate_treatment_higher_than_control(analyzer):
    result = analyzer.test_conversion_rate()
    assert result["treatment_rate"] >= result["control_rate"]


def test_test_mean_difference_keys(analyzer):
    result = analyzer.test_mean_difference("session_duration")
    expected_keys = {
        "metric", "control_mean", "treatment_mean", "mean_difference",
        "levene_p_value", "equal_variances_assumed", "t_statistic",
        "p_value", "significant_at_0_05",
    }
    assert set(result.keys()) == expected_keys


def test_test_mean_difference_p_value_in_valid_range(analyzer):
    result = analyzer.test_mean_difference("session_duration")
    assert 0 <= result["p_value"] <= 1


def test_confidence_interval_bounds_around_mean(analyzer):
    lower, upper = analyzer.confidence_interval("session_duration", "control")
    control_mean = analyzer._group("control")["session_duration"].mean()
    assert lower < control_mean < upper
    assert isinstance(lower, float)
    assert isinstance(upper, float)


def test_confidence_interval_narrower_with_lower_confidence(analyzer):
    ci_95 = analyzer.confidence_interval("session_duration", "control", confidence=0.95)
    ci_80 = analyzer.confidence_interval("session_duration", "control", confidence=0.80)
    width_95 = ci_95[1] - ci_95[0]
    width_80 = ci_80[1] - ci_80[0]
    assert width_80 < width_95


def test_cohens_d_is_finite_float(analyzer):
    d = analyzer.cohens_d("session_duration")
    assert isinstance(d, float)
    assert d == d  # not NaN


def test_cohens_d_positive_when_treatment_mean_higher(analyzer):
    d = analyzer.cohens_d("session_duration")
    control_mean = analyzer._group("control")["session_duration"].mean()
    treatment_mean = analyzer._group("treatment")["session_duration"].mean()
    if treatment_mean > control_mean:
        assert d > 0
