# Installation & Setup Guide

Complete guide to set up the Seek Job Scraper system from scratch.

---

## 📋 Prerequisites

### **Required Software**

1. **Python 3.9 or higher**
   - Check: `python3 --version`
   - Install: https://www.python.org/downloads/

2. **Node.js 18+ and npm** (for frontend build)
   - Check: `node --version` and `npm --version`
   - Install: https://nodejs.org/

3. **Git** (optional, for version control)
   - Check: `git --version`
   - Install: https://git-scm.com/

### **System Requirements**

- macOS, Linux, or Windows
- 2GB free disk space
- Internet connection (for scraping)

---

## 🚀 Installation Steps

### **Step 1: Set Up Python Environment**

```bash
# Navigate to project directory
cd JobScraperSeek

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip
```

### **Step 2: Install Python Dependencies**

```bash
# Install all required packages
pip install -r requirements.txt

# Install Playwright browsers (IMPORTANT!)
playwright install chromium
```

**What gets installed:**
- `playwright` - Web scraping automation
- `fastapi` & `uvicorn` - API server
- `pyyaml` - Configuration management
- `pydantic` - Data validation
- `requests` - HTTP client

### **Step 3: Install Frontend Dependencies**

```bash
# Navigate to frontend directory
cd frontend

# Install npm packages
npm install

# Build the frontend
npm run build

# Go back to root
cd ..
```

This creates the `static/` directory with built frontend files.

### **Step 4: Verify Installation**

```bash
# Check if all commands work
./venv/bin/python3 --version
./venv/bin/playwright --version

# Check if frontend is built
ls -la static/
```

You should see:
- `static/index.html`
- `static/assets/*.js`
- `static/assets/*.css`

---

## ⚙️ Configuration

### **Step 5: Review Configuration**

The default configuration is in `config/config.yaml`. Review these settings:

```yaml
scraper:
  date_range: 3                    # Scrape jobs from last 3 days
  max_pages: null                  # Scrape ALL pages (no limit)
  excluded_companies:              # 58 recruitment agencies excluded
    - "Hays"
    - "Hudson"
    # ... (see full list in config.yaml)

deduplication:
  retention_days: 30               # Auto-delete jobs older than 30 days
```

**No changes needed** - these are optimal defaults!

---

## 🎯 First Run

### **Step 6: Test the Scraper**

```bash
# Run a test scrape (takes ~2 minutes for 20 pages)
./venv/bin/python3 main.py
```

**Expected output:**
```
============================================================
Seek Job Scraper - Starting
============================================================
Starting scraping process...
Navigating to: https://www.seek.com.au/jobs-in-human-resources-recruitment...
Scraping page 1...
Found 20 jobs on page 1
...
Scraping page 20...
Total jobs scraped: 397
New jobs to save: 397
Cleaning up old jobs...
No jobs older than 30 days to clean up
Scraping completed successfully
============================================================
```

**Result:** You should now have:
- `data/jobs_2025-11-08.json` (397 jobs)
- `data/seen_jobs.json` (deduplication tracker)

### **Step 7: Start the Dashboard**

```bash
# Start both API and frontend servers
./start.sh
```

**Expected output:**
```
Starting Seek Job Scraper servers...
API Server starting on port 8000...
Frontend Server starting on port 8001...

Dashboard available at: http://localhost:8001
API docs available at: http://localhost:8000/api/docs

Press Ctrl+C to stop servers
```

### **Step 8: View the Dashboard**

Open your browser to: **http://localhost:8001**

You should see:
- ✅ Stats bar (total jobs, last 24h, companies)
- ✅ Color-coded job age badges (green/teal/orange/gray)
- ✅ Search and filter functionality
- ✅ All 397 jobs displayed

---

## 🤖 Set Up Automation

### **Step 9: Install Cron Job** (Automatic Scraping Every 3 Days)

```bash
# Run the interactive setup
./setup_cron.sh
```

**Follow the prompts:**
```
==========================================
Seek Job Scraper - Cron Job Setup
==========================================

This will set up automated scraping with the following schedule:
  - Every 3 days at 9:00 AM
  - Logs saved to: /path/to/JobScraperSeek/logs/

Do you want to continue? (y/n): y

==========================================
Cron job installed successfully!
==========================================
```

**Verify cron job is installed:**
```bash
crontab -l
```

You should see:
```
0 9 */3 * * cd /path/to/JobScraperSeek && /path/to/JobScraperSeek/run_scraper.sh
```

---

## ✅ Verification Checklist

After installation, verify everything works:

