# 🚀 Deployment Checklist

Use this checklist to deploy the Seek Job Scraper for your team.

---

## ✅ Pre-Deployment

- [x] Code pushed to GitHub: https://github.com/JixuanYU0/JobScraperSeek
- [ ] GitHub repo is private (recommended) or public
- [x] `.gitignore` configured (no sensitive data pushed)
- [x] `render.yaml` created
- [x] `runtime.txt` created
- [x] `requirements.txt` present

---

## ✅ Deploy Scraper API to Render

### Account Setup
- [ ] Created Render.com account
- [ ] Connected GitHub to Render
- [ ] Authorized Render to access your repo

### Service Creation
- [ ] Created new Web Service
- [ ] Connected to: `JixuanYU0/JobScraperSeek`
- [ ] Name set to: `seek-scraper-api`
- [ ] Runtime set to: `Python 3`
- [ ] Build command: `pip install -r requirements.txt && playwright install chromium && playwright install-deps chromium`
- [ ] Start command: `python3 api_server.py --host 0.0.0.0 --port $PORT`
- [ ] Plan: `Free`
- [ ] Clicked "Create Web Service"

### Verify Deployment
- [ ] Deployment completed (status: Live)
- [ ] Copied URL: `https://seek-scraper-api-_______.onrender.com`
- [ ] Tested health endpoint: `https://seek-scraper-api-_______.onrender.com/api/v1/health`
- [ ] Response shows: `{"status":"healthy"}`

**Scraper API URL:** `_________________________________`

---

## ✅ Deploy n8n to Render

### Service Creation
- [ ] Created new Web Service
- [ ] Selected "Deploy an existing image from a registry"
- [ ] Image URL: `n8nio/n8n:latest`
- [ ] Name set to: `n8n-workflow-automation`
- [ ] Plan: `Free`

### Environment Variables Set
- [ ] `N8N_HOST` = `n8n-workflow-automation-_______.onrender.com`
- [ ] `N8N_PORT` = `5678`
- [ ] `N8N_PROTOCOL` = `https`
- [ ] `WEBHOOK_URL` = `https://n8n-workflow-automation-_______.onrender.com/`
- [ ] `GENERIC_TIMEZONE` = `Australia/Sydney`
- [ ] `N8N_BASIC_AUTH_ACTIVE` = `true`
- [ ] `N8N_BASIC_AUTH_USER` = `admin` (or your choice)
- [ ] `N8N_BASIC_AUTH_PASSWORD` = `___________` (SECURE PASSWORD!)
- [ ] Clicked "Create Web Service"

### Verify Deployment
- [ ] Deployment completed (status: Live)
- [ ] Copied URL: `https://n8n-workflow-automation-_______.onrender.com`
- [ ] Can access n8n login page
- [ ] Can login with credentials

**n8n URL:** `_________________________________`
**Username:** `_________________________________`
**Password:** `_________________________________` (Keep secure!)

---

## ✅ Configure n8n Workflow

### Import Workflow
- [ ] Logged into n8n
- [ ] Clicked "Workflows" → "Add workflow" → "Import from File"
- [ ] Selected `n8n_workflow_example.json`
- [ ] Workflow imported successfully

### Update API URL
- [ ] Opened imported workflow
- [ ] Clicked "Trigger Scraping" node
- [ ] Updated URL from `http://your-api-server:8000`
- [ ] To: `https://seek-scraper-api-_______.onrender.com`
- [ ] Saved node

### Configure Google Sheets
- [ ] Created Google Sheet with columns: title, company, location, salary, job_url, posted_date, scraped_at
- [ ] Clicked "Save to Google Sheets" node
- [ ] Created credential → Signed in with Google
- [ ] Selected correct Google Sheet
- [ ] Selected correct sheet name
- [ ] Column mapping verified
- [ ] Saved node

**Google Sheet URL:** `_________________________________`

