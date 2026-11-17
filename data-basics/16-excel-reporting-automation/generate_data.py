"""
Day 16 - Excel Reporting Automation
Generates a reproducible sales dataset (data/sales_data.csv) used as
the input for an automated, formatted Excel report.
"""

import numpy as np
import pandas as pd

RANDOM_SEED = 16
N_ROWS = 400

REGIONS = ["North", "South", "East", "West"]
CATEGORIES = ["Electronics", "Office Supplies", "Furniture", "Apparel"]


def generate_dataset(n_rows: int = N_ROWS, seed: int = RANDOM_SEED) -> pd.DataFrame:
    """Build a synthetic sales DataFrame for the Excel report."""
    rng = np.random.default_rng(seed)

    dates = pd.to_datetime("2024-01-01") + pd.to_timedelta(
        rng.integers(0, 365, size=n_rows), unit="D"
    )
    category = rng.choice(CATEGORIES, size=n_rows, p=[0.3, 0.25, 0.25, 0.2])
    region = rng.choice(REGIONS, size=n_rows)

    category_base = {"Electronics": 220, "Office Supplies": 40, "Furniture": 380, "Apparel": 60}
    base = np.array([category_base[c] for c in category])
    quantity = rng.integers(1, 8, size=n_rows)
    revenue = (base * rng.uniform(0.7, 1.3, size=n_rows) * quantity / 3).round(2)

    df = pd.DataFrame({
        "order_id": [f"ORD-{i:05d}" for i in range(1, n_rows + 1)],
        "order_date": dates,
        "region": region,
        "product_category": category,
        "quantity": quantity,
        "revenue": revenue,
    })

    return df.sort_values("order_date").reset_index(drop=True)


if __name__ == "__main__":
    dataset = generate_dataset()
    dataset.to_csv("data/sales_data.csv", index=False)
    print(f"Wrote {len(dataset)} rows to data/sales_data.csv")
