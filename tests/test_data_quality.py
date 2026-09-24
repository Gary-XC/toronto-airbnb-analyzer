import pandas as pd
import pytest
from pathlib import Path

# Path to the processed data
BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_FILE = BASE_DIR / "data" / "processed" / "listings_clean.csv"


@pytest.fixture
def df():
    """Load the cleaned dataset for testing."""
    return pd.read_csv(PROCESSED_FILE)


def test_no_duplicate_ids(df):
    """Ensure each listing is unique. Duplicates would artificially inflate neighborhood metrics."""
    assert df["id"].is_unique, "Duplicate listing IDs found in processed data."


def test_no_nulls_in_critical_columns(df):
    """Ensure core analytical dimensions have no missing values."""
    critical_cols = [
        "id",
        "neighbourhood",
        "room_type",
        "price",
        "estimated_annual_revenue",
    ]
    null_counts = df[critical_cols].isnull().sum()
    assert (
        null_counts.sum() == 0
    ), f"Null values found in critical columns: {null_counts[null_counts > 0]}"


def test_price_is_positive(df):
    """Business rule: Price cannot be negative or zero."""
    assert (df["price"] > 0).all(), "Found listings with price <= 0."


def test_minimum_nights_logical(df):
    """Business rule: Minimum nights must be between 1 and 365."""
    assert (df["minimum_nights"] >= 1).all() and (
        df["minimum_nights"] <= 365
    ).all(), "Found illogical minimum_nights values."
