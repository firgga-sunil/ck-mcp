#!/usr/bin/env python3
"""
Remote MCP Server for Nexus Production Insights
Implements MCP protocol over HTTP JSON-RPC for remote access.
"""

import asyncio
import json
import logging
import os
import secrets
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.types import Tool, TextContent, Resource
import mcp.types as types

# Import the original server logic
from server import (
    NexusClient, 
    get_production_usage_impl,
    get_unified_execution_tree_impl,
    get_hot_methods_impl,
    find_service_names_impl
)

# Configure logging
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, log_level, logging.INFO),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("codekarma-mcp-server")

# Domain configuration 
# nginx upstream handles authentication and adds ck-domain header

# Initialize the MCP server instance (we'll use this for handlers)
mcp_server = Server("codekarma-mcp-server")

# Copy the tool and resource handlers from the original server
@mcp_server.list_resources()
async def handle_list_resources() -> List[Resource]:
    """List available resources for production code analytics"""
    return [
        Resource(
            uri="production://capabilities",
            name="Production Analytics Capabilities",
            description="Overview of available production code analysis features",
            mimeType="application/json"
        ),
        Resource(
            uri="production://metrics",
            name="Available Metrics", 
            description="Types of production metrics and performance data available",
            mimeType="application/json"
        ),
        Resource(
            uri="production://use-cases",
            name="Common Use Cases",
            description="Examples of how to use production analytics for optimization",
            mimeType="application/json"
        )
    ]

@mcp_server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """List available tools for Nexus production insights"""
    return [
        Tool(
            name="get_production_usage",
            description="Get production usage information for methods including throughput and activity status",
            inputSchema={
                "type": "object",
                "properties": {
                    "service_name": {
                        "type": "string",
                        "description": "Name of the service (e.g., 'codetrails')"
                    },
                    "class_name": {
                        "type": "string",
                        "description": "Full class name (e.g., 'com.example.codetrails.services.HttpClientService')"
                    },
                    "method_name": {
                        "type": "string",
                        "description": "Optional: specific method name. If not provided, returns usage for all methods in the class"
                    },
                    "step": {
                        "type": "string",
                        "description": "Time window for data aggregation (default: '1m')",
                        "default": "1m"
                    }
                },
                "required": ["service_name", "class_name"]
            }
        ),
        Tool(
            name="get_production_call_flows",
            description="Analyze production method call patterns and flows with aggregated performance metrics and hot method annotations",
            inputSchema={
                "type": "object",
                "properties": {
                    "service_name": {
                        "type": "string",
                        "description": "Name of the service"
                    },
                    "class_name": {
                        "type": "string",
                        "description": "Full class name"
                    },
                    "method_name": {
                        "type": "string",
                        "description": "Optional: specific method name. If not provided, shows unified tree for all methods in the class"
                    },
                    "step": {
                        "type": "string",
                        "description": "Time window for data aggregation (default: '1m')",
                        "default": "1m"
                    }
                },
                "required": ["service_name", "class_name"]
            }
        ),
        Tool(
            name="get_hot_methods",
            description="Get details about hot methods that have high CPU utilization in production (above 1% CPU threshold)",
            inputSchema={
                "type": "object",
                "properties": {
                    "service_name": {
                        "type": "string",
                        "description": "Name of the service"
                    },
                    "step": {
                        "type": "string",
                        "description": "Time window for data aggregation (default: '1m')",
                        "default": "1m"
                    }
                },
                "required": ["service_name"]
            }
        ),
        Tool(
            name="find_service_names",
            description="Find service names from a list of class names visible in the IDE. This tool helps discover which services contain the specified classes when the service name is unknown. Provide about 10-20 class names from the codebase for better matching accuracy.",
            inputSchema={
                "type": "object",
                "properties": {
                    "class_names": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "List of fully qualified class names (e.g., 'com.example.service.UserService', 'com.example.util.DatabaseUtil'). Provide 10-20 class names from the IDE/codebase for optimal service matching. More class names generally lead to better matching accuracy.",
                        "minItems": 1,
                        "maxItems": 50
                    }
                },
                "required": ["class_names"]
            }
        )
    ]

