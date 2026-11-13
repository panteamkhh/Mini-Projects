"""
Day 16 - Excel Reporting Automation

Turns a raw sales CSV into a polished, multi-sheet Excel workbook —
the kind of deliverable a stakeholder can open directly, with no
extra formatting work: a KPI summary, a filterable raw-data table,
and a category breakdown with a native embedded chart.

Run directly to build the report:
    python main.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.worksheet import Worksheet

HEADER_FILL = PatternFill(start_color="2E5EAA", end_color="2E5EAA", fill_type="solid")
HEADER_FONT = Font(color="FFFFFF", bold=True)
KPI_LABEL_FONT = Font(bold=True, size=12)
KPI_VALUE_FONT = Font(size=16, bold=True, color="2E5EAA")


class ExcelReportBuilder:
    """Builds a formatted, multi-sheet Excel sales report from a CSV."""

    def __init__(self, csv_path: str | Path = "data/sales_data.csv") -> None:
        self.csv_path = Path(csv_path)
        self.df: pd.DataFrame = self._load()
        self.workbook: Workbook | None = None

    # ------------------------------------------------------------------
    # Loading
    # ------------------------------------------------------------------
    def _load(self) -> pd.DataFrame:
        if not self.csv_path.exists():
            raise FileNotFoundError(
                f"Dataset not found at {self.csv_path}. "
                "Run `python generate_data.py` first."
            )
        return pd.read_csv(self.csv_path, parse_dates=["order_date"])

    # ------------------------------------------------------------------
    # Shared styling helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _style_header_row(ws: Worksheet, row: int, n_cols: int) -> None:
        for col in range(1, n_cols + 1):
            cell = ws.cell(row=row, column=col)
            cell.fill = HEADER_FILL
            cell.font = HEADER_FONT
            cell.alignment = Alignment(horizontal="center")

    @staticmethod
    def _autosize_columns(ws: Worksheet, df: pd.DataFrame, start_col: int = 1) -> None:
        for i, column in enumerate(df.columns, start=start_col):
            max_len = max(len(str(column)), df[column].astype(str).map(len).max())
            ws.column_dimensions[get_column_letter(i)].width = min(max_len + 4, 30)

    # ------------------------------------------------------------------
    # Sheets
    # ------------------------------------------------------------------
    def build_summary_sheet(self, wb: Workbook) -> None:
        """A KPI dashboard sheet: total revenue, orders, AOV, top region."""
        ws = wb.active
        ws.title = "Summary"

        total_revenue = self.df["revenue"].sum()
        total_orders = len(self.df)
        avg_order_value = self.df["revenue"].mean()
        top_region = self.df.groupby("region")["revenue"].sum().idxmax()

        ws["B2"] = "Sales Report Summary"
        ws["B2"].font = Font(bold=True, size=16)

        kpis = [
            ("Total Revenue", f"${total_revenue:,.2f}"),
            ("Total Orders", f"{total_orders:,}"),
            ("Average Order Value", f"${avg_order_value:,.2f}"),
            ("Top Region", top_region),
        ]
        for i, (label, value) in enumerate(kpis):
            row = 4 + i
            ws.cell(row=row, column=2, value=label).font = KPI_LABEL_FONT
            ws.cell(row=row, column=3, value=value).font = KPI_VALUE_FONT

        ws.column_dimensions["B"].width = 22
        ws.column_dimensions["C"].width = 20

    def build_data_sheet(self, wb: Workbook) -> None:
        """A filterable raw-data sheet with a styled, frozen header row."""
        ws = wb.create_sheet("Raw Data")

        display_df = self.df.copy()
        display_df["order_date"] = display_df["order_date"].dt.strftime("%Y-%m-%d")

        ws.append(list(display_df.columns))
        for row in display_df.itertuples(index=False):
            ws.append(list(row))

        self._style_header_row(ws, row=1, n_cols=display_df.shape[1])
        self._autosize_columns(ws, display_df)

        ws.freeze_panes = "A2"
        ws.auto_filter.ref = ws.dimensions

    def build_category_sheet(self, wb: Workbook) -> None:
        """A category revenue summary with a native embedded bar chart."""
        ws = wb.create_sheet("By Category")

        summary = (
            self.df.groupby("product_category")["revenue"]
            .sum()
            .sort_values(ascending=False)
            .round(2)
            .reset_index()
        )

        ws.append(["Product Category", "Total Revenue"])
        for row in summary.itertuples(index=False):
            ws.append(list(row))

        self._style_header_row(ws, row=1, n_cols=2)
        self._autosize_columns(ws, summary)

        chart = BarChart()
        chart.title = "Revenue by Product Category"
        chart.y_axis.title = "Total Revenue ($)"
        chart.x_axis.title = "Product Category"

        data_ref = Reference(ws, min_col=2, min_row=1, max_row=len(summary) + 1)
        categories_ref = Reference(ws, min_col=1, min_row=2, max_row=len(summary) + 1)
        chart.add_data(data_ref, titles_from_data=True)
        chart.set_categories(categories_ref)

        ws.add_chart(chart, "D2")

    # ------------------------------------------------------------------
    # Orchestration
    # ------------------------------------------------------------------
    def build(self, output_path: str | Path = "output/sales_report.xlsx") -> Path:
        """Build all sheets and save the workbook. Returns the saved path."""
        wb = Workbook()
        self.build_summary_sheet(wb)
        self.build_data_sheet(wb)
        self.build_category_sheet(wb)

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        wb.save(output_path)

        self.workbook = wb
        return output_path


if __name__ == "__main__":
    builder = ExcelReportBuilder()
    saved_path = builder.build()
    print(f"Saved Excel report to {saved_path}")
