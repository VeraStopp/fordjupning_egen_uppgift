import pandas as pd 
from income_report.config import (
    RAW_DATA_PATH,
    CSV_ENCODING,
    CSV_SKIPROWS,
    logger,
)

def load_raw_data() -> pd.DataFrame:
    """
    Loads raw income CSV data exported from SCB using project configurations.

    Returns:
        pd.DataFrame: Loaded raw dataset.

    Raises:
        FileNotFoundError: If the raw data CSV file does not exist.
        ValueError: If the file is empty or cannot be parsed.
    """
    logger.info(f"Loading raw data from: {RAW_DATA_PATH}")

    if not RAW_DATA_PATH.exists():
        logger.error(f"File nor found: {RAW_DATA_PATH}")
        raise FileNotFoundError(f"Raw data file missing at {RAW_DATA_PATH}")

    try:
        df = pd.read_csv(
            RAW_DATA_PATH,
            encoding=CSV_ENCODING,
            skiprows=CSV_SKIPROWS,
            dtype=str,
        )

        df.columns = df.columns.str.strip()

        logger.info(f"Successfully loaded raw data. Shape: {df.shape} (rows, columns)")

        return df

    except Exception as e:
        logger.error(f"Failed to load raw data from {RAW_DATA_PATH}. Error: {e}")
        raise ValueError(f"Could nor parse raw CSV data: {e}") from e

if __name__ == "__main__":
    raw_df = load_raw_data()
    print("\n--- FIRST 5 ROWS ---")
    print(raw_df.head())