@mcp_server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle tool calls"""
    try:
        async with NexusClient() as client:
            if name == "get_production_usage":
                usage_report = await get_production_usage_impl(
                    client,
                    arguments["service_name"],
                    arguments["class_name"],
                    arguments.get("method_name"),
                    arguments.get("step", "1m")
                )
                return [types.TextContent(type="text", text=usage_report)]
            
            elif name == "get_production_call_flows":
                call_flows_report = await get_unified_execution_tree_impl(
                    client,
                    arguments["service_name"],
                    arguments["class_name"],
                    arguments.get("method_name"),
                    arguments.get("step", "1m")
                )
                return [types.TextContent(type="text", text=call_flows_report)]
            
            elif name == "get_hot_methods":
                hot_methods_report = await get_hot_methods_impl(
                    client,
                    arguments["service_name"],
                    arguments.get("step", "1m")
                )
                return [types.TextContent(type="text", text=hot_methods_report)]
            
            elif name == "find_service_names":
                service_names_report = await find_service_names_impl(
                    client,
                    arguments["class_names"]
                )
                return [types.TextContent(type="text", text=service_names_report)]
            
            else:
                raise ValueError(f"Unknown tool: {name}")
                
    except Exception as e:
        logger.error(f"Error handling tool {name}: {str(e)}")
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]

# FastAPI app for HTTP transport
app = FastAPI(
    title="CodeKarma Production Insights MCP Server",
    description="Remote MCP server implementing MCP protocol over HTTP",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_domain_from_headers(request: Request) -> str:
    """
    Get ck-domain from request headers (added by nginx upstream)
    Defaults to 'test' if not provided
    """
    domain = request.headers.get("ck-domain", "test")
    logger.debug(f"Using domain from nginx: {domain}")
    return domain

class MCPJSONRPCHandler:
    """Handles MCP JSON-RPC requests over HTTP"""
    
    async def handle_request(self, request_data: Dict[str, Any], domain: str = "test") -> Dict[str, Any]:
        """Handle incoming JSON-RPC request"""
        try:
            method = request_data.get("method")
            params = request_data.get("params", {})
            request_id = request_data.get("id")
            
            if method == "initialize":
                result = {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {},
                        "resources": {},
                        "prompts": {}
                    },
                    "serverInfo": {
                        "name": "codekarma-mcp-server",
                        "version": "2.0.0"
                    }
                }
            
            elif method == "tools/list":
                tools = await handle_list_tools()
                result = {"tools": [
                    {
                        "name": tool.name,
                        "description": tool.description,
                        "inputSchema": tool.inputSchema
                    }
                    for tool in tools
                ]}
            
            elif method == "tools/call":
                tool_result = await self.handle_tool_call(
                    params.get("name"), 
                    params.get("arguments", {}),
                    domain
                )
                result = {"content": [
                    {
                        "type": content.type,
                        "text": content.text
                    }
                    for content in tool_result
                ]}
            
            elif method == "resources/list":
                resources = await handle_list_resources()
                result = {"resources": [
                    {
                        "uri": str(resource.uri),
                        "name": resource.name,
                        "description": resource.description,
                        "mimeType": resource.mimeType
                    }
                    for resource in resources
                ]}
            
            else:
                raise ValueError(f"Unknown method: {method}")
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Error handling request: {str(e)}")
            return {
                "jsonrpc": "2.0",
                "id": request_data.get("id"),
                "error": {
                    "code": -1,
                    "message": str(e)
                }
            }
    
    async def handle_tool_call(self, name: str, arguments: Dict[str, Any], domain: str) -> List[types.TextContent]:
        """Handle tool calls with domain parameter"""
        try:
            async with NexusClient(domain=domain) as client:
                if name == "get_production_usage":
                    usage_report = await get_production_usage_impl(
                        client,
                        arguments["service_name"],
                        arguments["class_name"],
                        arguments.get("method_name"),
                        arguments.get("step", "1m")
                    )
                    return [types.TextContent(type="text", text=usage_report)]
                
                elif name == "get_production_call_flows":
                    call_flows_report = await get_unified_execution_tree_impl(
                        client,
                        arguments["service_name"],
                        arguments["class_name"],
                        arguments.get("method_name"),
                        arguments.get("step", "1m")
                    )
                    return [types.TextContent(type="text", text=call_flows_report)]
                
                elif name == "get_hot_methods":
                    hot_methods_report = await get_hot_methods_impl(
                        client,
                        arguments["service_name"],
                        arguments.get("step", "1m")
                    )
                    return [types.TextContent(type="text", text=hot_methods_report)]
                
                elif name == "find_service_names":
                    service_names_report = await find_service_names_impl(
                        client,
                        arguments["class_names"]
                    )
                    return [types.TextContent(type="text", text=service_names_report)]
                
                else:
                    raise ValueError(f"Unknown tool: {name}")
                    
        except Exception as e:
            logger.error(f"Error handling tool {name}: {str(e)}")
            return [types.TextContent(type="text", text=f"Error: {str(e)}")]

# Global handler instance
rpc_handler = MCPJSONRPCHandler()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "server": "codekarma-mcp-server",
        "version": "2.0.0",
        "protocol": "MCP over HTTP JSON-RPC"
    }

@app.post("/mcp")
async def mcp_endpoint(request: Request):
    """Main MCP JSON-RPC endpoint"""
    # Get domain from headers (nginx upstream adds this after authentication)
    domain = get_domain_from_headers(request)
    
    try:
        # Parse JSON-RPC request
        request_data = await request.json()
        logger.info(f"Received MCP request: {request_data.get('method', 'unknown')}")
        
        # Handle the request with domain
        response = await rpc_handler.handle_request(request_data, domain)
        
        return JSONResponse(content=response)
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8547))
    host = os.getenv("HOST", "0.0.0.0")
    
    logger.info(f"Starting CodeKarma MCP Server on {host}:{port}")
    logger.info(f"MCP Endpoint: http://{host}:{port}/mcp")
    logger.info(f"Architecture: Expects nginx upstream to handle authentication")
    logger.info(f"Domain Header: Reads 'ck-domain' header from nginx (defaults to 'test')")
    logger.info(f"Use ./generate-config.sh to create client configuration")
    
    uvicorn.run(
        "remote_server:app",
        host=host,
        port=port,
        log_level="info",
        reload=False
    )