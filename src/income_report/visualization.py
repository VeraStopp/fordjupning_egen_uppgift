from pathlib import Path
import matplotlib.pyplot as plt 
import pandas as pd
import seaborn as sns

from income_report.config import logger
from income_report.processing import run_processing_pipeline

sns.set_theme(style="whitegrid")
FIGURES_DIR = Path("reports/figures")

def setup_figures_dir() -> None:
    """Ensures that the output directory for figures exists"""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

def plot_education_trends(df: pd.DataFrame) -> None:
    """Generates a line plot showing average income over time per education level"""
    plt.figure(figsize=(10, 6))

    sns.lineplot(
        data=df,
        x="year",
        y="inkomst_tkr",
        hue="utbildningsnivå",
        marker="o",
        linewidth=2.5
    )

    plt.title("Utbildningens avkastning över tid", fontsize=14, pad=15)
    plt.xlabel("År", fontsize=12)
    plt.ylabel("Medelinkomst (tkr)", fontsize=12)
    plt.legend(title="Utbildningsnivå", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()

    output_path = FIGURES_DIR / "education_income_over_time.png"
    plt.savefig(output_path, dpi=300)
    plt.close()
    logger.info(f"Saved education trend plot to: {output_path}")