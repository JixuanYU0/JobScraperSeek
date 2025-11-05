# Subclassification Filtering Guide

## Overview

The scraper now supports **TWO LEVELS of filtering** to exclude recruitment agency jobs:

1. **Source-Level Filtering** (Recommended) - Filter at Seek's server via URL parameters
2. **Client-Level Filtering** - Filter after scraping (backup/safety net)

## Source-Level Filtering (Most Efficient)

### How It Works

Instead of scraping ALL HR jobs and then filtering out unwanted ones, we tell Seek to **only return specific subcategories** in the URL:

```
https://www.seek.com.au/jobs-in-human-resources-recruitment?daterange=3&subclassification=6323%2C6322%2C6321%2C6318%2C6319%2C6320%2C6325%2C6326%2C6327%2C6328
```

**Benefits:**
✅ **Faster** - Fewer pages to scrape
✅ **More efficient** - Less bandwidth and processing
✅ **More accurate** - Gets exactly what you want from Seek
✅ **Reduces load** - Respectful to Seek's servers

### Subcategory IDs

Here are the HR & Recruitment subcategories on Seek:

| ID | Subcategory | Include? |
|----|-------------|----------|
| 6318 | Consulting & Generalist HR | ✅ Yes |
| 6319 | Health, Safety & Environment | ✅ Yes |
| 6320 | Industrial & Employee Relations | ✅ Yes |
| 6321 | Management - Internal | ✅ Yes |
| 6322 | Organisational Development | ✅ Yes |
| 6323 | Recruitment - Internal | ✅ Yes |
| **6324** | **Recruitment - Agency** | ❌ **NO** |
| 6325 | Remuneration & Benefits | ✅ Yes |
| 6326 | Training & Development | ✅ Yes |
| 6327 | Work Health & Safety | ✅ Yes |
| 6328 | Other | ✅ Yes |

### Configuration

In [config/config.yaml](config/config.yaml):

```yaml
scraper:
  # Include all subcategories EXCEPT Recruitment - Agency (6324)
  subclassification_ids: "6323,6322,6321,6318,6319,6320,6325,6326,6327,6328"
```

**Note:** The IDs are comma-separated. 6324 (Recruitment - Agency) is intentionally excluded.

## Client-Level Filtering (Backup)

Even with source-level filtering, we keep the backup filters:

```yaml
scraper:
  # Backup subcategory filter
  excluded_subcategories:
    - "Recruitment - Agency"

  # Company name filter (59 agencies)
  excluded_companies:
    - "Hays"
    - "Michael Page"
    # ... and 57 more
```

**Why keep both?**
- **Defense in depth** - Double check nothing slips through
- **Handles edge cases** - In case Seek's categorization is wrong
- **Company filtering** - Catches agency jobs miscategorized as internal

## Three-Layer Filtering Strategy

```
Layer 1: Source (Subclassification IDs)
         ↓
    [Only correct subcategories scraped]
         ↓
Layer 2: Subcategory Text Matching
         ↓
    [Filter "Recruitment - Agency" by name]
         ↓
Layer 3: Company Name Matching
         ↓
    [Filter 59 known agency companies]
         ↓
    FINAL RESULTS: Pure HR jobs, no agencies
```

## URL Structure Explained

### Before (Inefficient)

```
https://www.seek.com.au/jobs-in-human-resources-recruitment?daterange=3

→ Returns ALL HR jobs (including agency)
→ We filter out agency jobs after scraping
→ Wastes bandwidth and time
```

### After (Efficient)

```
https://www.seek.com.au/jobs-in-human-resources-recruitment?daterange=3&subclassification=6323%2C6322%2C6321%2C6318%2C6319%2C6320%2C6325%2C6326%2C6327%2C6328

→ Returns ONLY non-agency HR jobs
→ No agency jobs to filter
→ Faster and more efficient
```

**Note:** `%2C` is URL encoding for comma (`,`)

## How to Update Subcategories

### Adding a Subcategory

If you want to include a currently excluded subcategory:

```yaml
# Add the ID to the list
subclassification_ids: "6323,6322,6321,6318,6319,6320,6325,6326,6327,6328,6324"
#                                                                            ^^^^
#                                                          Added 6324 (Agency)
```

### Removing a Subcategory

If you want to exclude more subcategories:

```yaml
# Remove IDs from the list
# Example: Exclude "Other" (6328)
subclassification_ids: "6323,6322,6321,6318,6319,6320,6325,6326,6327"
#                                                                ^^^^ 6328 removed
```

### Disable Subclassification Filtering

To scrape ALL HR subcategories and rely on post-scrape filtering:

```yaml
# Comment out or remove the line
# subclassification_ids: "6323,6322,6321,6318,6319,6320,6325,6326,6327,6328"

# Or set to empty
subclassification_ids: ""
```

## Verification

### Check the URL Being Used

