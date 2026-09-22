import numpy as np
import pandas as pd
from pathlib import Path
import pytest
from income_report import (
    get_age_income_profile,
    get_education_income_over_time,
    get_gender_income_over_time,
    get_yearly_extreme_groups,
    save_processed_data
)

@pytest.fixture
def mock_cleaned_df() -> pd.DataFrame:
    """Provides a cleaned long-format DataFrame for analysis testning"""
    return pd.DataFrame(
        {
            "utbildningsnivå": ["förgymnasial", "eftergymnasial", "förgymnasial", "eftergymnasial"],
            "kön": ["män", "kvinnor", "män", "kvinnor"],
            "ålder": ["20-29 år", "30-39 år", "20-29 år", "30-39 år"],
            "year": [2020, 2020, 2021, 2021],
            "inkomst_tkr": [100.0, 300.0, 120.0, 350.0]
        }
    )

def test_get_yearly_extreme_groups(mock_cleaned_df: pd.DataFrame):
    """Verifies that max and min income groups are correctly identified per year"""
    extremes = get_yearly_extreme_groups(mock_cleaned_df)

    assert len(extremes) == 4
    assert set(extremes["typ"].unique()) == {"högst", "lägst"}

    row_2020_high = extremes[(extremes["year"] == 2020) & (extremes["typ"] == "högst")].iloc[0]
    assert row_2020_high["inkomst_tkr"] == 300.0
    assert row_2020_high["kön"] == "kvinnor"

def test_get_gender_income_over_time(mock_cleaned_df: pd.DataFrame):
    """Verifies average income aggregation per year and gender"""
    gender_df = get_gender_income_over_time(mock_cleaned_df)

    assert "year" in gender_df.columns
    assert "kön" in gender_df.columns
    assert "inkomst_tkr" in gender_df.columns
    assert len(gender_df) == 4

def test_get_age_income_profile(mock_cleaned_df: pd.DataFrame):
    """Verifies average income aggregation across age groups"""
    age_df = get_age_income_profile(mock_cleaned_df)

    assert "ålder" in age_df.columns
    assert "inkomst_tkr" in age_df.columns
    assert len(age_df) == 2

def test_get_education_income_over_time(mock_cleaned_df: pd.DataFrame):
    """Verifies average income aggregation per year and education level"""
    edu_df = get_education_income_over_time(mock_cleaned_df)

    assert edu_df is not None
    assert "utbildningsnivå" in edu_df.columns
    assert len(edu_df) == 4

def test_save_processed_data(tmp_path: Path, monkeypatch, mock_cleaned_df: pd.DataFrame):
    """Verifies that files are correctly saved to disk"""
    fake_path = tmp_path / "scb_income_cleaned.csv"
    monkeypatch.setattr("income_report.processing.PROCESSED_DATA_PATH", fake_path)

    results = {
        "cleaned_data": mock_cleaned_df,
        "yearly_extremes": get_yearly_extreme_groups(mock_cleaned_df)
    }

    save_processed_data(results)

    assert fake_path.exists()
    assert (tmp_path / "yearly_income_extremes.csv").exists()