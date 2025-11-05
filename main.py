"""Main entry point for the Seek job scraper."""

import sys
import argparse
from pathlib import Path

from src.utils import Config, setup_logger
from src.scraper import SeekScraper
from src.storage import JSONStorage, CSVStorage
from src.utils.deduplicator import Deduplicator
from src.models import Job


def main():
    """Main execution function."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Seek HR & Recruitment Job Scraper")
    parser.add_argument(
        "--config",
        type=str,
        help="Path to config file (default: config/config.yaml)"
    )
    parser.add_argument(
        "--no-dedup",
        action="store_true",
        help="Disable deduplication"
    )
    parser.add_argument(
        "--output-format",
        choices=["json", "csv", "both"],
        default="json",
        help="Output format (default: json)"
    )
    parser.add_argument(
        "--headless",
        type=lambda x: x.lower() in ["true", "1", "yes"],
        default=None,
        help="Run browser in headless mode (true/false)"
    )

    args = parser.parse_args()

    # Load configuration
    try:
        config = Config(args.config) if args.config else Config()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Override headless setting if provided
    if args.headless is not None:
        config._config["scraper"]["headless"] = args.headless

    # Setup logging
    logger = setup_logger(
        name="seek_scraper",
        log_file=config.get_log_path(),
        level=config.get("logging.level", "INFO"),
        console=config.get("logging.console", True),
        log_format=config.get("logging.format")
    )

    logger.info("=" * 60)
    logger.info("Seek Job Scraper - Starting")
    logger.info("=" * 60)

    try:
        # Initialize scraper
        scraper = SeekScraper(config, logger)

        # Scrape jobs
        logger.info("Starting scraping process...")
        jobs = scraper.scrape()

        if not jobs:
            logger.warning("No jobs found")
            return

        # Initialize storage
        json_storage = JSONStorage(
            output_path=config.get_output_path("json"),
            seen_jobs_path=config.get_seen_jobs_path(),
            retention_days=config.get("deduplication.retention_days", 30)
        )

        # Deduplication
        if not args.no_dedup:
            logger.info("Running deduplication...")
            deduplicator = Deduplicator(
                storage=json_storage,
                key_field=config.get("deduplication.key_field", "job_url")
            )

            # Remove duplicates within batch
            jobs = deduplicator.remove_within_batch_duplicates(jobs)

            # Filter out previously seen jobs
            new_jobs = deduplicator.filter_new_jobs(jobs)

            logger.info(f"New jobs to save: {len(new_jobs)}")
            jobs = new_jobs

        if not jobs:
            logger.info("No new jobs to save after deduplication")
            return

        # Save to storage
        if args.output_format in ["json", "both"]:
            logger.info("Saving to JSON...")
            json_storage.save(jobs)

        if args.output_format in ["csv", "both"]:
            logger.info("Saving to CSV...")
            csv_storage = CSVStorage(config.get_output_path("csv"))
            csv_storage.save(jobs)

        # Summary
        logger.info("=" * 60)
        logger.info("Scraping completed successfully")
        logger.info(f"Total jobs scraped: {len(jobs)}")
        logger.info(f"Output format: {args.output_format}")
        logger.info("=" * 60)

        # Print sample
        if jobs:
            logger.info("\nSample job:")
            sample = jobs[0]
            logger.info(f"  Title: {sample.title}")
            logger.info(f"  Company: {sample.company}")
            logger.info(f"  Location: {sample.location}")
            logger.info(f"  Subcategory: {sample.subcategory}")
            logger.info(f"  URL: {sample.job_url}")

    except KeyboardInterrupt:
        logger.info("Scraping interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
