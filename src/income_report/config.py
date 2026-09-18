import logging 
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"

def get_raw_data_path() -> Path:
    """Locates the first CSV file in the data/raw directory"""
    raw_folder = DATA_DIR / "raw"
    csv_files = list(raw_folder.glob("*.csv"))

    if not csv_files:
        raise FileNotFoundError(f"No CSV file found in {raw_folder}")
    if len(csv_files) > 1:
        print(f"Warning: Multiple CSV files found. Using: {csv_files[0].name}")

    return csv_files[0]

RAW_DATA_PATH = get_raw_data_path()
PROCESSED_DATA_PATH = DATA_DIR / "processed" / "scb_income_cleaned.csv"

OUTPUT_DIR = BASE_DIR / "output"
FIGURES_DIR = OUTPUT_DIR / "figures"

CSV_ENCODING = "latin1"
CSV_SKIPROWS = 2

REQUIRED_RAW_METADATA_COLUMNS = [
    "region",
    "utbildningsnivå",
    "kön",
    "ålder",
    "inkomstklass"
]

REQUIRED_CLEANED_COLUMNS = [
    "utbildningsnivå",
    "kön",
    "ålder",
    "year",
    "inkomst_tkr"
]

LOG_FILE = BASE_DIR / "income_report.log"
LOGGER_NAME = "income_report"

def configure_logging() -> None:
    """Configures package specific logging for income_report"""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    package_logger = logging.getLogger(LOGGER_NAME)
    if package_logger.handlers:
        return

    package_logger.setLevel(logging.DEBUG)
    package_logger.propagate = False

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8",
    )

    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    package_logger.addHandler(console_handler)
    package_logger.addHandler(file_handler)

configure_logging()
logger = logging.getLogger(LOGGER_NAME)

