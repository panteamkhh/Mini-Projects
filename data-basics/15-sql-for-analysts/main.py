"""
Day 15 - SQL for Analysts

Answers business questions directly in SQL against a normalized
SQLite database (customers, products, orders, order_items), the way
an analyst would query a real production data warehouse — joins,
aggregation, and a LEFT JOIN to catch missing relationships.

Run directly for a full console report:
    python main.py
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd


class SQLAnalyzer:
    """Runs analytical SQL queries against the sales SQLite database."""

    def __init__(self, db_path: str | Path = "data/sales.db") -> None:
        self.db_path = Path(db_path)
        if not self.db_path.exists():
            raise FileNotFoundError(
                f"Database not found at {self.db_path}. "
                "Run `python generate_data.py` first."
            )
        self.conn = sqlite3.connect(self.db_path)

    def close(self) -> None:
        self.conn.close()

    # ------------------------------------------------------------------
    # Generic escape hatch
    # ------------------------------------------------------------------
    def run_query(self, sql: str, params: tuple = ()) -> pd.DataFrame:
        """Run an arbitrary SQL query and return the result as a DataFrame."""
        return pd.read_sql_query(sql, self.conn, params=params)

    # ------------------------------------------------------------------
    # Business questions
    # ------------------------------------------------------------------
    def top_customers_by_revenue(self, n: int = 5) -> pd.DataFrame:
        """Which customers generated the most total revenue?"""
        sql = """
            SELECT
                c.customer_id,
                c.name,
                c.region,
                ROUND(SUM(oi.quantity * p.unit_price * (1 - oi.discount)), 2) AS total_revenue
            FROM customers AS c
            JOIN orders AS o ON o.customer_id = c.customer_id
            JOIN order_items AS oi ON oi.order_id = o.order_id
            JOIN products AS p ON p.product_id = oi.product_id
            GROUP BY c.customer_id, c.name, c.region
            ORDER BY total_revenue DESC
            LIMIT ?
        """
        return self.run_query(sql, params=(n,))

    def revenue_by_category(self) -> pd.DataFrame:
        """Which product category earns the most revenue?"""
        sql = """
            SELECT
                p.category,
                ROUND(SUM(oi.quantity * p.unit_price * (1 - oi.discount)), 2) AS total_revenue,
                SUM(oi.quantity) AS units_sold
            FROM order_items AS oi
            JOIN products AS p ON p.product_id = oi.product_id
            GROUP BY p.category
            ORDER BY total_revenue DESC
        """
        return self.run_query(sql)

    def monthly_revenue_trend(self) -> pd.DataFrame:
        """Total revenue per calendar month, across all orders."""
        sql = """
            SELECT
                strftime('%Y-%m', o.order_date) AS month,
                ROUND(SUM(oi.quantity * p.unit_price * (1 - oi.discount)), 2) AS total_revenue
            FROM orders AS o
            JOIN order_items AS oi ON oi.order_id = o.order_id
            JOIN products AS p ON p.product_id = oi.product_id
            GROUP BY month
            ORDER BY month
        """
        return self.run_query(sql)

    def customers_without_orders(self) -> pd.DataFrame:
        """Customers who have never placed an order (a LEFT JOIN / anti-join)."""
        sql = """
            SELECT c.customer_id, c.name, c.region, c.segment
            FROM customers AS c
            LEFT JOIN orders AS o ON o.customer_id = c.customer_id
            WHERE o.order_id IS NULL
        """
        return self.run_query(sql)

    def average_order_value_by_region(self) -> pd.DataFrame:
        """Average order value (per order, not per line item) by region."""
        sql = """
            SELECT region, ROUND(AVG(order_total), 2) AS avg_order_value
            FROM (
                SELECT
                    o.order_id,
                    c.region,
                    SUM(oi.quantity * p.unit_price * (1 - oi.discount)) AS order_total
                FROM orders AS o
                JOIN customers AS c ON c.customer_id = o.customer_id
                JOIN order_items AS oi ON oi.order_id = o.order_id
                JOIN products AS p ON p.product_id = oi.product_id
                GROUP BY o.order_id, c.region
            )
            GROUP BY region
            ORDER BY avg_order_value DESC
        """
        return self.run_query(sql)

    # ------------------------------------------------------------------
    # Console report
    # ------------------------------------------------------------------
    def print_report(self) -> None:
        print("=" * 60)
        print("SQL ANALYSIS REPORT")
        print("=" * 60)

        print("\nTop 5 customers by revenue:")
        print(self.top_customers_by_revenue(5).to_string(index=False))

        print("\nRevenue by product category:")
        print(self.revenue_by_category().to_string(index=False))

        print("\nMonthly revenue trend:")
        print(self.monthly_revenue_trend().to_string(index=False))

        print("\nCustomers without any orders:")
        without_orders = self.customers_without_orders()
        print(without_orders.to_string(index=False) if len(without_orders) else "  (none)")

        print("\nAverage order value by region:")
        print(self.average_order_value_by_region().to_string(index=False))
        print("=" * 60)


if __name__ == "__main__":
    analyzer = SQLAnalyzer()
    try:
        analyzer.print_report()
    finally:
        analyzer.close()
