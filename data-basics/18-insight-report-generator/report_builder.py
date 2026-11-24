import pandas as pd


def build_report(df, metric, dimension):
    grouped = df.groupby(dimension)[metric].agg(["sum", "mean", "count"])
    grouped = grouped.sort_values("sum", ascending=False)
    return grouped.reset_index()


def to_markdown(df, title="Report"):
    header = "| " + " | ".join(df.columns) + " |"
    divider = "| " + " | ".join(["---"] * len(df.columns)) + " |"
    rows = [
        "| " + " | ".join(str(value) for value in row) + " |"
        for row in df.itertuples(index=False)
    ]
    return "\n".join([f"# {title}", "", header, divider, *rows])
