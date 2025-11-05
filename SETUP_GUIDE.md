# Quick Setup Guide

## Step 1: Installation

```bash
# Clone or navigate to the project
cd JobScraperSeek

# Run setup script
./setup.sh
```

## Step 2: Configuration (Optional)

Edit `config/config.yaml` to customize:
- Excluded subcategories
- Max pages to scrape
- Output formats
- Logging level

## Step 3: First Run

```bash
# Activate virtual environment
source venv/bin/activate

# Run the scraper
python main.py
```

You should see output like:
```
============================================================
Seek Job Scraper - Starting
============================================================
INFO - Starting Seek scraper...
INFO - Navigating to: https://www.seek.com.au/jobs?classification=6251
INFO - Scraping page 1...
INFO - Found 30 jobs on page 1
...
INFO - Total jobs scraped: 87
============================================================
```

## Step 4: Check Output

```bash
# View scraped jobs
cat data/jobs_$(date +%Y-%m-%d).json

# Or in a nicer format
python -m json.tool data/jobs_$(date +%Y-%m-%d).json | less
```

## Step 5: Schedule Daily Runs

```bash
# Open crontab editor
crontab -e

# Add this line (runs daily at 9 AM)
0 9 * * * cd /Users/yuhuaisheng/Desktop/LiquidHR/Seek_Scraper/JobScraperSeek && ./schedule_scraper.sh

# Save and exit
```

## Testing

### Test Run (5 pages max)

Edit `config/config.yaml`:
```yaml
scraper:
  max_pages: 5  # Limit to 5 pages for testing
  headless: false  # See the browser
```

Then run:
```bash
python main.py
```

### View Logs

```bash
# View latest log
tail -f logs/scraper_$(date +%Y-%m-%d).log
```

## Common Commands

```bash
# Run with different options
python main.py --output-format both  # Save as JSON and CSV
python main.py --no-dedup            # Disable deduplication
python main.py --headless false      # See browser in action

# Check what jobs were scraped today
jq '.[].title' data/jobs_$(date +%Y-%m-%d).json

# Count jobs
jq 'length' data/jobs_$(date +%Y-%m-%d).json

# Filter by company
jq '.[] | select(.company | contains("Google"))' data/jobs_$(date +%Y-%m-%d).json
```

## Troubleshooting

### "Playwright not installed"
```bash
source venv/bin/activate
playwright install chromium
```

### "Config file not found"
```bash
# Check if config exists
ls -la config/config.yaml
```

### "Permission denied"
```bash
chmod +x setup.sh schedule_scraper.sh
```

## Next Steps

1. **Integrate with Airtable**:
   - Update `.env` with Airtable credentials
   - Modify storage backend in config

2. **Set up notifications**:
   - Add Slack webhook to `.env`
   - Uncomment notification in `schedule_scraper.sh`

3. **Monitor performance**:
   - Check logs daily
   - Review duplicate rates
   - Adjust `max_pages` if needed

## Need Help?

Check the full [README.md](README.md) for detailed documentation.
