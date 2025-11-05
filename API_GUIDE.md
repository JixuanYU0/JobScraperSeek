# Seek Job Scraper - API Guide

## Overview

The Seek Job Scraper now includes a **production-ready FastAPI REST API** that enables:
- Asynchronous job scraping with status tracking
- Webhook notifications (perfect for n8n integration)
- Job retrieval with filtering and pagination
- Health monitoring and observability

---

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the API Server

```bash
# Development mode (with auto-reload)
python api_server.py --reload

# Production mode
python api_server.py --host 0.0.0.0 --port 8000 --workers 4
```

### 3. Access API Documentation

Open your browser to:
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **Health Check**: http://localhost:8000/api/v1/health

---

## API Endpoints

### Health & Status

#### `GET /api/v1/health`
Check API health and component status.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2025-10-14T10:30:45",
  "components": {
    "config": "loaded",
    "storage": "available",
    "scraper": "ready",
    "job_queue": "operational"
  }
}
```

---

### Scraping Operations

#### `POST /api/v1/scrape`
Trigger a new scraping job (async - returns immediately).

**Request Body:**
```json
{
  "headless": true,
  "max_pages": 5,
  "webhook_url": "https://your-n8n-instance.com/webhook/job-results"
}
```

**Response:**
```json
{
  "job_id": "scrape_20251014_103045_abc123",
  "status": "pending",
  "message": "Scraping job queued successfully",
  "created_at": "2025-10-14T10:30:45"
}
```

---

#### `GET /api/v1/scrape/{job_id}`
Check status of a scraping job.

**Response:**
```json
{
  "job_id": "scrape_20251014_103045_abc123",
  "status": "completed",
  "created_at": "2025-10-14T10:30:45",
  "started_at": "2025-10-14T10:30:46",
  "completed_at": "2025-10-14T10:35:12",
  "jobs_found": 45,
  "jobs_new": 12,
  "results": [...]
}
```

**Status Values:**
- `pending` - Job queued, not started yet
- `running` - Currently scraping
- `completed` - Finished successfully
- `failed` - Encountered an error

---

#### `GET /api/v1/scrape`
List all scraping jobs.

**Query Parameters:**
- `status` (optional): Filter by status (pending/running/completed/failed)
- `limit` (default: 100): Maximum jobs to return

**Response:**
```json
[
  {
    "job_id": "scrape_20251014_103045_abc123",
    "status": "completed",
    "jobs_found": 45,
    "jobs_new": 12,
    ...
  }
]
```

---

### Job Retrieval

#### `GET /api/v1/jobs`
List all scraped jobs with pagination.

**Query Parameters:**
- `page` (default: 1): Page number
- `page_size` (default: 50): Items per page
- `company` (optional): Filter by company name
- `location` (optional): Filter by location

**Response:**
```json
{
  "total": 150,
  "page": 1,
  "page_size": 50,
  "jobs": [...]
}
```

---

#### `GET /api/v1/jobs/latest`
Get the most recent jobs.

**Query Parameters:**
- `limit` (default: 20): Number of jobs to return

**Response:**
```json
[
  {
    "title": "HR Manager",
    "company": "Tech Corp",
    "location": "Sydney NSW",
    "classification": "Human Resources & Recruitment",
    "subcategory": "Human Resources Management",
    "job_url": "https://www.seek.com.au/job/12345678",
    "posted_date": "2d ago",
    "salary": "$80,000 - $100,000",
    "scraped_at": "2025-10-14T10:30:00",
    "job_id": "12345678"
  }
]
```

---

#### `GET /api/v1/jobs/{job_id}`
Get a specific job by ID.

**Response:**
```json
{
  "title": "HR Manager",
  "company": "Tech Corp",
  ...
}
```

---

### Webhook Management

#### `POST /api/v1/webhooks`
Register a webhook for job notifications.

**Request Body:**
```json
{
  "webhook_url": "https://your-n8n-instance.com/webhook/job-results",
  "events": ["scrape.completed", "scrape.failed"],
  "description": "n8n workflow integration"
}
```

**Response:**
```json
{
  "webhook_id": "webhook_abc123",
  "webhook_url": "https://your-n8n-instance.com/webhook/job-results",
  "events": ["scrape.completed"],
  "created_at": "2025-10-14T10:30:45"
}
```

**Webhook Events:**
- `scrape.completed` - Called when scraping succeeds
- `scrape.failed` - Called when scraping fails

**Webhook Payload:**
```json
{
  "event": "scrape.completed",
  "job_id": "scrape_20251014_103045_abc123",
  "data": {
    "jobs_found": 45,
    "jobs_new": 12,
    "jobs": [...]
  },
  "timestamp": "2025-10-14T10:35:12"
}
```

---

#### `GET /api/v1/webhooks`
List all registered webhooks.

---

#### `DELETE /api/v1/webhooks/{webhook_id}`
Delete a webhook.

---

## Integration Examples

### n8n Workflow

#### Option 1: Trigger & Poll Pattern

1. **HTTP Request Node** - Trigger scraping
   - Method: POST
   - URL: `http://your-api-server:8000/api/v1/scrape`
   - Body: `{"headless": true, "max_pages": 5}`

