# Job Filtering Guide

## Overview

The scraper uses **two filtering mechanisms** to exclude recruitment agency jobs:

1. **Subcategory Filtering** - Excludes jobs in specific subcategories
2. **Company Filtering** - Excludes jobs from known recruitment agencies

## How Filtering Works

### Subcategory Filtering

Jobs are filtered out if their subcategory contains any of the excluded terms.

**Example:**
```yaml
excluded_subcategories:
  - "Recruitment - Agency"
```

This will exclude jobs categorized as "Recruitment - Agency" on Seek.

### Company Filtering (Primary Method)

Jobs are filtered out if the company name contains any of the excluded company names (case-insensitive, partial match).

**Example:**
```yaml
excluded_companies:
  - "Hays"
  - "Michael Page"
  - "Robert Walters"
```

This will exclude jobs from:
- "Hays Recruitment"
- "Hays Australia"
- "Michael Page International"
- "Robert Walters Group"
- etc.

**How it works:**
- Uses **case-insensitive** matching
- Uses **partial string matching** (substring search)
- If "Hays" is in the excluded list, it will match:
  - "Hays"
  - "Hays Recruitment"
  - "Hays Australia Limited"
  - Any company with "Hays" in the name

## Current Excluded Companies (59 agencies)

The system currently excludes jobs from these recruitment agencies:

### Major Agencies
- Hays
- Hudson
- Michael Page
- Robert Walters
- Frazer Jones
- The Next Step
- Tandem Partners
- HR Partners / Randstad
- Peoplecorp
- Beaumont People
- Davidson
- Six Degrees Executive
- Sharp & Carter
- u&u Recruitment Partners
- Slade Group
- Bluefin Resources
- FutureYou
- people2people
- Derwent
- SHK / SHK Asia Pacific

### Executive Search Firms
- Korn Ferry
- Heidrick & Struggles
- Spencer Stuart
- Egon Zehnder
- NGS Global
- Watermark Search International
- Fisher Leadership
- Pacific Search Partners

### Staffing & Temp Agencies
- DFP Recruitment
- Ignite / Candle
- Chandler Macleod
- Adecco
- ManpowerGroup
- Programmed
- Drake International
- Kelly Services

### Specialist Recruiters
- McArthur
- Public Sector People
- Rowben Consulting
- SustainAbility Consulting
- Talent International
- Paxus
- Salt Recruitment
- Morgan Consulting
- Kaizen Recruitment
- BWS Recruitment
- u&XL People
- TQSolutions
- etonHR
- Capability HR
- Levyl
- Robert Half

## Adding New Companies to Exclude

Edit [config/config.yaml](config/config.yaml):

```yaml
scraper:
  excluded_companies:
    - "Hays"
    - "Michael Page"
    # Add your new agency here
    - "New Agency Name"
```

**Tips:**
1. Use the shortest unique part of the company name
2. If multiple variations exist (e.g., "HR Partners" is part of "Randstad"), use the most specific name
3. Test after adding to ensure it's working

## Removing Companies from Exclusion

Simply delete or comment out the company name in [config/config.yaml](config/config.yaml):

```yaml
excluded_companies:
  - "Hays"
  # - "Michael Page"  # Commented out - will NOT be filtered
```

## Viewing Filter Results

### See what's being filtered (DEBUG mode)

Edit [config/config.yaml](config/config.yaml):

```yaml
logging:
  level: "DEBUG"  # Change from INFO to DEBUG
```

Run the scraper:

```bash
python main.py
```

You'll see messages like:
```
DEBUG - Excluded by company 'Hays': Senior HR Manager at Hays Recruitment
DEBUG - Excluded by company 'Robert Walters': HR Business Partner at Robert Walters
```

### Count excluded companies

```bash
# In Python
import yaml
with open('config/config.yaml') as f:
    config = yaml.safe_load(f)
    print(f"Excluding {len(config['scraper']['excluded_companies'])} companies")
```

Or check the log output:
```
INFO - Excluding 59 recruitment agencies
```

## Testing Filters

### Test with a small sample

