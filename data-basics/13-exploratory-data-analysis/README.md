# Day 13 — Exploratory Data Analysis

An `EDAExplorer` class that runs a structured exploratory analysis
over an employee-performance dataset: not just `.describe()`, but a
full path from raw numbers to plain-English insights an employer
would actually act on.

---

## What it answers

- What does the data look like (shape, dtypes, missingness)?
- What are the summary statistics for every numeric column?
- Which variables are correlated with `performance_rating`, and how
  strongly?
- How does average performance differ across departments?
- Are there statistical outliers in `monthly_sales` worth a closer look?
- Does remote work correlate with satisfaction?

Every one of these is backed by a real, reusable method — not just a
one-off script — so the same `EDAExplorer` class could be pointed at
a different dataset with the same shape and still work.

---

## Key concepts used

- Dataset structure inspection (`.shape`, `.dtypes`, `.isna().sum()`)
- Descriptive statistics (`.describe()`)
- Correlation analysis (`.corr()`, ranking by absolute strength)
- Group-by comparisons across categorical variables (`.groupby().mean()`)
- Outlier detection with the 1.5 × IQR rule
- Turning statistical output into short, decision-relevant insights
  (`key_insights()`) instead of stopping at raw numbers

---

## Dataset

`data/employee_performance.csv` (300 employees) is synthetic but
built with **intentional relationships** between columns — e.g.
`training_hours` genuinely drives `performance_rating` — so the
correlation and group-comparison analysis finds real signal instead
of noise.

```bash
python generate_data.py
```

## How to run

```bash
python main.py
```

## How to test

```bash
pip install -r ../../requirements.txt
pytest test_main.py
```
