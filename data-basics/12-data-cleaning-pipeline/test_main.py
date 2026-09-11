"""Unit tests for DataCleaner (Day 12 - Data Cleaning Pipeline)."""

import pandas as pd
import pytest

from main import DataCleaner


@pytest.fixture
def raw_csv(tmp_path):
    """A small, hand-crafted messy CSV covering every issue type."""
    content = (
        "order_id,customer_name,region,order_date,amount,quantity\n"
        "ORD-1,Ali Ahmadi, north ,2024-01-05,$120.50,3\n"
        "ORD-1,Ali Ahmadi, north ,2024-01-05,$120.50,3\n"        # exact duplicate
        "ORD-2,Sara Karimi,SOUTH,01/15/2024,250.00,5\n"
        "ORD-3,Reza Moradi,East,5-Feb-2024,1,000.00,2\n"          # comma-formatted amount (mis-split by csv is avoided below)
        "ORD-4,Mina Hosseini,west,2024-03-01, 99.99 ,-2\n"        # invalid negative quantity
        "ORD-5,,North,2024-03-10,150.00,4\n"                      # missing customer_name
        "ORD-6,Kian Jafari,South,2024-03-12,,6\n"                 # missing amount
        "ORD-7,Nazanin Rostami,West,2024-03-15,300.00,N/A\n"      # junk quantity
    )
    # Fix the comma-in-amount row so the CSV itself stays well-formed
    content = content.replace("Reza Moradi,East,5-Feb-2024,1,000.00,2",
                               'Reza Moradi,East,5-Feb-2024,"1,000.00",2')
    path = tmp_path / "raw_customer_orders.csv"
    path.write_text(content)
    return path


@pytest.fixture
def cleaner(raw_csv) -> DataCleaner:
    return DataCleaner(csv_path=raw_csv)


def test_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        DataCleaner(csv_path=tmp_path / "nope.csv")


def test_standardize_text_strips_and_title_cases():
    series = pd.Series([" north ", "SOUTH", "east", None])
    result = DataCleaner.standardize_text(series)
    assert result.iloc[0] == "North"
    assert result.iloc[1] == "South"
    assert result.iloc[2] == "East"
    assert pd.isna(result.iloc[3])


def test_parse_messy_dates_handles_multiple_formats():
    series = pd.Series(["2024-01-05", "01/15/2024", "5-Feb-2024"])
    result = DataCleaner.parse_messy_dates(series)
    assert result.iloc[0] == pd.Timestamp("2024-01-05")
    assert result.iloc[1] == pd.Timestamp("2024-01-15")
    assert result.iloc[2] == pd.Timestamp("2024-02-05")


def test_parse_messy_amount_strips_currency_and_commas():
    series = pd.Series(["$120.50", "1,000.00", " 99.99 ", "250.00"])
    result = DataCleaner.parse_messy_amount(series)
    assert list(result) == [120.50, 1000.00, 99.99, 250.00]


def test_parse_quantity_turns_junk_into_nan():
    series = pd.Series(["3", "-2", "N/A", "6"])
    result = DataCleaner.parse_quantity(series)
    assert result.iloc[0] == 3
    assert result.iloc[1] == -2  # sign preserved here; filtering happens in clean()
    assert pd.isna(result.iloc[2])
    assert result.iloc[3] == 6


def test_clean_removes_duplicates(cleaner):
    cleaner.clean()
    assert cleaner.report["duplicates_removed"] == 1


def test_clean_removes_invalid_quantities(cleaner):
    cleaner.clean()
    # ORD-4 (-2) and ORD-7 (N/A) should both be gone
    assert "ORD-4" not in set(cleaner.clean_df["order_id"])
    assert "ORD-7" not in set(cleaner.clean_df["order_id"])


def test_clean_removes_missing_value_rows(cleaner):
    cleaner.clean()
    # ORD-5 (missing name) and ORD-6 (missing amount) should both be gone
    assert "ORD-5" not in set(cleaner.clean_df["order_id"])
    assert "ORD-6" not in set(cleaner.clean_df["order_id"])


def test_clean_dataframe_has_no_missing_values(cleaner):
    cleaned = cleaner.clean()
    assert cleaned.isna().sum().sum() == 0


def test_clean_dataframe_dtypes(cleaner):
    cleaned = cleaner.clean()
    assert pd.api.types.is_datetime64_any_dtype(cleaned["order_date"])
    assert pd.api.types.is_float_dtype(cleaned["amount"])
    assert pd.api.types.is_integer_dtype(cleaned["quantity"])


def test_region_values_are_normalized(cleaner):
    cleaned = cleaner.clean()
    assert set(cleaned["region"]).issubset({"North", "South", "East", "West"})


def test_report_totals_are_consistent(cleaner):
    cleaner.clean()
    r = cleaner.report
    dropped = (
        r["duplicates_removed"]
        + r["invalid_quantity_rows_removed"]
        + r["missing_value_rows_removed"]
    )
    assert r["initial_rows"] - dropped == r["final_rows"]


def test_save_clean_writes_file(cleaner, tmp_path):
    cleaner.clean()
    out_path = tmp_path / "clean.csv"
    cleaner.save_clean(out_path)
    assert out_path.exists()
    reloaded = pd.read_csv(out_path)
    assert len(reloaded) == len(cleaner.clean_df)


def test_save_clean_before_clean_raises(raw_csv):
    fresh = DataCleaner(csv_path=raw_csv)
    with pytest.raises(RuntimeError):
        fresh.save_clean()