### Configure Slack (Optional)
- [ ] Clicked "Slack Notification" node
- [ ] Created credential → Signed in to Slack
- [ ] Selected channel (e.g., #job-alerts)
- [ ] Customized message (optional)
- [ ] Saved node
- [ ] OR: Deleted this node if not using Slack

### Activate Workflow
- [ ] Toggled "Active" switch to ON 🟢
- [ ] Saved workflow

---

## ✅ Test Everything

### Test 1: API Health
- [ ] Visited: `https://seek-scraper-api-_______.onrender.com/api/v1/health`
- [ ] Response: `{"status":"healthy"}`

### Test 2: Manual Workflow Execution
- [ ] In n8n, clicked "Execute Workflow"
- [ ] All nodes turned green ✅
- [ ] Waited ~60 seconds
- [ ] Checked Google Sheet
- [ ] Jobs appeared in sheet ✅

### Test 3: Webhook
- [ ] Workflow execution completed
- [ ] Google Sheet updated automatically
- [ ] (If using) Slack notification received

### Test 4: Schedule
- [ ] Verified schedule node shows: `0 9 * * *` (daily at 9 AM)
- [ ] OR: Changed to desired schedule
- [ ] Workflow is Active (green toggle)

---

## ✅ Documentation

### Team Handover Documents Created
- [x] `TEAM_HANDOVER_GUIDE.md` - User guide for team
- [x] `DEPLOYMENT_CHECKLIST.md` - This file
- [ ] Updated `README.md` with deployment info

### Information to Share with Team
- [ ] n8n URL
- [ ] n8n login credentials (securely!)
- [ ] Google Sheet URL
- [ ] `TEAM_HANDOVER_GUIDE.md` file
- [ ] Quick start: "Just open n8n → Execute workflow"

---

## ✅ Handover Meeting

### Prepare for Meeting
- [ ] Test workflow one more time
- [ ] Have all URLs ready
- [ ] Have credentials written down (securely)
- [ ] Have Google Sheet open
- [ ] Have n8n open in browser

### During Meeting - Show Team:
- [ ] How to access n8n
- [ ] How to execute workflow manually
- [ ] Where to find results (Google Sheet)
- [ ] How to view execution history
- [ ] How to check if API is healthy
- [ ] Who to contact if issues

### Provide Team:
- [ ] n8n login credentials (secure method - password manager, 1Password, etc.)
- [ ] Google Sheet link (with edit access)
- [ ] Link to `TEAM_HANDOVER_GUIDE.md`
- [ ] Your contact info for questions

---

## ✅ Post-Deployment

### Monitor First Week
- [ ] Day 1: Check workflow ran successfully at 9 AM
- [ ] Day 2: Check workflow ran successfully
- [ ] Day 3: Check workflow ran successfully
- [ ] Day 7: Review with team - any issues?

### Render Dashboard Access
- [ ] Gave team member access to Render dashboard (if needed)
- [ ] Showed how to view logs
- [ ] Showed how to restart services

### GitHub Access (Optional)
- [ ] Added team members as collaborators (if they're technical)
- [ ] OR: Kept access with team lead only

---

## ✅ Optional Enhancements

Consider adding later:
- [ ] Increase max_pages for more jobs
- [ ] Add email notifications via n8n
- [ ] Set up monitoring/alerting
- [ ] Create job analytics dashboard
- [ ] Add other job boards (Indeed, LinkedIn)

---

## 📝 Notes & Issues

**Deployment Date:** ___________________

**Deployed By:** ___________________

**Issues Encountered:**
-
-
-

**Solutions:**
-
-
-

**Team Feedback:**
-
-
-

---

## 🎉 Success Criteria

Your deployment is successful when:
- ✅ API is live and responds to health check
- ✅ n8n is accessible and team can log in
- ✅ Workflow executes successfully
- ✅ Jobs appear in Google Sheet
- ✅ Team can execute workflow manually
- ✅ Scheduled run works at 9 AM
- ✅ Team knows who to contact for issues

---

**Status:** [ ] Not Started | [ ] In Progress | [ ] Completed ✅

**Next Review Date:** ___________________

