#!/bin/bash

echo "🔧 MCP Client Configuration Generator"
echo "====================================="
echo ""

# Function to generate auth token
generate_token() {
    python3 -c "import secrets; print('mcp_' + secrets.token_urlsafe(32))"
}

# Ask for connection type
echo "1. Choose Connection Type:"
echo "   [1] Direct Connection (ck-domain) - Connect directly to MCP server"
echo "   [2] nginx Proxy (Bearer Token) - Connect through nginx with authentication"
echo ""
read -p "Enter choice (1 or 2): " auth_choice

# Ask for client type
echo ""
echo "2. Choose MCP Client Type:"
echo "   [1] Windsurf"
echo "   [2] Claude Desktop / Cursor"
echo ""
read -p "Enter choice (1 or 2): " client_choice

echo ""
echo "🎯 Generated Configuration:"
echo "=========================="

# Generate configuration based on choices
if [ "$auth_choice" = "1" ]; then
    # Direct Connection with ck-domain
    echo "Enter the domain name (e.g., test, production, staging):"
    read -p "Domain: " domain
    
    if [ "$client_choice" = "1" ]; then
        # Windsurf with ck-domain
        echo "📋 Copy this to your Windsurf MCP config (Direct Connection):"
        echo ""
        cat << EOF
{
  "mcpServers": {
    "codekarma-insights": {
      "serverUrl": "http://localhost:8547/mcp",
      "headers": {
        "ck-domain": "$domain"
      }
    }
  }
}
EOF
    else
        # Claude Desktop/Cursor with ck-domain
        echo "📋 Copy this to your Claude Desktop/Cursor MCP config (Direct Connection):"
        echo ""
        cat << EOF
{
  "mcpServers": {
    "codekarma-insights": {
      "url": "http://localhost:8547/mcp",
      "headers": {
        "ck-domain": "$domain"
      }
    }
  }
}
EOF
    fi
    
    echo ""
    echo "💡 Direct connection - MCP server reads ck-domain header directly"
    echo "🔗 This will make Nexus API calls to: /$domain/api/method-graph-paths/..."
    
elif [ "$auth_choice" = "2" ]; then
    # nginx Proxy with Bearer Token
    TOKEN=$(generate_token)
    echo "Enter the nginx proxy URL (e.g., https://your-nginx-proxy.com):"
    read -p "nginx URL: " nginx_url
    
    if [ "$client_choice" = "1" ]; then
        # Windsurf with nginx Proxy
        echo "📋 Copy this to your Windsurf MCP config (nginx Proxy):"
        echo ""
        cat << EOF
{
  "mcpServers": {
    "codekarma-insights": {
      "serverUrl": "$nginx_url/mcp",
      "headers": {
        "Authorization": "Bearer $TOKEN"
      }
    }
  }
}
EOF
    else
        # Claude Desktop/Cursor with nginx Proxy
        echo "📋 Copy this to your Claude Desktop/Cursor MCP config (nginx Proxy):"
        echo ""
        cat << EOF
{
  "mcpServers": {
    "codekarma-insights": {
      "url": "$nginx_url/mcp",
      "headers": {
        "Authorization": "Bearer $TOKEN"
      }
    }
  }
}
EOF
    fi
    
    echo ""
    echo "🔐 nginx validates Bearer token, then adds ck-domain header to MCP server"
    echo "🎫 Bearer Token: $TOKEN"
    echo "💡 nginx determines domain and makes Nexus API calls to: /{domain}/api/method-graph-paths/..."
    
else
    echo "❌ Invalid choice. Please run the script again."
    exit 1
fi

echo ""
echo "📁 Common Config File Locations:"
echo "  • Claude Desktop: ~/.config/claude-desktop/claude_desktop_config.json"
echo "  • Cursor: ~/.cursor/mcp_config.json"
echo "  • Windsurf: ~/.codeium/windsurf/mcp_config.json"
echo ""
echo "🔄 After updating your config, restart your IDE to load the MCP server!"
