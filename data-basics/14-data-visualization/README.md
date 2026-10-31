# Day 14 — Data Visualization

A `SalesVisualizer` class that turns a sales dataset into five
presentation-ready charts with `matplotlib` + `seaborn` — each one
built to answer a specific business question, not just "plot the
column."

---

## Charts and the question each one answers

| Chart | Question |
|---|---|
| `revenue_trend.png` | Is revenue growing month over month? |
| `revenue_by_category.png` | Which product category drives the most revenue? |
| `order_value_distribution.png` | How does order value vary across customer segments? |
| `experience_vs_revenue.png` | Does sales-rep experience relate to order value? |
| `correlation_heatmap.png` | How do all the numeric variables relate to each other? |

Every chart method returns a `matplotlib.figure.Figure`, so charts
can be reviewed, tested, or embedded elsewhere before being saved —
`save_all()` is just a convenience wrapper that saves every chart as
a PNG.

---

## Key concepts used

- Line charts for time trends (`resample("ME")` + `ax.plot`)
- Horizontal bar charts for category comparison
- Box plots for distribution comparison across groups (`seaborn.boxplot`)
- Regression scatter plots for relationships (`seaborn.regplot`)
- Correlation heatmaps (`seaborn.heatmap`)
- Headless-safe plotting (`matplotlib.use("Agg")`) so charts generate
  reliably in scripts/CI, not just notebooks
- Class-based design where each chart is one testable method, plus a
  `save_all()` that batches and saves everything to `charts/`

---

## Dataset

`data/sales_performance.csv` (700 orders) is generated with genuine
(if mild) relationships built in — e.g. more experienced sales reps
tend toward higher-value orders — so the charts show real signal.

```bash
python generate_data.py
```

## How to run

```bash
python main.py
```

This saves all five charts into `charts/`.

## How to test

```bash
pip install -r ../../requirements.txt
pytest test_main.py
```
