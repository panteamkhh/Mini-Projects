"""
Day 12 - Data Cleaning Pipeline
Generates a deliberately messy customer-orders dataset
(data/raw_customer_orders.csv) so main.py has real problems to fix:

- Missing values (empty cells) scattered across several columns
- Exact duplicate rows
- Dates in three different formats
- Currency amounts written inconsistently ("$120.50", "120.5", "1,200")
- Inconsistent text casing/whitespace in region and customer_name
- Invalid quantities (negative numbers, zero, non-numeric junk)

The messiness is injected deterministically (fixed seed) so the
"before" dataset is reproducible and the cleaning pipeline in
main.py can be tested against known issues.
"""

import numpy as np
import pandas as pd

RANDOM_SEED = 7
N_ROWS = 500

REGIONS = ["North", "South", "East", "West"]
REGION_VARIANTS = {
    "North": ["North", "north", "NORTH", " North", "North "],
    "South": ["South", "south", "SOUTH ", " south"],
    "East": ["East", "east", " EAST"],
    "West": ["West", "west", "WEST", "West  "],
}

FIRST_NAMES = ["Ali", "Sara", "Reza", "Mina", "Amir", "Nazanin", "Kian", "Leila"]
LAST_NAMES = ["Ahmadi", "Karimi", "Hosseini", "Moradi", "Rostami", "Jafari"]


def _messy_date(date: pd.Timestamp, style: int) -> str:
    """Render one date in one of three inconsistent formats."""
    if style == 0:
        return date.strftime("%Y-%m-%d")
    if style == 1:
        return date.strftime("%m/%d/%Y")
    return date.strftime("%-d-%b-%Y") if hasattr(date, "strftime") else str(date)


def _messy_amount(amount: float, style: int) -> str:
    """Render one amount in one of several inconsistent string formats."""
    if style == 0:
        return f"${amount:,.2f}"
    if style == 1:
        return f"{amount:.2f}"
    if style == 2:
        return f"{amount:,.0f}"
    return f" {amount:.2f} "


def generate_dataset(n_rows: int = N_ROWS, seed: int = RANDOM_SEED) -> pd.DataFrame:
    """Build a deliberately messy customer-orders DataFrame."""
    rng = np.random.default_rng(seed)

    order_ids = [f"ORD-{i:05d}" for i in range(1, n_rows + 1)]
    first = rng.choice(FIRST_NAMES, size=n_rows)
    last = rng.choice(LAST_NAMES, size=n_rows)
    customer_names = [f"{f} {l}" for f, l in zip(first, last)]

    regions_clean = rng.choice(REGIONS, size=n_rows)
    regions_messy = [rng.choice(REGION_VARIANTS[r]) for r in regions_clean]

    base_dates = pd.to_datetime("2024-01-01") + pd.to_timedelta(
        rng.integers(0, 300, size=n_rows), unit="D"
    )
    date_styles = rng.integers(0, 3, size=n_rows)
    dates_messy = [_messy_date(d, s) for d, s in zip(base_dates, date_styles)]

    amounts_clean = rng.uniform(15, 900, size=n_rows).round(2)
    amount_styles = rng.integers(0, 4, size=n_rows)
    amounts_messy = [_messy_amount(a, s) for a, s in zip(amounts_clean, amount_styles)]

    quantities = rng.integers(1, 12, size=n_rows).astype(object)
    # Inject invalid quantities: negatives, zero, and junk strings
    bad_qty_idx = rng.choice(n_rows, size=int(n_rows * 0.06), replace=False)
    for i, idx in enumerate(bad_qty_idx):
        quantities[idx] = [-3, 0, "N/A", "unknown"][i % 4]

    df = pd.DataFrame({
        "order_id": order_ids,
        "customer_name": customer_names,
        "region": regions_messy,
        "order_date": dates_messy,
        "amount": amounts_messy,
        "quantity": quantities,
    })

    # Missing values scattered in customer_name, region, amount
    for col, frac in [("customer_name", 0.03), ("region", 0.04), ("amount", 0.02)]:
        idx = rng.choice(n_rows, size=int(n_rows * frac), replace=False)
        df.loc[idx, col] = np.nan

    # Exact duplicate rows (append copies of random existing rows)
    n_dupes = int(n_rows * 0.05)
    dupe_rows = df.sample(n=n_dupes, random_state=seed)
    df = pd.concat([df, dupe_rows], ignore_index=True)

    # Shuffle so duplicates aren't conveniently adjacent
    df = df.sample(frac=1, random_state=seed).reset_index(drop=True)

    return df


if __name__ == "__main__":
    dataset = generate_dataset()
    dataset.to_csv("data/raw_customer_orders.csv", index=False)
    print(f"Wrote {len(dataset)} rows to data/raw_customer_orders.csv")
