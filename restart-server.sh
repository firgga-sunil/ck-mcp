#!/bin/bash

echo "🔄 Restarting CodeKarma MCP Server..."

# Stop any running container
docker-compose down

# Start fresh container  
docker-compose up -d --build

echo "✅ Server restarted and running on http://localhost:8547"
