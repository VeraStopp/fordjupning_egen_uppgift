import pandas as pd

from income_report.config import (
    PROCESSED_DATA_PATH,
    logger
)

from income_report.loading import load_raw_data
from income_report.validation import validate_and_sanitize_raw_data

def get_yearly_extreme_groups(df: pd.DataFrame) -> pd.DataFrame:
    """Finds the highest and lowest income group for each individual year"""
    max_idx = df.groupby("year")["inkomst_tkr"].idxmax()
    min_idx = df.groupby("year")["inkomst_tkr"].idxmin()

    highest_per_year = df.loc[max_idx].copy()
    highest_per_year["typ"] = "högst"

    lowest_per_year = df.loc[min_idx].copy()
    lowest_per_year["typ"] = "lägst"

    yearly_extremes = (
        pd.concat([highest_per_year, lowest_per_year])
        .sort_values(by=["year", "typ"], ascending=[True, False])
        .reset_index(drop=True)
    )

    logger.info("Successfully calculated yearly income extremes")
    return yearly_extremes

def get_gender_income_over_time(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregates average income per year and gender"""
    gender_df = (
        df.groupby(["year", "kön"])["inkomst_tkr"]
        .mean()
        .reset_index()
    )

    logger.info("Calculated average income over time per gender")
    return gender_df

def get_gender_gap_data(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates average income by gender and percentage gap per year"""
    gender_yearly = (
        df.groupby(["year", "kön"])["inkomst_tkr"]
        .mean()
        .unstack(level="kön")
        .reset_index()
    )

    if "män" in gender_yearly.columns and "kvinnor" in gender_yearly.columns:
        gender_yearly["gap_pct"] = (
            (gender_yearly["män"] - gender_yearly["kvinnor"]) / gender_yearly["män"]
        ) * 100
        logger.info("Successfully calculated gender income gap percentage")
    else:
        logger.warning("Columns 'män' or 'kvinnor' are missing for gap calculation")

    return gender_yearly


def get_age_income_profile(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregates average income per age group across the dataset to identify peak earning age"""
    age_df = (
        df.groupby("ålder")["inkomst_tkr"]
        .mean()
        .reset_index()
        .sort_values(by="ålder")
    )

    logger.info("Calculated age-income profile")
    return age_df

def get_education_income_over_time(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregates average income per year and education level"""
    edu_df = (
        df.groupby(["year", "utbildningsnivå"])["inkomst_tkr"]
        .mean()
        .reset_index()
    )

    logger.info("Calculated average income over time per education level")

    return edu_df


def save_processed_data(results: dict[str, pd.DataFrame]) -> None:
    """Saves the final processed DataFrame to the designated CSV path"""
    PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

    results["cleaned_data"].to_csv(PROCESSED_DATA_PATH, index=False, encoding="utf-8")

    extreme_path = PROCESSED_DATA_PATH.parent / "yearly_income_extremes.csv"
    results["yearly_extremes"].to_csv(extreme_path, index=False, encoding="utf-8")

    gender_gap_path = PROCESSED_DATA_PATH.parent / "gender_gap_summary.csv"
    results["gender_gap"].to_csv(gender_gap_path, index=False, encoding="utf-8")

    logger.info(f"Saved processed data to: {PROCESSED_DATA_PATH}")
    logger.info(f"Saved yearly extremes table to: {extreme_path}")
    logger.info(f"Saved gender gap table to: {gender_gap_path}")

def run_processing_pipeline() -> pd. DataFrame:
    """Executes the full end-to-end data processing pipeline"""
    logger.info("Starting processing pipeline execution...")

    raw_df = load_raw_data()
    cleaned_df = validate_and_sanitize_raw_data(raw_df)


    results = {
        "cleaned_data": cleaned_df,
        "yearly_extremes": get_yearly_extreme_groups(cleaned_df),
        "gender_over_time": get_gender_income_over_time(cleaned_df),
        "gender_gap": get_gender_gap_data(cleaned_df),
        "age_profile": get_age_income_profile(cleaned_df),
        "education_over_time": get_education_income_over_time(cleaned_df),

    }

    save_processed_data(results)

    logger.info("Processing pipeline executed successfully")
    return results
    

if __name__ == "__main__":
    results = run_processing_pipeline()

    print("\n--- CLEANED DATA HEAD ---")
    print(results["cleaned_data"].head())

    print("\n--- YEARLY EXTREMES HEAD ---")
    print(results["yearly_extremes"].head())

    print("\n--- GENDER GAP HEAD ---")
    print(results["gender_gap"].head())