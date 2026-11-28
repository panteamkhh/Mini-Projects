"""
Day 17 - Statistical Analysis

Runs a proper statistical analysis of an A/B test — not just
"treatment mean > control mean" but actual hypothesis testing:
a two-proportion z-test for conversion rate, an independent t-test
(with a variance-equality check) for session duration, confidence
intervals, and an effect size, ending in a plain-English verdict.

Run directly for a full console report:
    python main.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats


class StatisticalAnalyzer:
    """Runs hypothesis tests comparing a control and treatment group."""

    def __init__(self, csv_path: str | Path = "data/ab_test_results.csv") -> None:
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
        df = pd.read_csv(self.csv_path)
        if set(df["group"].unique()) != {"control", "treatment"}:
            raise ValueError("Expected exactly two groups: 'control' and 'treatment'.")
        return df

    def _group(self, name: str) -> pd.DataFrame:
        return self.df[self.df["group"] == name]

    # ------------------------------------------------------------------
    # Descriptives
    # ------------------------------------------------------------------
    def descriptive_stats_by_group(self) -> pd.DataFrame:
        """Sample size, conversion rate, and mean session duration/revenue per group."""
        return self.df.groupby("group").agg(
            n=("user_id", "count"),
            conversion_rate=("converted", "mean"),
            avg_session_duration=("session_duration", "mean"),
            avg_revenue=("revenue", "mean"),
        ).round(4)

    # ------------------------------------------------------------------
    # Conversion rate: two-proportion z-test
    # ------------------------------------------------------------------
    def test_conversion_rate(self) -> dict:
        """Two-proportion z-test: is the conversion rate difference significant?"""
        control, treatment = self._group("control"), self._group("treatment")

        n1, n2 = len(control), len(treatment)
        x1, x2 = control["converted"].sum(), treatment["converted"].sum()
        p1, p2 = x1 / n1, x2 / n2

        p_pool = (x1 + x2) / (n1 + n2)
        se = np.sqrt(p_pool * (1 - p_pool) * (1 / n1 + 1 / n2))
        z_stat = (p2 - p1) / se
        p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))

        return {
            "control_rate": round(p1, 4),
            "treatment_rate": round(p2, 4),
            "absolute_lift": round(p2 - p1, 4),
            "relative_lift_pct": round((p2 - p1) / p1 * 100, 2),
            "z_statistic": round(z_stat, 4),
            "p_value": round(p_value, 6),
            "significant_at_0_05": p_value < 0.05,
        }

    # ------------------------------------------------------------------
    # Continuous metric: independent t-test (with variance check)
    # ------------------------------------------------------------------
    def test_mean_difference(self, metric: str = "session_duration") -> dict:
        """Independent-samples t-test on a continuous metric between groups."""
        control, treatment = self._group("control")[metric], self._group("treatment")[metric]

        # Levene's test: are the two variances equal? (decides equal_var for the t-test)
        _, levene_p = stats.levene(control, treatment)
        equal_var = levene_p >= 0.05

        t_stat, p_value = stats.ttest_ind(treatment, control, equal_var=equal_var)

        return {
            "metric": metric,
            "control_mean": round(control.mean(), 2),
            "treatment_mean": round(treatment.mean(), 2),
            "mean_difference": round(treatment.mean() - control.mean(), 2),
            "levene_p_value": round(levene_p, 4),
            "equal_variances_assumed": equal_var,
            "t_statistic": round(t_stat, 4),
            "p_value": round(p_value, 6),
            "significant_at_0_05": p_value < 0.05,
        }

    # ------------------------------------------------------------------
    # Confidence interval
    # ------------------------------------------------------------------
    def confidence_interval(
        self, metric: str, group: str, confidence: float = 0.95
    ) -> tuple[float, float]:
        """A confidence interval for the mean of `metric` within one group."""
        data = self._group(group)[metric]
        mean = data.mean()
        sem = stats.sem(data)
        interval = stats.t.interval(confidence, df=len(data) - 1, loc=mean, scale=sem)
        return float(round(interval[0], 2)), float(round(interval[1], 2))

    # ------------------------------------------------------------------
    # Effect size
    # ------------------------------------------------------------------
    def cohens_d(self, metric: str) -> float:
        """Cohen's d effect size for `metric` between treatment and control."""
        control, treatment = self._group("control")[metric], self._group("treatment")[metric]
        n1, n2 = len(control), len(treatment)
        pooled_std = np.sqrt(
            ((n1 - 1) * control.std(ddof=1) ** 2 + (n2 - 1) * treatment.std(ddof=1) ** 2)
            / (n1 + n2 - 2)
        )
        return round((treatment.mean() - control.mean()) / pooled_std, 3)

    # ------------------------------------------------------------------
    # Console report
    # ------------------------------------------------------------------
    def print_report(self) -> None:
        print("=" * 60)
        print("A/B TEST STATISTICAL ANALYSIS")
        print("=" * 60)

        print("\nDescriptive statistics by group:")
        print(self.descriptive_stats_by_group().to_string())

        conv = self.test_conversion_rate()
        print("\nConversion rate test (two-proportion z-test):")
        for key, value in conv.items():
            print(f"  {key}: {value}")

        session_test = self.test_mean_difference("session_duration")
        print("\nSession duration test (independent t-test):")
        for key, value in session_test.items():
            print(f"  {key}: {value}")

        ci_control = self.confidence_interval("session_duration", "control")
        ci_treatment = self.confidence_interval("session_duration", "treatment")
        print(f"\n95% CI session_duration (control):   {ci_control}")
        print(f"95% CI session_duration (treatment): {ci_treatment}")

        d = self.cohens_d("session_duration")
        print(f"\nCohen's d (session_duration): {d}")

        print("\nVerdict:")
        if conv["significant_at_0_05"]:
            print(
                f"  Conversion rate lift of {conv['relative_lift_pct']}% is statistically "
                f"significant (p={conv['p_value']}). Recommend shipping the treatment."
            )
        else:
            print(
                f"  Conversion rate lift of {conv['relative_lift_pct']}% is NOT statistically "
                f"significant (p={conv['p_value']}). Recommend collecting more data."
            )
        print("=" * 60)


if __name__ == "__main__":
    analyzer = StatisticalAnalyzer()
    analyzer.print_report()
