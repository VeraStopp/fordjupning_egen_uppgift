from income_report.processing import run_processing_pipeline
from income_report.visualization import generate_all_plots
from income_report.reporting import run_full_reporting_pipeline
from income_report.config import logger

def main():
    """Main entry point for the income report application"""
    logger.info("Starting SCB Income Analysis Pipeline")
    try: 
        run_processing_pipeline()
        logger.info("Data processing completed successfully")

        generate_all_plots()
        logger.info("Plots generated completed successfully")

        run_full_reporting_pipeline()
        logger.info("Reporting pipeline completed successfully")

        logger.info("Pipeline executed successfully! All output files are ready")

    except Exception as e:
        logger.error(f"Pipeline failed during execution. Error: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()