2. **Wait Node** - Wait 30 seconds

3. **HTTP Request Node** - Check status
   - Method: GET
   - URL: `http://your-api-server:8000/api/v1/scrape/{{$json.job_id}}`

4. **IF Node** - Check if status is "completed"

5. **HTTP Request Node** - Get results
   - Method: GET
   - URL: `http://your-api-server:8000/api/v1/jobs/latest`

---

#### Option 2: Webhook Pattern (Recommended)

1. **Webhook Node** - Create n8n webhook
   - Copy the webhook URL

2. **HTTP Request Node** - Register webhook with API
   - Method: POST
   - URL: `http://your-api-server:8000/api/v1/webhooks`
   - Body:
     ```json
     {
       "webhook_url": "YOUR_N8N_WEBHOOK_URL",
       "events": ["scrape.completed"]
     }
     ```

3. **Schedule Node** - Trigger scraping daily
   - Cron: `0 9 * * *` (9 AM daily)

4. **HTTP Request Node** - Trigger scraping
   - Method: POST
   - URL: `http://your-api-server:8000/api/v1/scrape`

5. When scraping completes, n8n receives data automatically!

---

### cURL Examples

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Trigger scraping
curl -X POST http://localhost:8000/api/v1/scrape \
  -H "Content-Type: application/json" \
  -d '{"headless": true, "max_pages": 3}'

# Check job status
curl http://localhost:8000/api/v1/scrape/scrape_20251014_103045_abc123

# Get latest jobs
curl http://localhost:8000/api/v1/jobs/latest?limit=10

# Register webhook
curl -X POST http://localhost:8000/api/v1/webhooks \
  -H "Content-Type: application/json" \
  -d '{
    "webhook_url": "https://your-n8n.com/webhook/jobs",
    "events": ["scrape.completed"]
  }'
```

---

### Python Client Example

```python
import requests
import time

API_BASE = "http://localhost:8000/api/v1"

# Trigger scraping
response = requests.post(f"{API_BASE}/scrape", json={
    "headless": True,
    "max_pages": 5
})
job_id = response.json()["job_id"]
print(f"Job started: {job_id}")

# Poll for completion
while True:
    status_response = requests.get(f"{API_BASE}/scrape/{job_id}")
    status = status_response.json()["status"]

    print(f"Status: {status}")

    if status == "completed":
        data = status_response.json()
        print(f"Found {data['jobs_new']} new jobs!")
        break
    elif status == "failed":
        print(f"Error: {status_response.json()['error']}")
        break

    time.sleep(5)

# Get results
jobs = requests.get(f"{API_BASE}/jobs/latest?limit=20")
print(jobs.json())
```

---

## AI Agent Architecture Explained

### What Makes This an AI Agent?

This API implements the **Autonomous Agent Pattern**:

```
┌─────────────────────────────────────┐
│      USER INTENT (API Request)      │
└────────────┬────────────────────────┘
             ▼
┌─────────────────────────────────────┐
│   ORCHESTRATION (FastAPI Router)    │
│   - Parse & validate request         │
│   - Route to appropriate handler     │
│   - Manage job lifecycle             │
└────────────┬────────────────────────┘
             ▼
┌─────────────────────────────────────┐
│     AGENT CORE (Job Manager)        │
│   - Planning: What to scrape?        │
│   - Execution: Run scraping tasks    │
│   - Memory: Track seen jobs          │
│   - Feedback: Notify via webhooks    │
└────────────┬────────────────────────┘
             ▼
