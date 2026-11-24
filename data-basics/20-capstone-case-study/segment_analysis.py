import pandas as pd


def rfm_segments(df, customer_col, recency_col, frequency_col, monetary_col):
    segments = df.groupby(customer_col).agg(
        recency=(recency_col, "min"),
        frequency=(frequency_col, "count"),
        monetary=(monetary_col, "sum"),
    )
    segments["score"] = (
        pd.qcut(segments["recency"].rank(method="first"), 4, labels=[4, 3, 2, 1])
        .astype(int)
        + pd.qcut(segments["frequency"].rank(method="first"), 4, labels=[1, 2, 3, 4])
        .astype(int)
        + pd.qcut(segments["monetary"].rank(method="first"), 4, labels=[1, 2, 3, 4])
        .astype(int)
    )
    return segments.sort_values("score", ascending=False)
