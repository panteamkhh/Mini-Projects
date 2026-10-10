"""
Day 13 - Exploratory Data Analysis
Generates a reproducible employee-performance dataset
(data/employee_performance.csv) with enough numeric and categorical
columns to make correlation, distribution, and group-comparison
analysis meaningful (rather than trivial).
"""

import numpy as np
import pandas as pd

RANDOM_SEED = 21
N_ROWS = 300

DEPARTMENTS = ["Sales", "Engineering", "Support", "Marketing", "HR"]
REGIONS = ["North", "South", "East", "West"]


def generate_dataset(n_rows: int = N_ROWS, seed: int = RANDOM_SEED) -> pd.DataFrame:
    """Build a synthetic employee-performance DataFrame with realistic
    (correlated, not purely random) relationships between columns."""
    rng = np.random.default_rng(seed)

    department = rng.choice(DEPARTMENTS, size=n_rows)
    region = rng.choice(REGIONS, size=n_rows)
    remote_worker = rng.choice([True, False], size=n_rows, p=[0.35, 0.65])

    years_experience = rng.gamma(shape=3.0, scale=2.0, size=n_rows).round(1)
    years_experience = np.clip(years_experience, 0, 25)

    age = (24 + years_experience + rng.normal(0, 4, size=n_rows)).round().astype(int)
    age = np.clip(age, 21, 65)

    training_hours = rng.integers(0, 60, size=n_rows)

    # Monthly sales: correlated with years_experience and training_hours,
    # but only meaningful for Sales/Marketing; other depts get lower base.
    dept_multiplier = np.where(np.isin(department, ["Sales", "Marketing"]), 1.0, 0.3)
    monthly_sales = (
        2000
        + years_experience * 350
        + training_hours * 25
        + rng.normal(0, 800, size=n_rows)
    ) * dept_multiplier
    monthly_sales = np.clip(monthly_sales, 0, None).round(2)

    # Satisfaction score (1-10): higher with more training, lower with more age
    satisfaction_score = (
        6.5 + training_hours * 0.03 - (age - 30) * 0.02 + rng.normal(0, 1.0, size=n_rows)
    )
    satisfaction_score = np.clip(satisfaction_score, 1, 10).round(1)

    # Performance rating (1-5): correlated with training_hours and satisfaction
    performance_rating = (
        2.5 + training_hours * 0.03 + satisfaction_score * 0.15 + rng.normal(0, 0.5, size=n_rows)
    )
    performance_rating = np.clip(performance_rating, 1, 5).round(1)

    df = pd.DataFrame({
        "employee_id": [f"EMP-{i:04d}" for i in range(1, n_rows + 1)],
        "department": department,
        "region": region,
        "remote_worker": remote_worker,
        "age": age,
        "years_experience": years_experience,
        "training_hours": training_hours,
        "monthly_sales": monthly_sales,
        "satisfaction_score": satisfaction_score,
        "performance_rating": performance_rating,
    })

    return df


if __name__ == "__main__":
    dataset = generate_dataset()
    dataset.to_csv("data/employee_performance.csv", index=False)
    print(f"Wrote {len(dataset)} rows to data/employee_performance.csv")
