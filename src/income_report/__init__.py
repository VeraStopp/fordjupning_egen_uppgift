"""
Income Report Package

A modular data pipeline for processing SCB income data, generating visualizations and buliding dynacim PDF reports.
"""

from income_report.__main__ import main
from income_report.processing import run_processing_pipeline
from income_report.reporting import run_full_reporting_pipeline
from income_report.visualization import generate_all_plots

__version__="0.1.0"

__all__ = [
    "main",
    "run_processing_pipeline",
    "run_full_reporting_pipeline",
    "generate_all_plots",
    "__version__"
]