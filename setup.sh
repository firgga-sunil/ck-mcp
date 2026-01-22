#!/bin/bash

# CodeKarma MCP Server Setup Script
# This script sets up the virtual environment and installs all dependencies

echo "🔧 Setting up CodeKarma MCP Server..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment and install dependencies
echo "📥 Installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt

# Make scripts executable
chmod +x run_server.sh
chmod +x quick_test.py

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Make sure Nexus is running on http://localhost:8081"
echo "2. Add the configuration from claude_desktop_config.json to Claude Desktop"
echo "3. Test the server:"
echo "   - Run server: ./run_server.sh"
echo "   - Test tools: python3 quick_test.py"
echo ""
echo "For Claude Desktop integration, copy this configuration:"
echo "=============================================="
cat claude_desktop_config.json
echo "==============================================" 