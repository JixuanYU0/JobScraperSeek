"""Pydantic models for API request/response validation."""

from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, HttpUrl


class JobStatus(str, Enum):
    """Job scraping status enum."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class JobResponse(BaseModel):
    """Job response model matching the Job dataclass."""
    title: str
    company: str
    location: str
    classification: str
    subcategory: str
    job_url: str
    posted_date: Optional[str] = None
    salary: Optional[str] = None
    job_type: Optional[str] = None
    description: Optional[str] = None
    scraped_at: str
    job_id: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "HR Manager",
                "company": "Tech Corp",
                "location": "Sydney NSW",
                "classification": "Human Resources & Recruitment",
                "subcategory": "Human Resources Management",
                "job_url": "https://www.seek.com.au/job/12345678",
                "posted_date": "2d ago",
                "salary": "$80,000 - $100,000",
                "description": "We are looking for an experienced HR Manager...",
                "scraped_at": "2025-10-14T10:30:00",
                "job_id": "12345678"
            }
        }


class ScrapeRequest(BaseModel):
    """Request model for triggering a scrape."""
    config_path: Optional[str] = Field(
        None,
        description="Path to custom config file (optional)"
    )
    headless: Optional[bool] = Field(
        True,
        description="Run browser in headless mode"
    )
    max_pages: Optional[int] = Field(
        None,
        description="Override max pages to scrape"
    )
    webhook_url: Optional[HttpUrl] = Field(
        None,
        description="Webhook URL to POST results to when scraping completes"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "headless": True,
                "max_pages": 5,
                "webhook_url": "https://your-n8n-instance.com/webhook/job-results"
            }
        }


class ScrapeResponse(BaseModel):
    """Response model for scrape initiation."""
    job_id: str = Field(..., description="Unique job ID for tracking")
    status: JobStatus = Field(..., description="Current status of the scraping job")
    message: str = Field(..., description="Human-readable status message")
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        json_schema_extra = {
            "example": {
                "job_id": "scrape_20251014_103045_abc123",
                "status": "pending",
                "message": "Scraping job queued successfully",
                "created_at": "2025-10-14T10:30:45"
            }
        }


class ScrapeStatusResponse(BaseModel):
    """Response model for scrape status check."""
    job_id: str
    status: JobStatus
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    jobs_found: Optional[int] = None
    jobs_new: Optional[int] = None
    error: Optional[str] = None
    results: Optional[List[JobResponse]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "job_id": "scrape_20251014_103045_abc123",
                "status": "completed",
                "created_at": "2025-10-14T10:30:45",
                "started_at": "2025-10-14T10:30:46",
                "completed_at": "2025-10-14T10:35:12",
                "jobs_found": 45,
                "jobs_new": 12,
                "results": []
            }
        }


class JobsListResponse(BaseModel):
    """Response model for jobs list endpoint."""
    total: int = Field(..., description="Total number of jobs")
    page: int = Field(1, description="Current page number")
    page_size: int = Field(50, description="Number of items per page")
    jobs: List[JobResponse] = Field(..., description="List of jobs")

    class Config:
        json_schema_extra = {
            "example": {
                "total": 150,
                "page": 1,
                "page_size": 50,
                "jobs": []
            }
        }


class WebhookRegistration(BaseModel):
    """Model for registering a webhook."""
    webhook_url: HttpUrl = Field(..., description="Webhook URL to call")
    events: List[str] = Field(
        default=["scrape.completed"],
        description="Events to trigger webhook (scrape.completed, scrape.failed)"
    )
    description: Optional[str] = Field(None, description="Webhook description")

    class Config:
        json_schema_extra = {
            "example": {
                "webhook_url": "https://your-n8n-instance.com/webhook/job-results",
                "events": ["scrape.completed", "scrape.failed"],
                "description": "n8n workflow integration"
            }
        }


class WebhookResponse(BaseModel):
    """Response model for webhook registration."""
    webhook_id: str
    webhook_url: str
    events: List[str]
    created_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "webhook_id": "webhook_abc123",
                "webhook_url": "https://your-n8n-instance.com/webhook/job-results",
                "events": ["scrape.completed"],
                "created_at": "2025-10-14T10:30:45"
            }
        }


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field("healthy", description="Service health status")
    version: str = Field("1.0.0", description="API version")
    timestamp: datetime = Field(default_factory=datetime.now)
    components: Dict[str, str] = Field(
        default_factory=dict,
        description="Status of service components"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "version": "1.0.0",
                "timestamp": "2025-10-14T10:30:45",
                "components": {
                    "database": "connected",
                    "scraper": "ready",
                    "storage": "available"
                }
            }
        }


class ErrorResponse(BaseModel):
    """Standard error response."""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    detail: Optional[Any] = Field(None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.now)

    class Config:
        json_schema_extra = {
            "example": {
                "error": "ValidationError",
                "message": "Invalid request parameters",
                "detail": {"field": "max_pages", "issue": "Must be positive integer"},
                "timestamp": "2025-10-14T10:30:45"
            }
        }
