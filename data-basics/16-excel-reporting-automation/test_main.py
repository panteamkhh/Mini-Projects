"""Unit tests for ExcelReportBuilder (Day 16 - Excel Reporting Automation)."""

import pytest
from openpyxl import Workbook, load_workbook

from generate_data import generate_dataset
from main import ExcelReportBuilder


@pytest.fixture
def builder(tmp_path) -> ExcelReportBuilder:
    csv_path = tmp_path / "sales_data.csv"
    generate_dataset(n_rows=50, seed=2).to_csv(csv_path, index=False)
    return ExcelReportBuilder(csv_path=csv_path)


def test_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        ExcelReportBuilder(csv_path=tmp_path / "nope.csv")


def test_build_creates_file(builder, tmp_path):
    output_path = tmp_path / "report.xlsx"
    saved_path = builder.build(output_path=output_path)

    assert saved_path == output_path
    assert output_path.exists()


def test_build_creates_output_dir_if_missing(builder, tmp_path):
    output_path = tmp_path / "nested" / "report.xlsx"
    assert not output_path.parent.exists()

    builder.build(output_path=output_path)
    assert output_path.exists()


def test_workbook_has_three_sheets(builder, tmp_path):
    output_path = tmp_path / "report.xlsx"
    builder.build(output_path=output_path)

    wb = load_workbook(output_path)
    assert wb.sheetnames == ["Summary", "Raw Data", "By Category"]


def test_summary_sheet_kpi_values(builder, tmp_path):
    output_path = tmp_path / "report.xlsx"
    builder.build(output_path=output_path)

    wb = load_workbook(output_path)
    ws = wb["Summary"]

    labels = [ws.cell(row=r, column=2).value for r in range(4, 8)]
    assert labels == ["Total Revenue", "Total Orders", "Average Order Value", "Top Region"]

    total_orders_value = ws.cell(row=5, column=3).value
    assert total_orders_value == "50"


def test_raw_data_sheet_row_count_matches_dataframe(builder, tmp_path):
    output_path = tmp_path / "report.xlsx"
    builder.build(output_path=output_path)

    wb = load_workbook(output_path)
    ws = wb["Raw Data"]
    # +1 for header row
    assert ws.max_row == len(builder.df) + 1
    assert ws.max_column == len(builder.df.columns)


def test_raw_data_sheet_has_freeze_panes_and_autofilter(builder, tmp_path):
    output_path = tmp_path / "report.xlsx"
    builder.build(output_path=output_path)

    wb = load_workbook(output_path)
    ws = wb["Raw Data"]
    assert ws.freeze_panes == "A2"
    assert ws.auto_filter.ref is not None


def test_category_sheet_has_embedded_chart(builder, tmp_path):
    output_path = tmp_path / "report.xlsx"
    builder.build(output_path=output_path)

    wb = load_workbook(output_path)
    ws = wb["By Category"]
    assert len(ws._charts) == 1


def test_category_sheet_row_count_matches_categories(builder, tmp_path):
    output_path = tmp_path / "report.xlsx"
    builder.build(output_path=output_path)

    wb = load_workbook(output_path)
    ws = wb["By Category"]
    n_categories = builder.df["product_category"].nunique()
    assert ws.max_row == n_categories + 1  # + header