- [ ] **Python environment**: `./venv/bin/python3 --version` shows Python 3.9+
- [ ] **Playwright installed**: `./venv/bin/playwright --version` works
- [ ] **Frontend built**: `ls static/` shows `index.html` and `assets/`
- [ ] **First scrape completed**: `ls data/jobs_*.json` shows job file
- [ ] **Dashboard accessible**: http://localhost:8001 shows jobs
- [ ] **API working**: http://localhost:8000/api/v1/health shows "healthy"
- [ ] **Cron job installed**: `crontab -l` shows scraper schedule
- [ ] **Servers running**: `./start.sh` starts without errors

---

## 🔧 Troubleshooting

### **Issue: `playwright: command not found`**

**Solution:**
```bash
# Reinstall playwright and browsers
pip install playwright
playwright install chromium
```

### **Issue: `Permission denied: ./start.sh`**

**Solution:**
```bash
# Make scripts executable
chmod +x start.sh run_scraper.sh setup_cron.sh
```

### **Issue: Dashboard shows "Failed to fetch jobs"**

**Solution:**
```bash
# Check if API server is running
curl http://localhost:8000/api/v1/health

# If not running, restart servers
pkill -f api_server.py
pkill -f simple_static_server.py
./start.sh
```

### **Issue: Scraper finds 0 jobs**

**Solution:**
```bash
# Check internet connection
ping seek.com.au

# Check if Seek.com.au changed their HTML structure
# Run with visible browser to debug:
./venv/bin/python3 main.py --headless false
```

### **Issue: Cron job not running**

**Solution:**
```bash
# Check cron logs
tail -f /var/log/system.log | grep cron

# Test scraper manually
./run_scraper.sh

# Check if cron has correct path
crontab -l
```

---

## 📁 Project Structure

After installation, your directory should look like:

```
JobScraperSeek/
├── venv/                          # Python virtual environment
├── frontend/                      # React frontend source
│   ├── node_modules/              # npm packages
│   ├── src/
│   └── package.json
├── static/                        # Built frontend (served to users)
│   ├── index.html
│   └── assets/
├── data/                          # Job database
│   ├── jobs_2025-11-08.json
│   └── seen_jobs.json
├── logs/                          # Scraper logs
│   └── scraper_2025-11-08.log
├── config/
│   └── config.yaml                # Configuration
├── src/                           # Python source code
│   ├── scraper/
│   ├── storage/
│   ├── api/
│   └── utils/
├── main.py                        # Scraper entry point
├── api_server.py                  # API server
├── simple_static_server.py        # Frontend server
├── start.sh                       # Start both servers
├── run_scraper.sh                 # Run scraper with logging
├── setup_cron.sh                  # Install cron job
├── requirements.txt               # Python dependencies
└── INSTALLATION_GUIDE.md          # This file
```

---

## 🎓 Next Steps

Now that installation is complete:

1. **Customize excluded companies** (optional):
   - Edit `config/config.yaml`
   - Add/remove companies from `excluded_companies` list

2. **Adjust retention period** (optional):
   - Edit `config/config.yaml`
   - Change `retention_days: 30` to your preference

3. **Change scraping schedule** (optional):
   - Run: `crontab -e`
   - Modify: `0 9 */3 * *` to your preferred schedule
   - Examples:
     - Daily at 9am: `0 9 * * *`
     - Every 2 days: `0 9 */2 * *`
     - Weekly on Monday: `0 9 * * 1`

4. **Set up backups** (recommended):
   ```bash
   # Add weekly backup to cron
   crontab -e
   # Add line:
   0 0 * * 0 cd /path/to/JobScraperSeek && tar -czf backup_$(date +\%Y\%m\%d).tar.gz data/
   ```

---

## 📞 Quick Reference Commands

```bash
# Run scraper manually
./run_scraper.sh

# Start dashboard
./start.sh

# Stop dashboard
pkill -f api_server.py
pkill -f simple_static_server.py

# View logs
tail -f logs/scraper_*.log

# Check cron job
crontab -l

# Count jobs in database
cat data/jobs_*.json | python3 -c "import sys, json; print(len(json.load(sys.stdin)))"

# Backup data
tar -czf backup_$(date +%Y%m%d).tar.gz data/ config/

# Restore from backup
tar -xzf backup_20251108.tar.gz
```

---

## 🆘 Need Help?

1. Check logs: `tail -f logs/scraper_*.log`
2. Test API: `curl http://localhost:8000/api/v1/health`
3. Test scraper: `./venv/bin/python3 main.py --headless false`
4. Review configuration: `cat config/config.yaml`

---

**Installation Complete!** 🎉

Your Seek Job Scraper is now fully set up and ready to run automatically every 3 days.
