# Data Storage & Backup Guide

## 📁 Where All Data is Stored

### **Primary Data Location**

All job data is stored in the `data/` directory:

```
JobScraperSeek/
├── data/
│   ├── jobs_2025-11-08.json      ← Main job database (397 jobs, 249KB)
│   └── seen_jobs.json             ← Deduplication tracker (149KB)
```

### **1. Main Job Database**

**File**: `data/jobs_{date}.json`
- **Current file**: `data/jobs_2025-11-08.json`
- **Contains**: All 397 scraped jobs with complete details
- **Format**: JSON array with job objects
- **Size**: ~249KB (will grow as more jobs are added)
- **Updated**: Every time the scraper runs

**Example job structure**:
```json
{
  "title": "People & Culture Business Officer",
  "company": "Van Schaik's Bio Gro",
  "location": "Dandenong South",
  "salary": null,
  "job_type": null,
  "classification": "Human Resources & Recruitment",
  "subcategory": "(Human Resources & Recruitment)",
  "job_url": "https://www.seek.com.au/job/88373645...",
  "posted_date": "3d ago",
  "description": "...",
  "scraped_at": "2025-11-08T11:08:28.142557",
  "job_id": "88373645"
}
```

### **2. Deduplication Database**

**File**: `data/seen_jobs.json`
- **Purpose**: Tracks all job URLs ever seen to prevent duplicates
- **Contains**: Job URLs and first seen timestamps
- **Size**: ~149KB
- **Critical**: DO NOT delete this file (prevents duplicate jobs)

### **3. Scraper Logs**

**Location**: `logs/scraper_{date}.log`
- **Contains**: Complete scraper run history
- **Created**: Daily when scraper runs
- **Example**: `logs/scraper_2025-11-08.log`
- **Shows**:
  - Start/end times
  - Jobs found per page
  - Errors or issues
  - Total jobs scraped

**View recent logs**:
```bash
tail -f logs/scraper_*.log
```

---

## 🔍 How to Check Data

### **View All Jobs (JSON format)**
```bash
# Pretty print the jobs file
cat data/jobs_2025-11-08.json | python3 -m json.tool | less
```

### **Count Total Jobs**
```bash
# Count jobs in database
cat data/jobs_2025-11-08.json | python3 -c "import sys, json; print(len(json.load(sys.stdin)))"
```

### **Check Latest Scrape Time**
```bash
# View most recent log
ls -t logs/scraper_*.log | head -1 | xargs tail -20
```

### **View Scrape History**
```bash
# List all scraper logs
ls -lh logs/scraper_*.log
```

---

## 💾 Backup Strategy

### **Automatic Backups (Recommended)**

The system naturally creates backups because:
1. **Daily snapshots**: Each scrape creates `jobs_{date}.json`
2. **Deduplication**: Prevents data loss from duplicate jobs
3. **Logs**: Complete audit trail of all scrapes

### **Manual Backup (Before Important Changes)**

```bash
# Create a backup of all data
cd JobScraperSeek
tar -czf backup_$(date +%Y%m%d_%H%M%S).tar.gz data/ logs/ config/

# Creates: backup_20251108_110000.tar.gz
```

### **Restore from Backup**

```bash
# Extract backup
tar -xzf backup_20251108_110000.tar.gz

# This restores:
# - data/ directory (all jobs)
# - logs/ directory (scraper history)
# - config/ directory (settings)
```

---

## 🚨 What If Data is Lost?

### **Scenario 1: Missed a Scheduled Scrape**

**Problem**: Cron job didn't run, missed 3 days of jobs

**Solution**:
1. Run manual scrape immediately:
   ```bash
   ./run_scraper.sh
   ```

2. Jobs will be scraped with current date
3. You'll capture jobs posted in last 3 days (based on `date_range: 3` setting)
4. **Impact**: You may miss jobs that were posted 4-6 days ago

### **Scenario 2: `jobs_{date}.json` File Deleted**

**Problem**: Main job database file accidentally deleted

**Solution**:
1. Check if you have a backup:
   ```bash
   ls -lh backup_*.tar.gz
   ```

2. Restore from backup if available:
   ```bash
   tar -xzf backup_YYYYMMDD_HHMMSS.tar.gz data/
   ```

3. If no backup, run a fresh scrape:
   ```bash
   ./run_scraper.sh
   ```

