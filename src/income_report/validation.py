import pandas as pd
from income_report.config import (
    REQUIRED_RAW_METADATA_COLUMNS,
    REQUIRED_CLEANED_COLUMNS,
    logger,
)

def validate_raw_schema(df: pd.DataFrame) -> list[str]:
    """Validates metadata columns and identifies dynamic 4-digit year columns"""
    missing_cols = [col for col in REQUIRED_RAW_METADATA_COLUMNS if col not in df.columns]
    if missing_cols:
        logger.error(f"Missing required metadata columns: {missing_cols}")
        raise ValueError(f"Missing metadata columns: {missing_cols}")

    year_cols = [col for col in df.columns if col.isdigit() and len(col) == 4]
    if not year_cols:
        logger.error("No valid 4-digit year columns found in raw data")
        raise ValueError("Raw data lacks valid year columns")

    return year_cols

def transform_to_long_format(df: pd.DataFrame, year_cols: list[str]) -> pd.DataFrame:
    """Drops unnecessary columns and melts wide dataset to long format"""
    cols_to_exclude = ["inkomstklass", "region"]
    id_vars = [col for col in REQUIRED_RAW_METADATA_COLUMNS if col not in cols_to_exclude]

    df_melted = pd.melt(
        df,
        id_vars=id_vars,
        value_vars=year_cols,
        var_name="year",
        value_name="inkomst_tkr",
    )

    return df_melted

def clean_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """Cleans and standardizes data types in the DataFrame"""
    df_sanitized = df.copy()

    string_cols = ["utbildningsnivå", "kön", "ålder"]
    for col in string_cols:
        if col in df_sanitized.columns:
            df_sanitized[col] = (
                df_sanitized[col]
                .astype(str)
                .str.strip()
                .str.lower()
            )

    metadata_cols = [col for col in string_cols if col in df_sanitized.columns]
    inital_rows = len(df_sanitized)

    df_sanitized = df_sanitized.dropna(subset=metadata_cols)

    dropped_rows = inital_rows - len(df_sanitized)
    if dropped_rows > 0:
        logger.warning(f"Dropped {dropped_rows} rows due to missing metadata values")

    try:
        df_sanitized["year"] = df_sanitized["year"].astype(int)

        df_sanitized["inkomst_tkr"] = (
            df_sanitized["inkomst_tkr"]
            .astype(str)
            .str.replace(",", ".", regex=False)
        )

        df_sanitized["inkomst_tkr"] = df_sanitized["inkomst_tkr"].astype(float)

        income_nulls = df_sanitized["inkomst_tkr"].isnull().sum()
        if income_nulls > 0:
            logger.warning(f"Dropped {income_nulls} rows due to missing income data")
            df_sanitized = df_sanitized.dropna(subset=["inkomst_tkr"])

    except Exception as e:
        logger.error(f"Failed to cast data types: {e}")
        raise ValueError(f"Datatype conversion error: {e}") from e

    return df_sanitized  

def validate_cleaned_schema(df: pd.DataFrame) -> None:
    """Validates the output DataFrame against the final cleaned schema"""
    missing_cols = [col for col in REQUIRED_CLEANED_COLUMNS if col not in df.columns]
    if missing_cols:
        logger.error(f"Missing columns in sanitized data: {missing_cols}")
        raise ValueError(f"Cleaned schema mismatch: {missing_cols}")

    if df["inkomst_tkr"].isnull().any():
        logger.warning("Sanitized dataset contains null (NaN) income values")

def validate_and_sanitize_raw_data(df: pd.DataFrame) -> pd.DataFrame:
    """Pipeline for full validation, transformation, and sanitization"""
    logger.info("Starting validation anv sanitization pipeline...")

    years_cols = validate_raw_schema(df)
    df_long = transform_to_long_format(df, years_cols)
    df_sanitized = clean_data_types(df_long)
    validate_cleaned_schema(df_sanitized)

    logger.info(f"Pipeline completed. Output shape: {df_sanitized.shape}")
    return df_sanitized

if __name__ == "__main__":
    from income_report.loading import load_raw_data

    raw_df = load_raw_data()
    clean_df = validate_and_sanitize_raw_data(raw_df)

    print("\n--- VALIDATED & SANITIZED HEAD ---")
    print(clean_df.head())