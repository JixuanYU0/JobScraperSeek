# Architecture Documentation

## System Overview

The Seek Job Scraper is a modular, production-ready system for automated job listing collection from Seek.com.au.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        main.py                               │
│                  (Entry Point & CLI)                         │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ├─── Config Loader ───────────┐
                  │    (YAML + env vars)         │
                  │                              │
                  ├─── Logger Setup              │
                  │    (File + Console)          │
                  │                              │
                  ├─── SeekScraper ──────────────┤
                  │    (Playwright)              │
                  │    │                         │
                  │    ├── Browser Launch        │
                  │    ├── Page Navigation       │
                  │    ├── Job Extraction        │
                  │    └── Pagination            │
                  │                              │
                  ├─── Deduplicator              │
                  │    │                         │
                  │    ├── Batch Dedup           │
                  │    └── Historical Dedup      │
                  │                              │
                  └─── Storage Layer ────────────┤
                       │                         │
                       ├── JSON Storage          │
                       ├── CSV Storage           │
                       ├── (Future) Airtable     │
                       └── (Future) PostgreSQL   │
```

## Component Details

### 1. Configuration System ([src/utils/config_loader.py](src/utils/config_loader.py))

**Responsibilities:**
- Load YAML configuration
- Merge with environment variables
- Provide typed access to settings
- Generate dynamic paths (with dates)

**Key Features:**
- Dot-notation access: `config.get("scraper.max_pages")`
- Environment variable injection: `${AIRTABLE_API_KEY}`
- Path resolution with timestamp formatting

### 2. Scraper Core ([src/scraper/seek_scraper.py](src/scraper/seek_scraper.py))

**Responsibilities:**
- Browser automation via Playwright
- Page navigation and pagination
- Job data extraction
- Error handling and retries

**Key Methods:**
- `scrape()`: Main entry point
- `_scrape_page()`: Extract jobs from current page
- `_extract_job_data()`: Parse individual job cards
- `_should_include_job()`: Apply filters
- `_goto_next_page()`: Handle pagination

**Selector Strategy:**
Seek uses data attributes for stability:
- `[data-search-sol-meta]`: Job card containers
- `[data-automation="jobCompany"]`: Company name
- `[data-automation="jobLocation"]`: Location
- `[data-automation="jobSalary"]`: Salary info

### 3. Data Models ([src/models/job.py](src/models/job.py))

**Job Class:**
```python
@dataclass
class Job:
    title: str
    company: str
    location: str
    classification: str
    subcategory: str
    job_url: str
    posted_date: Optional[str]
    salary: Optional[str]
    description: Optional[str]
    scraped_at: str
```

**Features:**
- Automatic timestamp generation
- URL-based hashing for deduplication
- Dict serialization/deserialization
- Job ID extraction from URL

### 4. Storage Layer

#### Base Storage ([src/storage/base_storage.py](src/storage/base_storage.py))
Abstract interface defining:
- `save(jobs)`: Persist jobs
- `load()`: Retrieve jobs
- `exists(job)`: Check for duplicates

#### JSON Storage ([src/storage/json_storage.py](src/storage/json_storage.py))
- Writes jobs to dated JSON files
- Maintains separate `seen_jobs.json` for dedup tracking
- Auto-cleans old entries based on retention policy

#### CSV Storage ([src/storage/csv_storage.py](src/storage/csv_storage.py))
- Tabular output for easy analysis
- Compatible with Excel/Google Sheets
- UTF-8 encoding for international characters

### 5. Deduplication ([src/utils/deduplicator.py](src/utils/deduplicator.py))

**Two-Phase Approach:**

1. **Batch Deduplication**
   - Removes duplicates within current scrape
   - Uses job URL as unique key
   - O(n) time complexity with set-based checking

2. **Historical Deduplication**
   - Compares against previously seen jobs
   - Tracks job URLs with timestamps
   - Auto-expires entries after N days

### 6. Logging ([src/utils/logger.py](src/utils/logger.py))

**Multi-Channel Logging:**
- Console output for real-time monitoring
- File output for audit trail
- Configurable log levels (DEBUG, INFO, WARNING, ERROR)
- Automatic log rotation by date

## Data Flow

```
1. Load Config
   ↓
2. Initialize Logger
   ↓
3. Create Scraper
   ↓
4. Launch Browser → Navigate to Seek
   ↓
5. For Each Page:
   ├─ Find job cards
   ├─ Extract job data
   ├─ Apply filters (exclude agency)
   └─ Collect jobs
   ↓
6. Deduplication:
   ├─ Remove batch duplicates
   └─ Filter seen jobs
   ↓
7. Storage:
   ├─ Save to JSON/CSV
   └─ Update seen_jobs.json
   ↓
8. Log Summary
```

## Configuration Schema

See [config/config.yaml](config/config.yaml) for full schema. Key sections:

- **scraper**: Browser settings, URLs, filters
- **storage**: Output formats and destinations
- **logging**: Verbosity and output channels
- **deduplication**: Retention and key field
- **scheduler**: Frequency settings (for reference)

## Extensibility Points

### Adding New Storage Backends

1. Create new class extending `BaseStorage`
2. Implement `save()`, `load()`, `exists()`
3. Add to [src/storage/__init__.py](src/storage/__init__.py)
4. Update [main.py](main.py) to use new backend

Example: Airtable Storage
```python
class AirtableStorage(BaseStorage):
    def __init__(self, api_key, base_id, table_name):
        self.table = Table(api_key, base_id, table_name)

    def save(self, jobs):
        for job in jobs:
            self.table.create(job.to_dict())
