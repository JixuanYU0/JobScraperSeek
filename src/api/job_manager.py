"""Job manager for handling async scraping tasks."""

import uuid
import asyncio
from datetime import datetime
from typing import Dict, Optional, List
from pathlib import Path
import threading
import requests

from .models import JobStatus, ScrapeRequest
from ..utils import Config, setup_logger
from ..scraper import SeekScraper
from ..storage import JSONStorage
from ..utils.deduplicator import Deduplicator
from ..models import Job


class ScrapeJob:
    """Represents a single scraping job."""

    def __init__(self, job_id: str, request: ScrapeRequest):
        self.job_id = job_id
        self.request = request
        self.status = JobStatus.PENDING
        self.created_at = datetime.now()
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None
        self.jobs_found: Optional[int] = None
        self.jobs_new: Optional[int] = None
        self.error: Optional[str] = None
        self.results: List[Job] = []


class JobManager:
    """Manages scraping jobs and their lifecycle."""

    def __init__(self):
        self.jobs: Dict[str, ScrapeJob] = {}
        self.lock = threading.Lock()
        self.webhooks: Dict[str, dict] = {}

    def create_job(self, request: ScrapeRequest) -> str:
        """Create a new scraping job and return its ID."""
        job_id = f"scrape_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"

        with self.lock:
            job = ScrapeJob(job_id, request)
            self.jobs[job_id] = job

        return job_id

    def get_job(self, job_id: str) -> Optional[ScrapeJob]:
        """Get a job by ID."""
        with self.lock:
            return self.jobs.get(job_id)

    def list_jobs(self, status: Optional[JobStatus] = None, limit: int = 100) -> List[ScrapeJob]:
        """List all jobs, optionally filtered by status."""
        with self.lock:
            jobs = list(self.jobs.values())

        if status:
            jobs = [j for j in jobs if j.status == status]

        # Sort by created_at descending
        jobs.sort(key=lambda x: x.created_at, reverse=True)

        return jobs[:limit]

    def update_job_status(self, job_id: str, status: JobStatus, **kwargs):
        """Update job status and related fields."""
        with self.lock:
            if job_id in self.jobs:
                job = self.jobs[job_id]
                job.status = status

                if status == JobStatus.RUNNING and not job.started_at:
                    job.started_at = datetime.now()
                elif status in [JobStatus.COMPLETED, JobStatus.FAILED]:
                    job.completed_at = datetime.now()

                for key, value in kwargs.items():
                    setattr(job, key, value)

    def register_webhook(self, webhook_url: str, events: List[str], description: Optional[str] = None) -> str:
        """Register a webhook for job events."""
        webhook_id = f"webhook_{uuid.uuid4().hex[:8]}"

        with self.lock:
            self.webhooks[webhook_id] = {
                "url": webhook_url,
                "events": events,
                "description": description,
                "created_at": datetime.now()
            }

        return webhook_id

    def get_webhooks(self) -> Dict[str, dict]:
        """Get all registered webhooks."""
        with self.lock:
            return self.webhooks.copy()

    def delete_webhook(self, webhook_id: str) -> bool:
        """Delete a webhook."""
        with self.lock:
            if webhook_id in self.webhooks:
                del self.webhooks[webhook_id]
                return True
            return False

    def trigger_webhooks(self, event: str, job_id: str, data: dict):
        """Trigger webhooks for a specific event."""
        webhooks_to_call = []

        with self.lock:
            for webhook_id, webhook in self.webhooks.items():
                if event in webhook["events"]:
                    webhooks_to_call.append(webhook["url"])

        # Call webhooks without blocking
        for url in webhooks_to_call:
            try:
                payload = {
                    "event": event,
                    "job_id": job_id,
                    "data": data,
                    "timestamp": datetime.now().isoformat()
                }
                requests.post(url, json=payload, timeout=10)
            except Exception as e:
                print(f"Failed to call webhook {url}: {e}")

    async def run_scrape_job(self, job_id: str):
        """Execute a scraping job asynchronously."""
        job = self.get_job(job_id)
        if not job:
            return

        try:
            # Update status to running
            self.update_job_status(job_id, JobStatus.RUNNING)

            # Load config
            config_path = job.request.config_path
            config = Config(config_path) if config_path else Config()

            # Override headless setting
            if job.request.headless is not None:
                config._config["scraper"]["headless"] = job.request.headless

            # Override max_pages if provided
            if job.request.max_pages is not None:
                config._config["scraper"]["max_pages"] = job.request.max_pages

            # Setup logger
            logger = setup_logger(
                name=f"scraper_{job_id}",
                log_file=config.get_log_path(),
                level=config.get("logging.level", "INFO"),
                console=False
            )

            # Run scraper in thread pool (Playwright is sync)
            loop = asyncio.get_event_loop()
            jobs = await loop.run_in_executor(
                None,
                self._run_scraper_sync,
                config,
                logger
            )

            if not jobs:
                self.update_job_status(
                    job_id,
                    JobStatus.COMPLETED,
                    jobs_found=0,
                    jobs_new=0,
                    results=[]
                )
                return

            # Initialize storage
            json_storage = JSONStorage(
                output_path=config.get_output_path("json"),
                seen_jobs_path=config.get_seen_jobs_path(),
                retention_days=config.get("deduplication.retention_days", 30)
            )

            # Deduplication
            deduplicator = Deduplicator(
                storage=json_storage,
                key_field=config.get("deduplication.key_field", "job_url")
            )

            jobs_found = len(jobs)
            jobs = deduplicator.remove_within_batch_duplicates(jobs)
            new_jobs = deduplicator.filter_new_jobs(jobs)

            # Save to storage
            if new_jobs:
                json_storage.save(new_jobs)

            # Update job status
            self.update_job_status(
                job_id,
                JobStatus.COMPLETED,
                jobs_found=jobs_found,
                jobs_new=len(new_jobs),
                results=new_jobs
            )

            # Trigger webhooks
            webhook_data = {
                "jobs_found": jobs_found,
                "jobs_new": len(new_jobs),
                "jobs": [job.to_dict() for job in new_jobs[:10]]  # Send first 10 jobs
            }

            # Call job-specific webhook if provided
            if job.request.webhook_url:
                try:
                    requests.post(str(job.request.webhook_url), json=webhook_data, timeout=10)
                except Exception as e:
                    logger.error(f"Failed to call job webhook: {e}")

            # Call registered webhooks
            self.trigger_webhooks("scrape.completed", job_id, webhook_data)

        except Exception as e:
            error_msg = str(e)
            self.update_job_status(
                job_id,
                JobStatus.FAILED,
                error=error_msg
            )

            # Trigger failure webhooks
            self.trigger_webhooks("scrape.failed", job_id, {"error": error_msg})

    def _run_scraper_sync(self, config: Config, logger) -> List[Job]:
        """Run scraper synchronously (for thread pool execution)."""
        scraper = SeekScraper(config, logger)
        return scraper.scrape()


# Global job manager instance
job_manager = JobManager()
