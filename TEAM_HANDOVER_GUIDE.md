# Seek Job Scraper - Team User Guide

## 🎯 What This Does

Automatically scrapes HR & Recruitment jobs from Seek.com.au daily and saves them to Google Sheets.

---

## 🔗 Access Links

**n8n Workflow Automation:**
- URL: `https://n8n-workflow-automation-xxxx.onrender.com`
- Username: `admin`
- Password: `[Ask team lead]`

**API Server:**
- URL: `https://seek-scraper-api-xxxx.onrender.com`
- Health Check: `https://seek-scraper-api-xxxx.onrender.com/api/v1/health`

**GitHub Repository:**
- URL: `https://github.com/JixuanYU0/JobScraperSeek`
- Access: Contact team lead for access

**Google Sheet:**
- URL: `[Your Google Sheet Link]`

---

## 📱 How to Use (For Non-Technical Team)

### Daily Automatic Scraping (No Action Needed)

The system runs automatically every day at 9 AM:
- ✅ Scrapes Seek.com.au
- ✅ Filters out recruitment agencies
- ✅ Removes duplicates
- ✅ Saves to Google Sheet
- ✅ Sends Slack notification

**You just open the Google Sheet and see new jobs!**

---

### Manual Scraping (Run Anytime)

**When to use:** Need fresh jobs immediately, not waiting for 9 AM

**Steps:**

1. **Open n8n**
   ```
   Go to: https://n8n-workflow-automation-xxxx.onrender.com
   Login with credentials above
   ```

2. **Find the workflow**
   ```
   Click: "Workflows" (left menu)
   Open: "Seek Job Scraper Integration"
   ```

3. **Execute**
   ```
   Click: "Execute Workflow" button (top right)
   Wait: ~60 seconds
   ```

4. **Check results**
   ```
   Open your Google Sheet
   New rows with jobs appear!
   ```

**That's it!** No coding needed.

---

## 🛠️ Troubleshooting

### Problem: "No new jobs found"

**Check:**
- Is it a public holiday? (Fewer job postings)
- Already scraped today? (Duplicates are filtered)

**Solution:**
- Wait for tomorrow
- Or change date range (contact team lead)

---

### Problem: "Workflow execution failed"

**Check:**
1. Is API healthy?
   - Visit: `https://seek-scraper-api-xxxx.onrender.com/api/v1/health`
   - Should show: `{"status":"healthy"}`
   - If not, it's waking up (wait 30 seconds and try again)

2. Still failing?
   - Check n8n execution log:
     - Click on the failed workflow
     - Scroll down to see error message
     - Common issues:
       - Google Sheets credential expired → Reconnect
       - Slack credential expired → Reconnect

---

### Problem: "Google Sheet not updating"

**Solution:**
1. Open n8n workflow
2. Click "Save to Google Sheets" node
3. Click "Reconnect credential"
4. Sign in to Google again
5. Try executing workflow again

---

### Problem: "Slack notification not working"

**Solution:**
1. Open n8n workflow
2. Click "Slack Notification" node
3. Click "Reconnect credential"
4. Sign in to Slack again
5. Try executing workflow again

---

## 📊 Understanding the Data

### Columns in Google Sheet:

| Column | Description | Example |
|--------|-------------|---------|
| title | Job title | "HR Manager" |
| company | Company name | "Tech Corp Pty Ltd" |
| location | Job location | "Sydney NSW" |
| salary | Salary range | "$80,000 - $100,000" |
| job_url | Link to job | Click to apply |
| posted_date | When posted | "2d ago" |
| scraped_at | When we found it | "2025-11-05T14:30:00" |

### What's Filtered Out:

- ❌ Recruitment agencies (Hays, Michael Page, etc.)
- ❌ "Recruitment - Agency" subcategory
- ❌ Duplicate job posts
- ❌ Jobs older than 3 days

### What You Get:

- ✅ Direct employer jobs only
- ✅ HR & Recruitment category
- ✅ Recent postings (last 3 days)
- ✅ Unique jobs only

---

## 🔧 Advanced: Changing Settings

### Change Schedule (Daily 9 AM → Different Time)

1. Open n8n workflow
2. Click "Schedule - Daily 9 AM" node
3. Change cron expression:
   - Every 4 hours: `0 */4 * * *`
   - Twice daily (9 AM & 5 PM): `0 9,17 * * *`
   - Every Monday at 9 AM: `0 9 * * 1`
4. Click "Save"

### Change Max Pages (Scrape More/Less)

1. Open n8n workflow
2. Click "Trigger Scraping" node
3. Find `max_pages` parameter
4. Change value:
   - More jobs: `10` or `20`
   - Fewer jobs (faster): `3` or `5`
5. Click "Save"

---

## 📞 Support

### For Technical Issues:

**Check Render Dashboard:**
- Scraper API: https://dashboard.render.com
- Can restart services if needed
- View logs for errors

**Check GitHub:**
- Code repository: https://github.com/JixuanYU0/JobScraperSeek
- All documentation is here

### Contact:

**Team Lead:** [Your name/email]

**For urgent issues:**
1. Check if API is healthy (link above)
2. Try manual workflow execution
3. Check Slack for error notifications
4. Contact team lead

---

## 💰 Costs

**Current setup:**
- ✅ Render (API): $0/month
- ✅ Render (n8n): $0/month
- ✅ Google Sheets: $0/month
- ✅ Slack: $0/month (free tier)
- ✅ GitHub: $0/month (public repo)

**Total: $0/month** 🎉

**Note:** Free tier has some limits:
- API sleeps after 15 min inactivity (wakes automatically in 30-60 sec)
- n8n sleeps after 15 min inactivity (wakes automatically)
- This is normal and expected!

---

## 🎓 Training Resources

### Video Tutorials (If needed):

Ask team lead to record:
1. How to manually execute workflow (2 min video)
2. How to view execution history (1 min video)
3. How to reconnect Google Sheets (1 min video)

### Quick Reference Card:

**Daily usage:** Just open Google Sheet → See new jobs

**Manual trigger:** n8n → Open workflow → Click "Execute"

**Check health:** Visit API health URL → Should say "healthy"

---

## 📝 Maintenance

### Monthly Checks (Team Lead):

- [ ] Verify Render services are running
- [ ] Check Google Sheets credential still valid
- [ ] Review scraped job count (should be steady)
- [ ] Check logs for errors

### When to Worry:

- ❌ No jobs for 3+ days in a row
- ❌ API health check shows "unhealthy"
- ❌ Workflow always fails
- ❌ Google Sheet stopped updating

### When NOT to Worry:

- ✅ Weekend has fewer jobs (normal)
- ✅ Occasional execution failure (retries automatically)
- ✅ API takes 30-60 sec to respond first time (waking up)
- ✅ Duplicate count is high (working as intended!)

---

## 🚀 Future Enhancements

Ideas for improving the system:

- [ ] Email notifications when specific keywords appear
- [ ] Filter by salary range
- [ ] Filter by specific locations
- [ ] Add Indeed.com scraping
- [ ] Add LinkedIn scraping
- [ ] Create analytics dashboard
- [ ] Automatic job matching to candidates

**Want these features?** Contact team lead to discuss!

---

**Last Updated:** November 2025
**Version:** 1.0
**Maintained By:** [Your Team Name]

---

**Questions?** Check this guide first, then contact team lead.

**Feedback?** Let us know how to improve this system!

