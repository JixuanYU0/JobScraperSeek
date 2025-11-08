#!/bin/bash

# Setup Cron Job for Automated Scraping
# This script sets up a cron job to run the scraper every 3 days at 9:00 AM

# Get the absolute path of the project directory
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Cron job command - runs every 3 days at 9:00 AM
CRON_SCHEDULE="0 9 */3 * *"
CRON_COMMAND="cd $PROJECT_DIR && $PROJECT_DIR/run_scraper.sh"
CRON_JOB="$CRON_SCHEDULE $CRON_COMMAND"

echo "=========================================="
echo "Seek Job Scraper - Cron Job Setup"
echo "=========================================="
echo ""
echo "This will set up automated scraping with the following schedule:"
echo "  - Every 3 days at 9:00 AM"
echo "  - Logs saved to: $PROJECT_DIR/logs/"
echo ""
echo "Cron job to be added:"
echo "  $CRON_JOB"
echo ""
read -p "Do you want to continue? (y/n): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Setup cancelled."
    exit 0
fi

# Check if cron job already exists
EXISTING_CRON=$(crontab -l 2>/dev/null | grep -F "$PROJECT_DIR/run_scraper.sh")

if [ -n "$EXISTING_CRON" ]; then
    echo ""
    echo "Found existing cron job for this scraper:"
    echo "  $EXISTING_CRON"
    echo ""
    read -p "Do you want to replace it? (y/n): " -n 1 -r
    echo ""

    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Setup cancelled."
        exit 0
    fi

    # Remove existing cron job
    crontab -l 2>/dev/null | grep -v -F "$PROJECT_DIR/run_scraper.sh" | crontab -
    echo "Removed existing cron job."
fi

# Add new cron job
(crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -

echo ""
echo "=========================================="
echo "Cron job installed successfully!"
echo "=========================================="
echo ""
echo "The scraper will now run automatically:"
echo "  - Every 3 days at 9:00 AM"
echo "  - Next run: $(date -v+3d '+%Y-%m-%d 09:00:00' 2>/dev/null || date -d '+3 days' '+%Y-%m-%d 09:00:00' 2>/dev/null || echo 'Check cron schedule')"
echo ""
echo "To view your cron jobs:"
echo "  crontab -l"
echo ""
echo "To view scraper logs:"
echo "  tail -f $PROJECT_DIR/logs/scraper_*.log"
echo ""
echo "To remove the cron job later:"
echo "  crontab -e"
echo "  (then delete the line containing: run_scraper.sh)"
echo ""
echo "IMPORTANT: Make sure the dashboard servers are always running!"
echo "  Run: ./start.sh"
echo ""
