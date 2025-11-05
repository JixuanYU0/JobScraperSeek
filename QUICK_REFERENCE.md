# Quick Reference Card

## 🚀 Getting Started (First Time)

```bash
./setup.sh
source venv/bin/activate
python main.py
```

## 📋 Common Commands

### Run Scraper

```bash
# Basic run
python main.py

# Save as both JSON and CSV
python main.py --output-format both

# See browser in action (debugging)
python main.py --headless false

# Disable deduplication (scrape everything)
python main.py --no-dedup
```

### Check Results

```bash
# View today's jobs (pretty print)
python -m json.tool data/jobs_$(date +%Y-%m-%d).json | less

# Count jobs scraped today
jq 'length' data/jobs_$(date +%Y-%m-%d).json

# List job titles
jq '.[].title' data/jobs_$(date +%Y-%m-%d).json

# Find jobs by company
jq '.[] | select(.company | contains("Seek"))' data/jobs_$(date +%Y-%m-%d).json

# Export specific fields to CSV
jq -r '.[] | [.title, .company, .location, .salary] | @csv' data/jobs_*.json > summary.csv
```

### Logs

```bash
# Tail latest log
tail -f logs/scraper_$(date +%Y-%m-%d).log

# View all logs
less logs/scraper_*.log

# Count successful runs
grep "completed successfully" logs/*.log | wc -l

# Find errors
grep "ERROR" logs/*.log
```

## ⚙️ Configuration

### Quick Settings ([config/config.yaml](config/config.yaml))

```yaml
# Scrape fewer pages (faster)
scraper:
  max_pages: 5

# See browser
scraper:
  headless: false

# More verbose logging (see what's being filtered)
logging:
  level: "DEBUG"

# Keep dedup history longer
deduplication:
  retention_days: 60

# Add/remove excluded recruitment agencies
scraper:
  excluded_companies:
    - "Hays"
    - "New Agency Name"  # Add here

# Change date range filter
scraper:
  date_range: 7   # Last 7 days
  date_range: 1   # Last 24 hours
  date_range: 0   # All jobs (no date filter)
```

## 📅 Scheduling

### Setup Cron (One Time)

```bash
crontab -e

# Add this line (daily at 9 AM):
0 9 * * * cd /Users/yuhuaisheng/Desktop/LiquidHR/Seek_Scraper/JobScraperSeek && ./schedule_scraper.sh

# Or hourly:
0 * * * * cd /Users/yuhuaisheng/Desktop/LiquidHR/Seek_Scraper/JobScraperSeek && ./schedule_scraper.sh
```

### Check Cron Status

```bash
# List cron jobs
crontab -l

# Remove cron job
crontab -r
```

### Manual Schedule Run

```bash
./schedule_scraper.sh
```

## 🔍 Data Analysis

### Python

```python
import json

# Load jobs
with open('data/jobs_2025-10-09.json') as f:
    jobs = json.load(f)

# Count by subcategory
from collections import Counter
subcats = Counter(j['subcategory'] for j in jobs)
print(subcats)

# Find high-paying jobs
high_paying = [j for j in jobs if j.get('salary') and '$100' in j['salary']]
```

### Command Line

```bash
# Count jobs by location
jq -r '.[].location' data/jobs_*.json | sort | uniq -c | sort -nr

# Find Sydney jobs
jq '.[] | select(.location | contains("Sydney"))' data/jobs_*.json

# Check for any recruitment agencies (should be empty)
jq -r '.[].company' data/jobs_*.json | grep -i "hays\|michael page\|recruitment"

# List all companies
jq -r '.[].company' data/jobs_*.json | sort -u

# Average jobs per day
ls data/jobs_*.json | wc -l  # days
jq 'length' data/jobs_*.json | awk '{s+=$1} END {print s/NR}'
```

## 🐛 Troubleshooting

### Reset Everything

```bash
# Clear data and logs
rm data/*.json logs/*.log

# Re-run setup
./setup.sh
```

### Test Installation

```bash
source venv/bin/activate
python -c "import playwright; print('✓ Playwright installed')"
python -c "import yaml; print('✓ PyYAML installed')"
```

### Playwright Issues

```bash
# Reinstall browsers
playwright install chromium --force

# Check browser path
playwright install --help
```

### View Browser

```bash
# See what the scraper sees
python main.py --headless false
```

## 📊 Success Metrics

Check these regularly:

```bash
# Jobs scraped per run
jq 'length' data/jobs_*.json

# Unique companies
jq -r '.[].company' data/jobs_*.json | sort -u | wc -l

# Duplicate rate (should be <5%)
# Run twice and compare counts

# Error rate (should be <2%)
grep ERROR logs/*.log | wc -l
```

## 🔗 File Locations

| What | Where |
|------|-------|
| Config | `config/config.yaml` |
| Main script | `main.py` |
| Output data | `data/jobs_YYYY-MM-DD.json` |
| Dedup tracking | `data/seen_jobs.json` |
| Logs | `logs/scraper_YYYY-MM-DD.log` |
| Virtual env | `venv/` |
| Source code | `src/` |

## 💡 Tips

1. **Always activate venv first**: `source venv/bin/activate`
2. **Test with 5 pages first**: Set `max_pages: 5` in config
3. **Monitor logs during runs**: `tail -f logs/scraper_*.log`
4. **Back up data regularly**: `cp -r data/ data_backup/`
5. **Review config before production**: Check `excluded_subcategories`

## 🆘 Quick Help

```bash
# Get help
python main.py --help

# Check version
python main.py --version 2>/dev/null || python --version

# Test config syntax
python -c "import yaml; yaml.safe_load(open('config/config.yaml'))"

# Validate JSON output
jq empty data/jobs_*.json && echo "✓ Valid JSON"
```

## 📞 Support

For issues or questions:
1. Check [README.md](README.md) for detailed docs
2. Review [ARCHITECTURE.md](ARCHITECTURE.md) for technical details
3. Check [SETUP_GUIDE.md](SETUP_GUIDE.md) for installation help
4. Contact LiquidHR dev team

---

**Pro Tip**: Bookmark this file for quick reference during development!