4. **Impact**: You'll get fresh jobs from last 3 days, but lose historical data

### **Scenario 3: `seen_jobs.json` File Deleted**

**Problem**: Deduplication tracker deleted

**Solution**:
1. **Don't panic** - the job database is still intact
2. Run the scraper again - it will recreate `seen_jobs.json`
3. **Impact**: Next scrape may include some duplicate jobs (deduplication will be rebuilt)

### **Scenario 4: Entire `data/` Directory Lost**

**Problem**: Complete data loss

**Solution**:
1. Restore from backup if available
2. If no backup, start fresh:
   ```bash
   mkdir data
   ./run_scraper.sh
   ```
3. **Impact**: Lose all historical data, but can scrape fresh jobs

---

## 📊 Data Retention

### **Current Settings** (from `config/config.yaml`):

- **Job retention**: `retention_days: 30`
  - **Jobs older than 30 days are AUTOMATICALLY DELETED** ✅
  - Cleanup happens every time the scraper runs
  - Main database only keeps jobs from last 30 days

- **Date range for scraping**: `date_range: 3`
  - Only scrapes jobs posted in last 3 days

### **Automatic Cleanup**

Every time the scraper runs, it automatically:
1. Scrapes new jobs from Seek
2. Saves them to database
3. **Removes jobs older than 30 days** (automatic cleanup)

This keeps your database size manageable and only shows recent, relevant jobs.

### **How Database Size Changes Over Time**

**Week 1**: 397 jobs (all fresh)
**Week 2**: ~600 jobs (397 old + 200 new)
**Week 3**: ~800 jobs (600 old + 200 new)
**Week 4**: ~1000 jobs (800 old + 200 new)
**Week 5**: ~1000 jobs (stable - old jobs deleted, new jobs added)
**Week 6**: ~1000 jobs (stable - automatic cleanup keeps it balanced)

**Database size stabilizes at ~1000 jobs** after 30 days.

---

## 🔐 Important Files to NEVER Delete

1. ✅ **`data/jobs_{date}.json`** - Main database (all jobs)
2. ✅ **`data/seen_jobs.json`** - Deduplication tracker
3. ✅ **`config/config.yaml`** - Configuration settings
4. ✅ **`venv/`** - Python virtual environment

**Safe to delete**:
- ❌ Old log files (`logs/scraper_*.log` older than 30 days)
- ❌ Old backup files (`backup_*.tar.gz` older than 60 days)

---

## 📈 Monitoring Data Health

### **Daily Check** (Optional)

```bash
# Quick health check
echo "Jobs in database: $(cat data/jobs_2025-11-08.json | python3 -c 'import sys, json; print(len(json.load(sys.stdin)))')"
echo "Last scrape: $(ls -t logs/scraper_*.log | head -1)"
```

### **Monthly Check** (Recommended)

1. Check database size: `du -h data/`
2. Review logs for errors: `grep -i error logs/scraper_*.log`
3. Create monthly backup: `tar -czf monthly_backup_$(date +%Y%m).tar.gz data/ config/`

---

## 💡 Pro Tips

1. **Set up automatic backups**:
   ```bash
   # Add to crontab to backup weekly
   0 0 * * 0 cd /path/to/JobScraperSeek && tar -czf backup_$(date +\%Y\%m\%d).tar.gz data/
   ```

2. **Monitor disk space**:
   ```bash
   df -h .
   ```

3. **Archive old jobs** (if database gets too large):
   - Export to CSV from dashboard
   - Save CSV files to external storage
   - Keep only last 90 days in active database

4. **Version control your configs**:
   ```bash
   # Track changes to configuration
   git add config/config.yaml
   git commit -m "Updated excluded companies list"
   ```

---

## 📞 Quick Reference

| What                      | Location                        | Can Delete? |
|---------------------------|---------------------------------|-------------|
| Job database              | `data/jobs_*.json`              | ⚠️ Backup first |
| Deduplication tracker     | `data/seen_jobs.json`           | ❌ Keep it |
| Scraper logs              | `logs/scraper_*.log`            | ✅ After 30d |
| Configuration             | `config/config.yaml`            | ❌ Keep it |
| Backups                   | `backup_*.tar.gz`               | ✅ After 60d |
| Python packages           | `venv/`                         | ❌ Keep it |

---

**Questions?** Check the logs first: `tail -f logs/scraper_*.log`
