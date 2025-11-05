# Seek Job Scraper - HR & Recruitment

Automated scraping tool that collects Human Resources & Recruitment job listings from seek.com.au, **excluding recruitment agencies and their job postings**.

## 🎯 Features

- ✅ Scrapes HR & Recruitment jobs from Seek
- ✅ **Excludes 59 recruitment agencies** (Hays, Michael Page, Robert Walters, etc.)
- ✅ Excludes "Recruitment - Agency" subcategory
- ✅ Extracts detailed job metadata (title, company, location, salary, description, etc.)
- ✅ De-duplicates listings across runs
- ✅ Configurable scheduling (daily or custom intervals)
- ✅ Multiple output formats (JSON, CSV)
- ✅ Comprehensive logging
- ✅ Modular and extensible architecture

## 📦 Installation

### Prerequisites

- Python 3.8+
- pip

### Quick Setup

```bash
# Run the setup script
./setup.sh

# Or manually:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

## 🚀 Usage

### Basic Usage

```bash
# Activate virtual environment
source venv/bin/activate

# Run the scraper
python main.py
```

### Command Line Options

```bash
# Use custom config file
python main.py --config path/to/config.yaml

# Disable deduplication
python main.py --no-dedup

# Save as both JSON and CSV
python main.py --output-format both

# Run in non-headless mode (see browser)
python main.py --headless false
```

## ⚙️ Configuration

Edit [config/config.yaml](config/config.yaml) to customize:

```yaml
scraper:
  base_url: "https://www.seek.com.au"
  classification: "Human Resources & Recruitment"

  # Filter by subcategory
  excluded_subcategories:
    - "Recruitment - Agency"

  # Filter by company (59 agencies pre-configured)
  excluded_companies:
    - "Hays"
    - "Michael Page"
    - "Robert Walters"
    # ... and 56 more

  max_pages: 20
  headless: true

storage:
  type: "json"
  output_dir: "data"

logging:
  level: "INFO"
  console: true

deduplication:
  retention_days: 30
```

**See [FILTERING_GUIDE.md](FILTERING_GUIDE.md) for details on managing excluded agencies.**

## 📅 Scheduling

### Using Cron (macOS/Linux)

```bash
# Edit crontab
crontab -e

# Add this line to run daily at 9 AM
0 9 * * * cd /path/to/JobScraperSeek && ./schedule_scraper.sh

# Or hourly
0 * * * * cd /path/to/JobScraperSeek && ./schedule_scraper.sh
```

### Manual Scheduling

```bash
./schedule_scraper.sh
```

## 📊 Output Schema

### JSON Format
```json
{
  "title": "HR Business Partner",
  "company": "XYZ Pty Ltd",
  "location": "Sydney NSW",
  "salary": "$100,000 - $120,000",
  "classification": "Human Resources & Recruitment",
  "subcategory": "HR - Generalist",
  "posted_date": "2025-10-09",
  "job_url": "https://www.seek.com.au/job/12345678",
  "description": "...",
  "scraped_at": "2025-10-09T09:00:00"
}
```

## 📁 Project Structure

```
JobScraperSeek/
├── config/
│   └── config.yaml           # Configuration file
├── data/                     # Output data directory
│   ├── jobs_2025-10-09.json
│   └── seen_jobs.json        # Deduplication tracking
├── logs/                     # Log files
│   └── scraper_2025-10-09.log
├── src/
│   ├── models/               # Data models
│   │   └── job.py
│   ├── scraper/              # Scraping logic
│   │   └── seek_scraper.py
│   ├── storage/              # Storage backends
│   │   ├── json_storage.py
│   │   └── csv_storage.py
│   └── utils/                # Utilities
│       ├── config_loader.py
│       ├── logger.py
│       └── deduplicator.py
├── main.py                   # Main entry point
├── schedule_scraper.sh       # Scheduler script
├── setup.sh                  # Setup script
└── requirements.txt          # Dependencies
```

## 🔍 How It Works

1. **Configuration Loading**: Loads settings from [config/config.yaml](config/config.yaml)
2. **Browser Launch**: Uses Playwright to launch a Chromium browser
3. **URL Building**: Creates Seek URL with filters:
   - Classification: `jobs-in-human-resources-recruitment`
   - Date range: `daterange=3` (last 3 days)
   - Subcategories: `subclassification=6323,6322,...` (excludes agency at source)
4. **Navigation**: Direct navigation to filtered URL - no clicking needed!
5. **Scraping**: Extracts job data from search result pages
6. **Three-Layer Filtering**:
   - Layer 1: Subclassification IDs (filters at Seek's server)
   - Layer 2: Subcategory text matching ("Recruitment - Agency")
   - Layer 3: Company name matching (59 recruitment agencies)
7. **Deduplication**: Checks against previously seen jobs
8. **Storage**: Saves to JSON/CSV with timestamp
9. **Logging**: Records all activities to log file

**Efficiency:** Source-level filtering means ~60% fewer pages to scrape! See [SUBCLASSIFICATION_GUIDE.md](SUBCLASSIFICATION_GUIDE.md) for details.

## 🛡️ Best Practices

### Respectful Scraping

- Default 2-second delay between pages
- Respects Seek's robots.txt
- Uses realistic user agents
- Configurable retry logic

### Rate Limiting

To avoid overwhelming Seek's servers:
- Run once daily (recommended)
- Use headless mode in production
- Monitor logs for errors

## 🔧 Troubleshooting

### Browser Installation Issues

```bash
# Reinstall Playwright browsers
playwright install chromium --force
```

### Permission Denied

```bash
chmod +x setup.sh
chmod +x schedule_scraper.sh
```

### Module Not Found

```bash
# Ensure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

## 📈 Success Metrics

| Metric | Target |
|--------|--------|
| HR job coverage (no agency) | ≥95% accuracy |
| Duplicate rate | <5% |
| Error rate per run | <2% |
| Run frequency | 1x daily minimum |

## 🚧 Future Enhancements

- [ ] Airtable integration
- [ ] PostgreSQL/Supabase storage
- [ ] Email/Slack notifications
- [ ] Dashboard for analytics
- [ ] API endpoint for job data
- [ ] Multi-classification support
- [ ] Advanced filtering rules

## 📝 License

This tool is for internal use at LiquidHR. Please ensure compliance with Seek's Terms of Service.

## 🤝 Contributing

For questions or improvements, contact the LiquidHR development team.

---

**Built with ❤️ by LiquidHR**