Run with debug logging:

```bash
python main.py --headless false
```

Watch the browser navigate. You should see:
```
https://www.seek.com.au/jobs-in-human-resources-recruitment?daterange=3&subclassification=6323%2C6322%2C6321%2C6318%2C6319%2C6320%2C6325%2C6326%2C6327%2C6328
```

### Check the Logs

```bash
tail -f logs/scraper_*.log
```

Look for:
```
INFO - Using subclassification filter: 10 subcategories (excluding Recruitment - Agency at source)
INFO - Navigating to: https://www.seek.com.au/jobs-in-human-resources-recruitment?daterange=3&subclassification=...
```

### Verify No Agency Jobs

```bash
# Check scraped results
jq -r '.[].subcategory' data/jobs_*.json | sort -u

# Should NOT see:
# - "Recruitment - Agency"

# Should see:
# - "Recruitment - Internal"
# - "Consulting & Generalist HR"
# - "Management - Internal"
# - etc.
```

## Performance Comparison

### Without Subclassification Filter

```
Total jobs on Seek: 500
Agency jobs: 300 (60%)
Non-agency jobs: 200 (40%)

Pages scraped: 17 (500 jobs ÷ 30 per page)
Jobs filtered out: 300
Jobs kept: 200
Time: ~2 minutes
```

### With Subclassification Filter ✅

```
Total jobs on Seek: 200 (only non-agency returned)
Agency jobs: 0 (filtered at source)
Non-agency jobs: 200 (100%)

Pages scraped: 7 (200 jobs ÷ 30 per page)
Jobs filtered out: 0
Jobs kept: 200
Time: ~50 seconds
```

**Result: 60% faster, same output!**

## Troubleshooting

### Too Few Results

**Symptom:** Very few jobs returned

**Possible cause:** Subclassification IDs are wrong or too restrictive

**Solution:**
1. Disable subclassification filter temporarily:
   ```yaml
   subclassification_ids: ""
   ```
2. Run scraper and check subcategories:
   ```bash
   jq -r '.[].subcategory' data/jobs_*.json | sort -u
   ```
3. Verify which subcategories you want
4. Re-enable with correct IDs

### Agency Jobs Still Appearing

**Symptom:** Some agency jobs still in results

**Possible causes:**
1. Company is miscategorized on Seek
2. Job posted under wrong subcategory
3. New agency not in excluded list

**Solution:**
- Layer 2 & 3 filtering should catch these
- Add company to `excluded_companies` if needed
- Check if subcategory text matches excluded list

### URL Too Long Error

**Symptom:** URL encoding issues

**Solution:**
- The scraper properly URL-encodes the IDs
- If issues persist, reduce number of subcategories
- Or split into multiple runs

## Finding Subcategory IDs

If Seek changes their IDs or you need IDs for other classifications:

### Method 1: Manual Selection on Seek

1. Go to https://www.seek.com.au/jobs-in-human-resources-recruitment
2. Check the subcategory checkboxes you want
3. Look at the URL:
   ```
   ?subclassification=6323%2C6322%2C6321
   ```
4. Decode `%2C` → `,`
5. Copy the IDs: `6323,6322,6321`

### Method 2: Browser Developer Tools

1. Open Seek in browser
2. Press F12 (Developer Tools)
3. Go to Network tab
4. Click subcategory checkboxes
5. Look at the API request
6. Find `subclassification` parameter

## Advanced Configuration

### Combine with Location Filter

You could extend the URL builder to add location:

```python
# In _build_search_url()
location = self.config.get("scraper.location")
if location:
    params.append(f"where={quote(location)}")

# Result:
# ?daterange=3&subclassification=6323,6322&where=Sydney%20NSW
```

### Combine with Salary Filter

```python
salary_min = self.config.get("scraper.salary_min")
if salary_min:
    params.append(f"salaryrange={salary_min}-999999")
```

## Best Practices

1. ✅ **Always use subclassification filtering** - It's more efficient
2. ✅ **Keep backup filters** - Defense in depth
3. ✅ **Verify IDs periodically** - Seek may change them
4. ✅ **Monitor results** - Check for agency jobs slipping through
5. ✅ **Log the URL** - Easier to debug issues

## Summary

**Current Setup:**
- ✅ **Source filtering**: 10 subcategories (excluding 6324)
- ✅ **Subcategory text filter**: "Recruitment - Agency"
- ✅ **Company filter**: 59 recruitment agencies
- ✅ **Result**: Maximum efficiency, minimum agency jobs

This **three-layer approach** ensures you get exactly what you need with minimal wasted effort! 🎯

---

**Last Updated:** 2025-10-10
**Subcategories Included:** 10 (6318, 6319, 6320, 6321, 6322, 6323, 6325, 6326, 6327, 6328)
**Subcategories Excluded:** 1 (6324 - Recruitment - Agency)
