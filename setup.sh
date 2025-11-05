#!/bin/bash

# Setup script for Seek Job Scraper

echo "🚀 Setting up Seek Job Scraper..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Install Playwright browsers
echo "🌐 Installing Playwright browsers..."
playwright install chromium

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please update .env with your credentials"
fi

# Test installation
echo ""
echo "✅ Setup complete!"
echo ""
echo "To get started:"
echo "  1. Activate the virtual environment: source venv/bin/activate"
echo "  2. Update config/config.yaml if needed"
echo "  3. Run the scraper: python main.py"
echo ""
echo "For scheduling:"
echo "  Run: crontab -e"
echo "  Add: 0 9 * * * cd $(pwd) && ./schedule_scraper.sh"
echo ""
