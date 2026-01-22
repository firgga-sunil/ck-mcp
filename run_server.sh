#!/bin/bash

# CodeKarma MCP Server Runner
# This script activates the virtual environment and runs the MCP server

echo "🚀 Starting CodeKarma MCP Server..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Run setup.sh first."
    exit 1
fi

# Activate virtual environment and run server
source venv/bin/activate
exec python3 server.py 