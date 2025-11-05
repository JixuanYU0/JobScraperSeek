# Seek URL Structure Guide

## How the Scraper Accesses HR & Recruitment Jobs

The scraper **directly navigates to the correct classification URL** - it doesn't need to click anything because it uses Seek's structured URL format.

## Seek's URL Structure

### Classification-Based URLs

Seek uses **slug-based URLs** for job classifications:

```
Format: https://www.seek.com.au/{classification-slug}

Example:
https://www.seek.com.au/jobs-in-human-resources-recruitment
```

### How It Works

1. **Direct Navigation** (No Clicking Required)
   ```python
   # The scraper goes directly to:
   url = "https://www.seek.com.au/jobs-in-human-resources-recruitment"
   page.goto(url)
   ```

2. **This is equivalent to:**
   - Going to seek.com.au
   - Clicking "Browse Categories"
   - Clicking "Human Resources & Recruitment"

   **But faster and more reliable!**

### Why This Approach is Better

✅ **Faster**: No need to wait for category menus to load
✅ **More Reliable**: Doesn't depend on UI elements that might change
✅ **Consistent**: Always starts at the exact same place
✅ **Configurable**: Easy to change classification in config

## URL Examples

### Different Classifications

```bash
# HR & Recruitment
https://www.seek.com.au/jobs-in-human-resources-recruitment

# HR & Recruitment (last 3 days only)
https://www.seek.com.au/jobs-in-human-resources-recruitment?daterange=3

# Accounting
https://www.seek.com.au/jobs-in-accounting

# Information & Communication Technology
https://www.seek.com.au/jobs-in-information-communication-technology

# Marketing & Communications
https://www.seek.com.au/jobs-in-marketing-communications
```

### Date Range Parameter

The `daterange` parameter filters jobs by posting date:

```bash
# Last 24 hours
?daterange=1

# Last 3 days (default in our config)
?daterange=3

# Last 7 days
?daterange=7

# Last 14 days
?daterange=14

# Last 31 days
?daterange=31

# All jobs (no parameter)
(no daterange parameter)
```

### With Location Filters

```bash
# HR jobs in Sydney
https://www.seek.com.au/jobs-in-human-resources-recruitment/in-All-Sydney-NSW

# HR jobs in Melbourne
https://www.seek.com.au/jobs-in-human-resources-recruitment/in-All-Melbourne-VIC

# HR jobs in Brisbane
https://www.seek.com.au/jobs-in-human-resources-recruitment/in-All-Brisbane-QLD
```

### With Pagination

```bash
# Page 1 (default)
https://www.seek.com.au/jobs-in-human-resources-recruitment

# Page 2
https://www.seek.com.au/jobs-in-human-resources-recruitment?page=2

# Page 3
https://www.seek.com.au/jobs-in-human-resources-recruitment?page=3
```

## Configuration

The classification URL is configured in [config/config.yaml](config/config.yaml):

```yaml
scraper:
  base_url: "https://www.seek.com.au"
  classification: "Human Resources & Recruitment"
  classification_slug: "jobs-in-human-resources-recruitment"

  # Date range filter (in days)
  # 1 = Last 24 hours, 3 = Last 3 days, 7 = Last 7 days, etc.
  # Set to 0 or null to get all jobs (no date filter)
  date_range: 3
```

**This generates:** `https://www.seek.com.au/jobs-in-human-resources-recruitment?daterange=3`

### To Change Classification

1. Find the Seek URL for your desired classification
2. Extract the slug (part after `seek.com.au/`)
3. Update config:

```yaml
scraper:
  classification: "Accounting"
  classification_slug: "jobs-in-accounting"
```

### To Add Location Filter

Update the scraper code in [src/scraper/seek_scraper.py](src/scraper/seek_scraper.py):

```python
def _build_search_url(self) -> str:
    classification_slug = self.config.get("scraper.classification_slug")
    location = self.config.get("scraper.location", None)

    if location:
        return f"{self.base_url}/{classification_slug}/in-All-{location}"
    else:
        return f"{self.base_url}/{classification_slug}"
```

Then in config:
```yaml
scraper:
  location: "Sydney-NSW"  # Optional
```

## How the Scraper Works

### Step-by-Step Flow

```
1. Load config
   ↓
2. Build URL: https://www.seek.com.au/jobs-in-human-resources-recruitment
   ↓
3. Navigate directly to URL (page.goto())
   ↓
4. Wait for job cards to load
   ↓
5. Extract job data from current page
   ↓
6. Click "Next Page" button
   ↓
7. Repeat steps 5-6 until max_pages reached or no more pages
```

