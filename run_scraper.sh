#!/bin/bash

# Job Scraper - Automated Run Script
# This script runs the scraper and logs the output

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Log file with timestamp
LOG_FILE="logs/scraper_$(date +%Y-%m-%d).log"

# Ensure logs directory exists
mkdir -p logs

# Run the scraper and log output
echo "=====================================================" >> "$LOG_FILE"
echo "Scraper run started at: $(date)" >> "$LOG_FILE"
echo "=====================================================" >> "$LOG_FILE"

./venv/bin/python3 main.py >> "$LOG_FILE" 2>&1

echo "=====================================================" >> "$LOG_FILE"
echo "Scraper run completed at: $(date)" >> "$LOG_FILE"
echo "=====================================================" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