1. Edit [config/config.yaml](config/config.yaml):
   ```yaml
   scraper:
     max_pages: 2  # Only scrape 2 pages
   ```

2. Run with visible browser:
   ```bash
   python main.py --headless false
   ```

3. Check the output:
   ```bash
   jq '.[].company' data/jobs_*.json | sort | uniq
   ```

4. Verify no recruitment agencies appear

### Test specific company

```bash
# Check if any Hays jobs got through
jq '.[] | select(.company | contains("Hays"))' data/jobs_*.json

# Should return empty if filter is working
```

## Filter Statistics

After a run, you can analyze filtering effectiveness:

```bash
# Show all companies in results
jq -r '.[].company' data/jobs_*.json | sort | uniq -c | sort -nr

# Count unique companies
jq -r '.[].company' data/jobs_*.json | sort -u | wc -l

# Check for any agencies that might have slipped through
jq -r '.[].company' data/jobs_*.json | grep -i "recruitment\|search\|staffing"
```

## Common Issues

### Agency jobs still appearing

**Possible causes:**
1. Company name variation not in exclusion list
2. Typo in exclusion list
3. Company uses a different trading name on Seek

**Solution:**
1. Check the actual company name in the scraped data:
   ```bash
   jq '.[].company' data/jobs_*.json
   ```
2. Add the exact variation to `excluded_companies`
3. Re-run the scraper

### Too many jobs being filtered

**Symptom:** Very few or no jobs in output

**Check:**
1. Review your `excluded_companies` list for overly generic terms
2. Example: Don't use "HR" as it will match "HR Department" in legitimate companies

**Solution:**
1. Use more specific company names
2. Check logs for what's being filtered:
   ```bash
   grep "Excluded by company" logs/scraper_*.log | head -20
   ```

### False positives

**Example:** "Hays" might match "Hayes Valley Company" (different company)

**Solution:**
1. If this happens frequently, you may need to use exact matching instead
2. Contact the dev team to add an exact-match option
3. For now, use more specific names like "Hays Recruitment" instead of just "Hays"

## Advanced: Custom Filtering Logic

If you need more complex filtering (e.g., regex patterns, exact matching), you can modify [src/scraper/seek_scraper.py](src/scraper/seek_scraper.py):

```python
def _should_include_job(self, job: Job) -> bool:
    """Custom filtering logic."""

    # Exact match example
    if job.company.lower() in [c.lower() for c in self.excluded_companies]:
        return False

    # Regex example
    import re
    for pattern in self.excluded_patterns:
        if re.search(pattern, job.company, re.IGNORECASE):
            return False

    return True
```

## Performance Impact

**Filtering performance:**
- Subcategory filtering: ~0.001ms per job
- Company filtering: ~0.01ms per job
- Total overhead: Negligible (<1% of scraping time)

**No performance concerns** - filtering is very fast compared to network requests.

## Best Practices

1. **Keep the list updated**: Add new agencies as you discover them
2. **Use short names**: "Hays" instead of "Hays Recruitment Limited"
3. **Test regularly**: Run with DEBUG logging to verify filters work
4. **Document changes**: Comment why you added/removed an agency
5. **Review results**: Periodically check output to ensure quality

## Integration with Deduplication

Filtering happens **before** deduplication:

```
1. Scrape page
2. Extract job data
3. Apply filters (subcategory + company) ← You are here
4. Add to results
5. Deduplicate
6. Save to storage
```

This means filtered jobs are never stored or counted in statistics.

## Monitoring Filter Effectiveness

### Daily check

```bash
# After each run
grep "Excluding" logs/scraper_$(date +%Y-%m-%d).log
# Output: "Excluding 59 recruitment agencies"

# Check for any agency names in results
jq -r '.[].company' data/jobs_$(date +%Y-%m-%d).json | \
  grep -iE "recruitment|search|staffing|agency"
```

### Weekly review

```bash
# Get unique companies from last 7 days
jq -r '.[].company' data/jobs_*.json | sort -u > companies.txt

# Review for any new agencies to add
cat companies.txt
```

---

**Last Updated:** 2025-10-10
**Filter Count:** 59 recruitment agencies
**Maintainer:** LiquidHR Team
