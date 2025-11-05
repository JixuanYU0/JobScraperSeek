#!/bin/bash

# Seek Job Scraper - Scheduled Runner
# This script runs the scraper and can be used with cron

# Change to script directory
cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run the scraper
python main.py --output-format both

# Optional: Send notification on completion
# You can integrate with services like:
# - Slack webhook
# - Email notification
# - Discord webhook
# Example:
# curl -X POST -H 'Content-type: application/json' \
#   --data '{"text":"Seek scraper completed"}' \
#   YOUR_WEBHOOK_URL