```

### Adding New Scrapers

Follow pattern in [src/scraper/seek_scraper.py](src/scraper/seek_scraper.py):

1. Extend for other job boards (Indeed, LinkedIn, etc.)
2. Implement same interface
3. Use polymorphism in main.py

### Adding Notifications

Extend [schedule_scraper.sh](schedule_scraper.sh):

```bash
# Send Slack notification
curl -X POST $SLACK_WEBHOOK_URL \
  -H 'Content-type: application/json' \
  --data "{\"text\":\"Scraped ${job_count} jobs\"}"
```

## Performance Considerations

### Current Performance

- **Throughput**: ~30 jobs/page, 2 seconds/page
- **Typical Run**: 5-10 pages, 1-2 minutes
- **Memory**: <100MB (no history stored in memory)

### Optimization Opportunities

1. **Parallel Page Scraping**
   - Use asyncio + async Playwright
   - Scrape multiple pages concurrently

2. **Incremental Updates**
   - Stop scraping when all jobs are seen
   - Track "last scraped" timestamp

3. **Caching**
   - Cache job descriptions for repeat URLs
   - Reduce redundant requests

## Error Handling

### Retry Logic

- **Network errors**: 3 retries with 5-second backoff
- **Timeout errors**: Configurable timeout (default 30s)
- **Page load failures**: Log and continue to next page

### Graceful Degradation

- Missing fields (salary, description) → Use None
- Failed page → Log error, continue to next
- No jobs found → Log warning, exit gracefully

## Security & Compliance

### Respectful Scraping

- 2-second delays between requests
- Realistic user agents
- Respects robots.txt
- Headless mode to reduce resource usage

### Data Privacy

- No personal data collection
- Job listings are public information
- Credentials stored in `.env` (gitignored)

### Terms of Service

⚠️ **Important**: Review Seek's Terms of Service. Consider:
- Using Seek's official API if available
- Rate limiting to avoid overload
- Not reselling scraped data

## Testing Strategy

### Manual Testing

```bash
# Test with limited pages
python main.py --config config/test_config.yaml

# Visual debugging
python main.py --headless false

# Test deduplication
python main.py --no-dedup  # First run
python main.py             # Second run (should show dups)
```

### Unit Testing (Future)

```python
# tests/test_scraper.py
def test_extract_job_data():
    scraper = SeekScraper(config, logger)
    job = scraper._extract_job_data(mock_card)
    assert job.title == "HR Manager"
    assert "Agency" not in job.subcategory

# tests/test_deduplicator.py
def test_remove_duplicates():
    jobs = [job1, job2, job1]  # job1 appears twice
    unique = deduplicator.remove_within_batch_duplicates(jobs)
    assert len(unique) == 2
```

## Monitoring & Observability

### Key Metrics to Track

1. **Success Rate**: % of successful runs
2. **Job Count**: New jobs per run
3. **Duplicate Rate**: % of duplicates found
4. **Run Duration**: Time to complete
5. **Error Rate**: Failed requests per run

### Log Analysis

```bash
# Count successful runs
grep "Scraping completed successfully" logs/*.log | wc -l

# Average job count
grep "Total jobs scraped:" logs/*.log | awk '{sum+=$NF} END {print sum/NR}'

# Find errors
grep "ERROR" logs/*.log
```

## Deployment

### Local Development

```bash
python main.py --headless false
```

### Production

```bash
# Cron job (daily at 9 AM)
0 9 * * * cd /path/to/JobScraperSeek && ./schedule_scraper.sh
```

### Docker (Future)

```dockerfile
FROM python:3.11
RUN playwright install --with-deps chromium
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
```

## Troubleshooting Guide

### "No jobs found"

- Check if Seek URL structure changed
- Verify classification ID (6251 for HR)
- Run with `--headless false` to see page

### "Playwright not installed"

```bash
source venv/bin/activate
playwright install chromium
```

### "Config file not found"

- Ensure `config/config.yaml` exists
- Check file permissions
- Use `--config` to specify path

### High duplicate rate

- Increase `max_pages` to find more new jobs
- Adjust `retention_days` in config
- Check if jobs are being updated on Seek

## Future Roadmap

### Phase 1: Current (✅ Complete)
- Basic scraping with Playwright
- JSON/CSV storage
- Deduplication
- Scheduling

### Phase 2: Enhancement
- [ ] Airtable integration
- [ ] Email/Slack notifications
- [ ] Improved error recovery
- [ ] Job description detail scraping

### Phase 3: Scale
- [ ] PostgreSQL/Supabase backend
- [ ] Dashboard for analytics
- [ ] API endpoint for job data
- [ ] Multi-classification support

### Phase 4: Intelligence
- [ ] Job matching algorithm
- [ ] Trend analysis
- [ ] Salary benchmarking
- [ ] Lead scoring

## Contributing

For internal LiquidHR team:

1. Create feature branch
2. Make changes
3. Test thoroughly
4. Submit for review
5. Deploy to production

---

**Last Updated**: 2025-10-09
**Maintainer**: LiquidHR Development Team
