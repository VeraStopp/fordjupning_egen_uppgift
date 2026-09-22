import subprocess
from pathlib import Path
from income_report.config import logger
from income_report.visualization import generate_all_plots

def render_quarto_report(qmd_path: str = "report.qmd", output_format: str = "pdf") -> None:
    """Triggers Quarto CLI to render the report document"""
    report_file = Path(qmd_path)

    if not report_file.exists():
        logger.error(f"Report template not found at {qmd_path}")
        raise FileNotFoundError(f"Could not find {qmd_path}")

    logger.info(f"Rendering Quarto report ({qmd_path}) to {output_format.upper()}...")

    try:
        cmd = ["quarto", "render", str(report_file), "--to", output_format]
        subprocess.run(cmd, check=True)
        logger.info("Quarto report rendered successfully!")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to render Quarto report: {e}")
        raise e
    except FileNotFoundError:
        logger.error(f"Quarto CLI is not installed or not found in PATH")
        raise

def run_full_reporting_pipeline() -> None:
    """Runs the entire pipeline from visualization generation to final Quarto render"""
    logger.info("Starting full reporting pipeline execution...")

    generate_all_plots()

    render_quarto_report()

if __name__ == "__main__":
    run_full_reporting_pipeline()