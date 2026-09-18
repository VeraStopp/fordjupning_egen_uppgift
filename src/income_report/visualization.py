from pathlib import Path
import matplotlib.pyplot as plt 
import pandas as pd
import seaborn as sns

from income_report.config import logger, FIGURES_DIR
from income_report.processing import run_processing_pipeline

sns.set_theme(style="whitegrid")

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

def plot_yearly_extremes(df: pd.DataFrame) -> None:
    """Generates a grouped bar chart comparing yearly highest and lowest income groups"""
    plt.figure(figsize=(12, 6))

    sns.barplot(
        data=df,
        x="year",
        y="inkomst_tkr",
        hue="typ",
        palette={"högst": "#2b5c8f", "lägst": "#d95f02"}
    )

    plt.title("Skillnad mellan högsta och lägsta inkomstgrupp per år", fontsize=14, pad=15)
    plt.xlabel("År", fontsize=12)
    plt.ylabel("Inkomst (tkr)", fontsize=12)
    plt.legend(title="Typ")
    plt.tight_layout()

    output_path = FIGURES_DIR / "yearly_income_extremes.png"
    plt.savefig(output_path, dpi=300)
    plt.close()
    logger.info(f"Saved yearly extremes plot to: {output_path}")

def plot_gender_trends(df: pd.DataFrame) -> None:
    """Generates a line plot comparing male and female average income over time"""
    plt.figure(figsize=(12, 6))

    sns.lineplot(
        data=df,
        x="year",
        y="inkomst_tkr",
        hue="kön",
        marker="s",
        linewidth=2.5,
        palette={"män": "#1f77b4", "kvinnor": "#e377c2"}
    )

    plt.title("Könens inkomstutveckling över tid", fontsize=14, pad=15)
    plt.xlabel("År", fontsize=12)
    plt.ylabel("Medelinkomst (tkr)", fontsize=12)
    plt.legend(title="Kön")
    plt.tight_layout()

    output_path = FIGURES_DIR / "gender_income_over_time.png"
    plt.savefig(output_path, dpi=300)
    plt.close()
    logger.info(f"Saved gender trend plot to: {output_path}")

def plot_age_profile_bar(df: pd.DataFrame) -> None:
    """Generates a bar chart showing the age-income profile"""
    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=df,
        x="ålder",
        y="inkomst_tkr",
        color="green"
    )

    plt.title("Lönekarriär: Medelinkomst per åldersgrupp (Stapeldiagram)", fontsize=14, pad=15)
    plt.xlabel("Åldersgrupp", fontsize=12)
    plt.ylabel("Medelinkomst (tkr)", fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()

    output_path = FIGURES_DIR / "age_income_profile_bar.png"
    plt.savefig(output_path, dpi=300)
    plt.close()
    logger.info(f"Saved age profile bar plot to: {output_path}")

def plot_age_profile_line(df: pd.DataFrame) -> None:
    """Generates a line plot showing the age-income profile"""
    plt.figure(figsize=(10, 6))

    sns.lineplot(
        data=df,
        x="ålder",
        y="inkomst_tkr",
        marker="o",
        linewidth=2.5,
        color="#3182bd"
    )

    plt.title("Lönekarriär: Medelinkomst per åldersgrupp (Linjediagram)", fontsize=14, pad=15)
    plt.xlabel("Åldersgrupp", fontsize=12)
    plt.ylabel("Medelinkomst (tkr)", fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()

    output_path = FIGURES_DIR / "age_income_profile_line.png"
    plt.savefig(output_path, dpi=300)
    plt.close()
    logger.info(f"Saved age profile line plot to: {output_path}")
    


def generate_all_plots() -> None:
    """Runs the processing pipeline and generates all figure reports"""
    logger.info("Starting visualization process...")
    setup_figures_dir()

    results = run_processing_pipeline()

    plot_education_trends(results["education_over_time"])
    plot_yearly_extremes(results["yearly_extremes"])
    plot_gender_trends(results["gender_over_time"])
    plot_age_profile_bar(results["age_profile"])
    plot_age_profile_line(results["age_profile"])

    logger.info("All visualization plots generated successfully")
    


if __name__ == "__main__":
    generate_all_plots()