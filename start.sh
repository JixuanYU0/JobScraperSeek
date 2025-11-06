#!/bin/bash
# Quick start script for Seek Job Scraper

# Kill any existing processes
echo "Stopping any existing servers..."
pkill -f "api_server.py" 2>/dev/null
pkill -f "simple_static_server.py" 2>/dev/null
sleep 1

echo "=========================================="
echo "Starting Seek Job Scraper Dashboard"
echo "=========================================="
echo ""

# Start API server in background
echo "Starting API server on port 8000..."
./venv/bin/python3 api_server.py --port 8000 > /dev/null 2>&1 &
API_PID=$!

# Wait for API to start
sleep 3

# Start frontend server in background
echo "Starting frontend server on port 8001..."
./venv/bin/python3 simple_static_server.py > /dev/null 2>&1 &
FRONTEND_PID=$!

# Wait for frontend to start
sleep 2

echo ""
echo "=========================================="
echo "✓ Dashboard is running!"
echo "=========================================="
echo ""
echo "🌐 Open in your browser:"
echo "  → http://localhost:8001"
echo ""
echo "📊 Jobs are loaded from JSON files automatically"
echo "🔄 Dashboard auto-refreshes every 5 minutes"
echo ""
echo "API Documentation (if needed):"
echo "  → http://localhost:8000/api/docs"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Trap Ctrl+C to cleanup
trap "echo 'Shutting down...'; kill $API_PID $FRONTEND_PID 2>/dev/null; exit" INT

# Wait for user to press Ctrl+C
wait