┌─────────────────────────────────────┐
│      TOOLS (External Actions)        │
│   - Playwright (Web Automation)      │
│   - Storage (Persistence)            │
│   - Webhooks (Notifications)         │
└─────────────────────────────────────┘
```

### Key Agent Concepts

#### 1. **Perception**
The scraper "perceives" the web environment by:
- Navigating Seek.com.au
- Reading HTML/DOM structure
- Extracting job information

#### 2. **Memory Systems**
- **Short-term**: Current scrape results in job queue
- **Long-term**: Deduplication database (seen_jobs.json)
- **Episodic**: Job history and status tracking

#### 3. **Reasoning**
The agent makes decisions:
- Which jobs match filters?
- Have I seen this job before?
- Should I notify webhooks?

#### 4. **Action**
The agent performs actions:
- Save jobs to storage
- Trigger webhook notifications
- Update job status

#### 5. **Autonomy**
Once triggered, the agent runs independently:
- No human intervention needed
- Self-manages errors
- Reports back via webhooks

---

## Production Deployment

### Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install chromium
RUN playwright install-deps chromium

# Copy application
COPY . .

# Expose API port
EXPOSE 8000

# Run API server
CMD ["python", "api_server.py", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

Build and run:
```bash
docker build -t seek-scraper-api .
docker run -p 8000:8000 -v $(pwd)/data:/app/data seek-scraper-api
```

---

### Environment Variables

Create `.env` file:

```bash
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4

# Scraper Configuration
CONFIG_PATH=config/config.yaml

# Logging
LOG_LEVEL=INFO
```

---

### Security Considerations (Optional - Future Enhancement)

For production, consider adding:

1. **API Key Authentication**
   ```python
   from fastapi.security import APIKeyHeader
   ```

2. **Rate Limiting**
   ```bash
   pip install slowapi
   ```

3. **HTTPS/TLS**
   - Use reverse proxy (Nginx, Traefik)
   - Let's Encrypt for SSL certificates

4. **CORS Configuration**
   - Restrict `allow_origins` in production

---

## Monitoring & Observability

### Health Checks

```bash
# Kubernetes liveness probe
curl http://localhost:8000/api/v1/health
```

### Metrics to Monitor

1. **Request Latency**
   - P50, P95, P99 response times
   - Track scraping job duration

2. **Success Rate**
   - % of successful scrapes
   - Error rates by type

3. **Resource Usage**
   - CPU and memory per worker
   - Storage disk usage

4. **Business Metrics**
   - Jobs scraped per day
   - New jobs discovered
   - Webhook delivery success rate

---

## Troubleshooting

### Issue: Jobs not appearing in results

**Solution:**
- Check deduplication settings in `config/config.yaml`
- Use `--no-dedup` flag or disable in API request

### Issue: Scraping job stuck in "running"

**Solution:**
- Check logs in `logs/` directory
- Playwright may have crashed - restart API server
- Increase timeout in scraper config

### Issue: Webhook not being called

**Solution:**
- Verify webhook URL is accessible
- Check webhook registration: `GET /api/v1/webhooks`
- Test webhook with curl manually

---

## Advanced Usage

### Custom Configuration per Scrape

```json
POST /api/v1/scrape
{
  "config_path": "config/custom_config.yaml",
  "max_pages": 10,
  "webhook_url": "https://..."
}
```

### Filtering Jobs After Scraping

```bash
# Get jobs from specific company
curl "http://localhost:8000/api/v1/jobs?company=Google"

# Get jobs in Sydney
curl "http://localhost:8000/api/v1/jobs?location=Sydney"
```

---

## Next Steps

### Phase 1: Authentication (Recommended for Production)
Add API key authentication to secure endpoints.

### Phase 2: Enhanced Agent Intelligence
- LLM-based job relevance scoring
- Automatic salary extraction
- Company sentiment analysis

### Phase 3: Multi-Source Scraping
- Add LinkedIn scraper
- Add Indeed scraper
- Unified job aggregation

### Phase 4: Real-Time Features
- WebSocket support for live updates
- Server-Sent Events for job streaming
- Real-time dashboard

---

## Support

For issues or questions:
1. Check API documentation: http://localhost:8000/api/docs
2. Review logs in `logs/` directory
3. Consult main README.md for scraper configuration

---

**Built with FastAPI | Production-Ready | n8n Compatible**
