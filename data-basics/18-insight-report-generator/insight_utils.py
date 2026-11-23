import pandas as pd


def top_movers(df, value_col, label_col, n=5):
    ranked = df.groupby(label_col)[value_col].sum().sort_values(ascending=False)
    return {
        "top": ranked.head(n).to_dict(),
        "bottom": ranked.tail(n).to_dict(),
    }


def growth_rate(series):
    return series.pct_change().round(4).fillna(0)


def format_insight(title, values):
    lines = [f"## {title}"]
    for key, value in values.items():
        lines.append(f"- {key}: {value:,.2f}")
    return "\n".join(lines)
