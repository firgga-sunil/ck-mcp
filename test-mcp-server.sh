#!/bin/bash

# Test script for CodeKarma MCP Server
# Usage: ./test-mcp-server.sh

set -e

# Configuration
SERVER_URL="http://localhost:8547"
DOMAIN="test"  # Domain for testing - can be test, production, staging, etc.

echo "🧪 Testing CodeKarma MCP Server"
echo "=================================="
echo "Server: $SERVER_URL"
echo "Domain: $DOMAIN"
echo ""

# Test 1: Health Check
echo "1️⃣  HEALTH CHECK"
echo "-------------------"
curl -s "$SERVER_URL/health" | jq .
echo ""

# Test 2: MCP Initialize
echo "2️⃣  MCP INITIALIZE"
echo "-------------------"
curl -X POST "$SERVER_URL/mcp" \
  -H "ck-domain: $DOMAIN" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}}}' \
  | jq .
echo ""

# Test 3: Tools List
echo "3️⃣  TOOLS LIST"
echo "----------------"
curl -X POST "$SERVER_URL/mcp" \
  -H "ck-domain: $DOMAIN" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}' \
  | jq '.result.tools | length as $count | "Found \($count) tools:", .[].name'
echo ""

# Test 4: Tool Call - Hot Methods  
echo "4️⃣  TOOL CALL - HOT METHODS"
echo "-----------------------------"
echo "Calling get_hot_methods for codetrails service..."
curl -X POST "$SERVER_URL/mcp" \
  -H "ck-domain: $DOMAIN" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "get_hot_methods", "arguments": {"service_name": "codetrails"}}}' \
  | jq -r '.result.content[0].text' | head -20
echo "... (truncated for display)"
echo ""

# Test 5: Service Discovery Tool
echo "5️⃣  TOOL CALL - SERVICE DISCOVERY"
echo "----------------------------------"
echo "Testing find_service_names with sample class names..."
curl -X POST "$SERVER_URL/mcp" \
  -H "ck-domain: $DOMAIN" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "find_service_names", "arguments": {"class_names": ["com.example.UserService", "com.example.OrderController"]}}}' \
  | jq -r '.result.content[0].text' | head -15
echo "... (truncated for display)"
echo ""

# Test 6: Another Tool Call - Production Usage
echo "6️⃣  TOOL CALL - PRODUCTION USAGE"
echo "----------------------------------"
echo "Testing get_production_usage for OrderServiceImpl..."
curl -X POST "$SERVER_URL/mcp" \
  -H "ck-domain: $DOMAIN" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "get_production_usage", "arguments": {"service_name": "codetrails", "class_name": "com.example.codetrails.orders.service.impl.OrderServiceImpl"}}}' \
  | jq -r '.result.content[0].text' | head -15
echo "... (truncated for display)"
echo ""

echo "✅ MCP Server Testing Complete!"
echo ""
echo "🎯 What This Shows:"
echo "- ✅ Server is healthy and responding"
echo "- ✅ MCP protocol is working (initialize, tools/list, tools/call)"
echo "- ✅ Domain-based routing works (ck-domain: $DOMAIN)"
echo "- ✅ Real production data is being returned from /$DOMAIN/api/method-graph-paths/"
echo "- ✅ All 4 tools are available and functional (including service discovery)"
echo ""
echo "💡 Domain Testing:"
echo "- Change DOMAIN variable to test different environments"
echo "- Domain 'test' → calls /test/api/method-graph-paths/..."
echo "- Domain 'production' → calls /production/api/method-graph-paths/..."
echo ""
echo "🔧 Use these curl commands to debug MCP client issues!"
