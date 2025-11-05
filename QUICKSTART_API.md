# Quick Start - API Server

Get the Seek Job Scraper API running in 5 minutes!

---

## Step 1: Install Dependencies (1 minute)

```bash
# Install Python packages
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

---

## Step 2: Start the API Server (30 seconds)

```bash
# Development mode (with auto-reload)
python api_server.py --reload
```

You should see:
```
============================================================
Seek Job Scraper API Server
============================================================
Server starting on http://0.0.0.0:8000
API Documentation: http://0.0.0.0:8000/api/docs
ReDoc: http://0.0.0.0:8000/api/redoc
============================================================
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## Step 3: Test the API (1 minute)

### Option A: Interactive API Docs (Recommended)

1. Open browser: http://localhost:8000/api/docs
2. Click on `POST /api/v1/scrape`
3. Click "Try it out"
4. Modify the request body:
   ```json
   {
     "headless": true,
     "max_pages": 1
   }
   ```
5. Click "Execute"
6. Copy the `job_id` from the response
7. Use `GET /api/v1/scrape/{job_id}` to check status

### Option B: Using cURL

```bash
# 1. Health check
curl http://localhost:8000/api/v1/health

# 2. Trigger scraping (1 page only for testing)
curl -X POST http://localhost:8000/api/v1/scrape \
  -H "Content-Type: application/json" \
  -d '{"headless": true, "max_pages": 1}'

# Response: {"job_id": "scrape_20251014_103045_abc123", ...}

# 3. Check status (replace with your job_id)
curl http://localhost:8000/api/v1/scrape/scrape_20251014_103045_abc123

# 4. Get latest jobs
curl http://localhost:8000/api/v1/jobs/latest?limit=5
```

### Option C: Using Python Test Script

```bash
python test_api.py
# Choose option 1 for comprehensive test
# Choose option 2 for quick scrape test
```

---

## Step 4: Integrate with n8n (2 minutes)

### Setup Webhook in n8n

1. **Create a new workflow in n8n**

2. **Add a Webhook node**
   - Set method to `POST`
   - Copy the webhook URL (e.g., `https://your-n8n.com/webhook/test`)

3. **Test the webhook from API**
   ```bash
   curl -X POST http://localhost:8000/api/v1/scrape \
     -H "Content-Type: application/json" \
     -d '{
       "headless": true,
       "max_pages": 1,
       "webhook_url": "https://your-n8n.com/webhook/test"
     }'
   ```

4. **Wait for scraping to complete**
   - n8n will automatically receive the results!

5. **Process the data in n8n**
   - Add nodes to save to Google Sheets, send Slack notifications, etc.

---

## Common Use Cases

### Use Case 1: Daily Automated Scraping

**Setup:**
1. Register a permanent webhook:
   ```bash
   curl -X POST http://localhost:8000/api/v1/webhooks \
     -H "Content-Type: application/json" \
     -d '{
       "webhook_url": "https://your-n8n.com/webhook/jobs",
       "events": ["scrape.completed"]
     }'
   ```

2. Schedule daily scraping in n8n:
   - Add **Schedule Trigger** node (e.g., 9 AM daily)
   - Add **HTTP Request** node pointing to `http://your-api:8000/api/v1/scrape`
   - Results automatically sent to your webhook!

### Use Case 2: On-Demand Scraping

**Setup:**
1. Create n8n workflow with **Webhook Trigger**
2. Add **HTTP Request** to call scraping API
3. Add **Wait** node (30 seconds)
4. Add **HTTP Request** to fetch results via `/api/v1/jobs/latest`
5. Process and save data

### Use Case 3: Multi-Source Job Aggregation

**Future enhancement:**
```bash
# Scrape multiple sources in parallel
POST /api/v1/scrape/seek
POST /api/v1/scrape/linkedin
POST /api/v1/scrape/indeed

# Aggregate results
GET /api/v1/jobs/aggregated
```

---

## Production Deployment

### Option 1: Docker

```bash
# Build image
docker build -t seek-scraper-api .

# Run container
docker run -d \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/config:/app/config \
  --name seek-api \
  seek-scraper-api
```

### Option 2: systemd Service

Create `/etc/systemd/system/seek-api.service`:
```ini
[Unit]
Description=Seek Job Scraper API
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/seek-scraper
ExecStart=/usr/bin/python3 /opt/seek-scraper/api_server.py --workers 4
Restart=always

[Install]
WantedBy=multi-user.target
```

Start service:
```bash
sudo systemctl enable seek-api
sudo systemctl start seek-api
```

### Option 3: PM2 (Node.js Process Manager)

```bash
# Install PM2
npm install -g pm2

# Start API
pm2 start api_server.py --name seek-api --interpreter python3

# Save configuration
pm2 save
pm2 startup
```

---

## Security (Optional)

### Enable API Key Authentication

1. **Generate API key:**
   ```bash
   python -c "from src.api.auth import generate_api_key; print(generate_api_key())"
   ```

2. **Add to .env file:**
   ```bash
   API_KEYS=your-generated-key-here
   ```

3. **Use in requests:**
   ```bash
   curl http://localhost:8000/api/v1/scrape \
     -H "X-API-Key: your-generated-key-here" \
     -H "Content-Type: application/json" \
     -d '{"headless": true}'
   ```

---

## Troubleshooting

### Issue: "Connection refused"
**Solution:** Make sure the API server is running:
```bash
python api_server.py --reload
```

### Issue: "Playwright browser not found"
**Solution:** Install Playwright browsers:
```bash
playwright install chromium
```

### Issue: Scraping job stuck in "running"
**Solution:**
1. Check logs in `logs/` directory
2. Restart the API server
3. Try with `headless: false` to see browser

### Issue: n8n webhook not receiving data
**Solution:**
1. Verify webhook URL is publicly accessible
2. Check webhook registration: `GET /api/v1/webhooks`
3. Test webhook manually with cURL

---

## Next Steps

1. **Read the full API documentation:** [API_GUIDE.md](API_GUIDE.md)
2. **Learn about AI Agent concepts:** [AI_AGENT_GUIDE.md](AI_AGENT_GUIDE.md)
3. **Import n8n workflow:** [n8n_workflow_example.json](n8n_workflow_example.json)
4. **Configure scraper settings:** [config/config.yaml](config/config.yaml)

---

## Support

- **API Documentation:** http://localhost:8000/api/docs
- **Health Check:** http://localhost:8000/api/v1/health
- **Test Script:** `python test_api.py`

---

**You're all set! Start scraping jobs and building your HR automation pipeline! 🚀**