### Code Implementation

```python
# Build the classification URL
def _build_search_url(self) -> str:
    classification_slug = self.config.get(
        "scraper.classification_slug",
        "jobs-in-human-resources-recruitment"
    )
    return f"{self.base_url}/{classification_slug}"

# Navigate to it
search_url = self._build_search_url()
page.goto(search_url, wait_until="domcontentloaded")

# Start scraping
page_jobs = self._scrape_page(page)
```

## Verification

### Test the URL Works

```bash
# Run with non-headless mode to see the browser
python main.py --headless false
```

You should see:
1. Browser opens
2. Goes directly to: `https://www.seek.com.au/jobs-in-human-resources-recruitment`
3. Shows HR & Recruitment jobs immediately
4. No clicking or navigation needed!

### Check the Log

```bash
tail -f logs/scraper_$(date +%Y-%m-%d).log
```

Look for:
```
INFO - Navigating to: https://www.seek.com.au/jobs-in-human-resources-recruitment
INFO - Scraping page 1...
INFO - Found 30 jobs on page 1
```

## Troubleshooting

### Wrong Jobs Showing Up

**Symptom:** Jobs from different categories appear

**Cause:** Incorrect classification slug

**Solution:**
1. Visit Seek manually and find the correct category
2. Copy the URL slug
3. Update `classification_slug` in config

### No Jobs Found

**Symptom:** "No jobs found" or empty results

**Possible causes:**

1. **Seek changed their URL structure**
   - Check if the URL still works in a browser
   - Update the slug in config

2. **Page selectors changed**
   - Check [src/scraper/seek_scraper.py](src/scraper/seek_scraper.py)
   - Update selectors if Seek redesigned their site

3. **Network issues**
   - Check internet connection
   - Try increasing `request_timeout` in config

**Debug:**
```bash
python main.py --headless false
```

Watch the browser and see what page it loads.

### Page Doesn't Load

**Symptom:** Timeout errors

**Solutions:**

1. Increase timeout:
   ```yaml
   scraper:
     request_timeout: 60  # seconds
   ```

2. Add retry logic (already implemented):
   ```yaml
   scraper:
     retry_attempts: 5
     retry_delay: 10
   ```

## Advanced: Other Classification Slugs

To scrape other job categories, use these slugs:

| Category | Slug |
|----------|------|
| HR & Recruitment | `jobs-in-human-resources-recruitment` |
| Accounting | `jobs-in-accounting` |
| Marketing | `jobs-in-marketing-communications` |
| IT | `jobs-in-information-communication-technology` |
| Engineering | `jobs-in-engineering` |
| Sales | `jobs-in-sales` |
| Administration | `jobs-in-administration-office-support` |
| Healthcare | `jobs-in-healthcare-medical` |
| Education | `jobs-in-education-training` |

**Note:** You may need to adjust the excluded companies list for different categories.

## Future Enhancements

### Multi-Classification Support

Could be added by configuring multiple slugs:

```yaml
scraper:
  classifications:
    - slug: "jobs-in-human-resources-recruitment"
      name: "HR & Recruitment"
      excluded_companies: [list of HR agencies]

    - slug: "jobs-in-accounting"
      name: "Accounting"
      excluded_companies: [list of accounting recruiters]
```

### Dynamic URL Building

Add support for more URL parameters:

```python
def _build_search_url(self) -> str:
    params = {
        "classification": self.config.get("scraper.classification_slug"),
        "location": self.config.get("scraper.location"),
        "salaryrange": self.config.get("scraper.salary_range"),
        "worktype": self.config.get("scraper.work_type"),
        "daterange": self.config.get("scraper.date_range"),
    }
    # Build URL with query parameters
    return build_url_with_params(self.base_url, params)
```

## Summary

✅ **The scraper DOES ensure the correct classification is loaded**
✅ **It uses direct URL navigation (better than clicking)**
✅ **The URL is: `https://www.seek.com.au/jobs-in-human-resources-recruitment`**
✅ **Configurable via `classification_slug` in config.yaml**
✅ **No manual clicking or category selection needed**

The approach is **reliable, fast, and maintainable**! 🎉

---

**Last Updated:** 2025-10-10
**Current Classification:** Human Resources & Recruitment
**URL:** https://www.seek.com.au/jobs-in-human-resources-recruitment
