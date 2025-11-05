"""Deduplication utilities for job listings."""

import logging
from typing import List, Set

from ..models import Job
from ..storage import BaseStorage


class Deduplicator:
    """Handle deduplication of job listings."""

    def __init__(self, storage: BaseStorage, key_field: str = "job_url"):
        """Initialize deduplicator.

        Args:
            storage: Storage backend for tracking seen jobs
            key_field: Field to use as unique identifier
        """
        self.storage = storage
        self.key_field = key_field
        self.logger = logging.getLogger(__name__)

    def filter_new_jobs(self, jobs: List[Job]) -> List[Job]:
        """Filter out jobs that have been seen before.

        Args:
            jobs: List of scraped jobs

        Returns:
            List of new (unseen) jobs
        """
        new_jobs = []
        seen_count = 0

        for job in jobs:
            if not self.storage.exists(job):
                new_jobs.append(job)
            else:
                seen_count += 1
                self.logger.debug(f"Skipping duplicate: {job.title} - {job.company}")

        self.logger.info(f"Filtered {seen_count} duplicates, {len(new_jobs)} new jobs")
        return new_jobs

    def remove_within_batch_duplicates(self, jobs: List[Job]) -> List[Job]:
        """Remove duplicates within a single batch of jobs.

        Args:
            jobs: List of jobs

        Returns:
            List of unique jobs
        """
        seen: Set[str] = set()
        unique_jobs = []

        for job in jobs:
            key = getattr(job, self.key_field)
            if key not in seen:
                seen.add(key)
                unique_jobs.append(job)
            else:
                self.logger.debug(f"Removing duplicate within batch: {job.title}")

        if len(unique_jobs) < len(jobs):
            self.logger.info(f"Removed {len(jobs) - len(unique_jobs)} duplicates within batch")

        return unique_jobs
