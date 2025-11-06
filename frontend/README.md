# Seek Job Scraper - Frontend

A clean, professional React frontend for the Seek Job Scraper API.

## Features

- Trigger job scraping with a simple form
- Real-time status tracking with progress indicators
- Browse and filter scraped jobs
- Export results to CSV
- Mobile-responsive design
- Professional UI/UX

## Development

```bash
# Install dependencies
npm install

# Start development server (with API proxy)
npm run dev
```

The dev server runs on `http://localhost:3000` and proxies API requests to `http://localhost:8000`.

Make sure your API server is running:
```bash
# In the project root
python3 api_server.py
```

## Production Build

```bash
# Build for production
npm run build
```

This creates optimized static files in `../static/` that are served by the FastAPI backend.

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ScrapeForm.jsx      # Form to trigger scraping
│   │   ├── StatusTracker.jsx   # Real-time job status
│   │   ├── JobsList.jsx        # Jobs list with filters
│   │   └── JobCard.jsx         # Individual job card
│   ├── App.jsx                 # Main application
│   ├── App.css                 # Styles
│   └── main.jsx                # Entry point
└── vite.config.js              # Vite configuration
```

## Usage for Clients

1. **Start a Scrape**
   - Fill in keywords (e.g., "Software Engineer")
   - Select location
   - Choose number of pages
   - Click "Start Scraping"

2. **Track Progress**
   - Watch real-time status updates
   - See how many jobs were found

3. **View Results**
   - Browse jobs in card layout
   - Filter by location or company
   - Search by keywords
   - Export to CSV for further analysis

4. **View Job Details**
   - Click "View on Seek" to open the original listing

## API Integration

The frontend communicates with these API endpoints:

- `POST /api/v1/scrape` - Start scraping
- `GET /api/v1/scrape/{job_id}` - Check status
- `GET /api/v1/jobs/latest` - Fetch recent jobs

## Environment Variables

Create a `.env` file for custom API URL (optional):

```env
VITE_API_URL=http://localhost:8000
```

Leave empty for same-origin requests (production default).
