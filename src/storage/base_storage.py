"""Base storage interface."""

from abc import ABC, abstractmethod
from typing import List

from ..models import Job


class BaseStorage(ABC):
    """Abstract base class for storage backends."""

    @abstractmethod
    def save(self, jobs: List[Job]) -> None:
        """Save jobs to storage.

        Args:
            jobs: List of Job objects to save
        """
        pass

    @abstractmethod
    def load(self) -> List[Job]:
        """Load jobs from storage.

        Returns:
            List of Job objects
        """
        pass

    @abstractmethod
    def exists(self, job: Job) -> bool:
        """Check if job already exists in storage.

        Args:
            job: Job to check

        Returns:
            True if job exists
        """
        pass
