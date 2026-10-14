"""
Day 14 - Data Visualization
Generates a reproducible sales dataset (data/sales_performance.csv)
with enough structure (time, categories, segments, a numeric driver)
to support several different chart types meaningfully:
a trend line, a category comparison, a distribution comparison,
a scatter/correlation, and a full correlation heatmap.
"""

import numpy as np
import pandas as pd

RANDOM_SEED = 11
N_ROWS = 700

REGIONS = ["North", "South", "East", "West"]
SEGMENTS = ["Consumer", "Corporate", "Small Business"]
CATEGORIES = ["Electronics", "Office Supplies", "Furniture", "Apparel"]


def generate_dataset(n_rows: int = N_ROWS, seed: int = RANDOM_SEED) -> pd.DataFrame:
    """Build a synthetic sales-performance DataFrame for visualization."""
    rng = np.random.default_rng(seed)

    dates = pd.to_datetime("2024-01-01") + pd.to_timedelta(
        rng.integers(0, 365, size=n_rows), unit="D"
    )

    category = rng.choice(CATEGORIES, size=n_rows, p=[0.3, 0.25, 0.25, 0.2])
    segment = rng.choice(SEGMENTS, size=n_rows, p=[0.5, 0.3, 0.2])
    region = rng.choice(REGIONS, size=n_rows)

    # Sales rep experience (years), mildly correlated with revenue below
    sales_rep_experience = rng.gamma(shape=2.5, scale=1.8, size=n_rows).round(1)
    sales_rep_experience = np.clip(sales_rep_experience, 0, 15)

    category_base = {
        "Electronics": 220, "Office Supplies": 40, "Furniture": 380, "Apparel": 60,
    }
    base = np.array([category_base[c] for c in category])

    # Mild seasonal boost (higher revenue later in the year, e.g. holiday season)
    seasonal_boost = 1 + 0.3 * (dates.dayofyear / 365)

    revenue = (
        base * seasonal_boost
        + sales_rep_experience * 12
        + rng.normal(0, 40, size=n_rows)
    )
    revenue = np.clip(revenue, 10, None).round(2)

    discount = rng.choice([0.0, 0.05, 0.1, 0.15, 0.2], size=n_rows, p=[0.5, 0.2, 0.15, 0.1, 0.05])

    df = pd.DataFrame({
        "order_id": [f"ORD-{i:05d}" for i in range(1, n_rows + 1)],
        "order_date": dates,
        "region": region,
        "product_category": category,
        "customer_segment": segment,
        "sales_rep_experience": sales_rep_experience,
        "discount": discount,
        "revenue": revenue,
    })

    return df.sort_values("order_date").reset_index(drop=True)


if __name__ == "__main__":
    dataset = generate_dataset()
    dataset.to_csv("data/sales_performance.csv", index=False)
    print(f"Wrote {len(dataset)} rows to data/sales_performance.csv")
