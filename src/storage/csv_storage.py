"""CSV file storage backend."""

import csv
import logging
from pathlib import Path
from typing import List

from ..models import Job
from .base_storage import BaseStorage


class CSVStorage(BaseStorage):
    """CSV file-based storage."""

    def __init__(self, output_path: Path):
        """Initialize CSV storage.

        Args:
            output_path: Path to output CSV file
        """
        self.output_path = output_path
        self.logger = logging.getLogger(__name__)

        # Ensure directory exists
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

    def save(self, jobs: List[Job]) -> None:
        """Save jobs to CSV file.

        Args:
            jobs: List of Job objects to save
        """
        if not jobs:
            self.logger.warning("No jobs to save")
            return

        fieldnames = [
            "title",
            "company",
            "location",
            "classification",
            "subcategory",
            "job_url",
            "salary",
            "posted_date",
            "description",
            "scraped_at"
        ]

        with open(self.output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for job in jobs:
                writer.writerow(job.to_dict())

        self.logger.info(f"Saved {len(jobs)} jobs to {self.output_path}")

    def load(self) -> List[Job]:
        """Load jobs from CSV file.

        Returns:
            List of Job objects
        """
        if not self.output_path.exists():
            return []

        jobs = []
        with open(self.output_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                jobs.append(Job.from_dict(row))

        return jobs

    def exists(self, job: Job) -> bool:
        """Check if job already exists in CSV.

        Args:
            job: Job to check

        Returns:
            True if job exists
        """
        existing_jobs = self.load()
        return job in existing_jobs
