import numpy as np
import pandas as pd
import pytest
from income_report import (
    clean_data_types,
    transform_to_long_format,
    validate_and_sanitize_raw_data,
    validate_cleaned_schema,
    validate_raw_schema,
)

@pytest.fixture
def mock_raw_df() -> pd.DataFrame:
    """Provides a minimal raw DataFrame matching the expected raw structure"""
    return pd.DataFrame(
        {
            "region": ["riket", "riket"],
            "utbildningsnivå": [" Gymnasial", "Eftergymnasial"],
            "kön": ["MÄN", "kvinnor"],
            "ålder": ["20-29 år", "30-39 år"],
            "inkomstklass": ["samtliga", "samtliga"],
            "2020": ["250,5", "300.0"],
            "2021": ["260.0", "315.2"],
        }
    )

def test_validate_raw_schema_success(mock_raw_df: pd.DataFrame):
    """Verifies that 4-digit year columns are correctly identified"""
    years = validate_raw_schema(mock_raw_df)
    assert years == ["2020", "2021"]

def test_validate_raw_schema_no_year_column(mock_raw_df: pd.DataFrame):
    """Verifies that a ValueError is raised if no 4-digit year columns exist"""
    df_no_years = mock_raw_df.drop(columns=["2020", "2021"])
    with pytest.raises(ValueError, match="lacks valid year column"):
        validate_raw_schema(df_no_years)

def test_transform_to_long_format(mock_raw_df: pd.DataFrame):
    """Verifies that wide data is melted correctly and excluded columns are dropped"""
    year_cols = ["2020", "2021"]
    df_long = transform_to_long_format(mock_raw_df, year_cols)

    assert "region" not in df_long.columns
    assert "inkomstklass" not in df_long.columns

    assert len(df_long) == 4
    assert set(df_long.columns) == {
        "utbildningsnivå",
        "kön",
        "ålder",
        "year",
        "inkomst_tkr",
    }

def test_clean_data_types_formatting_and_casting(mock_raw_df: pd.DataFrame):
    """Verifies lowercase conversion, whitespace trimming, comma replacement, and type casting"""
    df_long = transform_to_long_format(mock_raw_df, ["2020", "2021"])
    df_cleaned = clean_data_types(df_long)

    assert df_cleaned["utbildningsnivå"].iloc[0] == "gymnasial"
    assert df_cleaned["kön"].iloc[0] == "män"

    assert pd.api.types.is_integer_dtype(df_cleaned["year"])
    assert pd.api.types.is_float_dtype(df_cleaned["inkomst_tkr"])

    assert df_cleaned["inkomst_tkr"].iloc[0] == 250.5

def test_clean_data_types_drops_missing_value():
    """Verifies that rows with NaN in metadata or income are dropped properly"""
    df_with_nans = pd.DataFrame(
        {
            "utbildningsnivå": ["gymnasial", None, "eftergymnasial"],
            "kön": ["män", "kvinnor", "kvinnor"],
            "ålder": ["20-29 år", "20-29 år", "30-39 år"],
            "year": ["2020", "2020", "2020"],
            "inkomst_tkr": ["250.0", "300.0", np.nan]
        }
    )

    df_cleaned = clean_data_types(df_with_nans)

    assert len(df_cleaned) == 1
    assert df_cleaned["utbildningsnivå"].iloc[0] == "gymnasial"

def test_validate_cleaned_schema_missing_column():
    """Verifies that an error is raised if final cleaned schema is missing columns"""
    incomplete_df = pd.DataFrame(
        {"utbildningsnivå": ["gymnasial"], "kön": ["män"]}
    )
    with pytest.raises(ValueError, match="Cleaned schema mismatch"):
        validate_cleaned_schema(incomplete_df)

def test_validate_and_sanitize_raw_data_pipeline(mock_raw_df: pd.DataFrame):
    """Verifies the entire end-to-end validation pipeline"""
    result_df = validate_and_sanitize_raw_data(mock_raw_df)

    assert not result_df.empty
    assert len(result_df) == 4
    assert result_df["year"].dtype == int
    assert result_df["inkomst_tkr"].dtype == float
    assert "region" not in result_df.columns

