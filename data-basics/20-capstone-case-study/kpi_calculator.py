import pandas as pd


def revenue_per_customer(revenue, customers):
    return revenue / customers if customers else 0.0


def margin_pct(revenue, cost):
    return (revenue - cost) / revenue if revenue else 0.0


def kpi_table(df, revenue_col="revenue", cost_col="cost", customer_col="customers"):
    summary = df[[revenue_col, cost_col, customer_col]].sum()
    return pd.DataFrame(
        {
            "kpi": ["revenue", "cost", "customers", "revenue_per_customer", "margin_pct"],
            "value": [
                summary[revenue_col],
                summary[cost_col],
                summary[customer_col],
                revenue_per_customer(summary[revenue_col], summary[customer_col]),
                margin_pct(summary[revenue_col], summary[cost_col]),
            ],
        }
    )
