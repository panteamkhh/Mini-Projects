import numpy as np
import pandas as pd


def summarize(series):
    data = pd.Series(series).dropna()
    return {
        "count": int(data.count()),
        "mean": float(data.mean()),
        "median": float(data.median()),
        "std": float(data.std()),
        "min": float(data.min()),
        "max": float(data.max()),
        "q1": float(data.quantile(0.25)),
        "q3": float(data.quantile(0.75)),
    }


def describe_frame(df):
    return df.describe().T


if __name__ == "__main__":
    sample = np.random.normal(loc=50, scale=10, size=200)
    for key, value in summarize(sample).items():
        print(f"{key}: {value:.2f}")
