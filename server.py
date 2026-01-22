#!/usr/bin/env python3
"""
MCP Server for Nexus Production Insights
Provides simplified tools for analyzing production code flows and usage patterns.
"""

import asyncio
import json
import logging
import os
import aiohttp
from typing import Any, Dict, List, Optional

from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.types import Tool, TextContent, Resource
import mcp.types as types

# Configure logging
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, log_level, logging.INFO),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("codekarma-mcp-server")

class NexusClient:
    """Client for interacting with Nexus API"""
    
    def __init__(self, base_url: str = None, domain: str = "test"):
        # Use environment variable CK_NEXUS_ENDPOINT if provided, otherwise use passed base_url, 
        # or fallback to default AWS ELB endpoint
        self.base_url = (
            os.getenv("CK_NEXUS_ENDPOINT") or 
            base_url or 
            "http://ac9248ac6be104c95987a0356fbd9ad6-d76d2f43834084df.elb.us-east-2.amazonaws.com:8081"
        )
        self.domain = domain
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def get_method_summary(self, service_name: str, class_name: str, 
                                method_name: Optional[str] = None, step: str = "1m") -> List[Dict[str, Any]]:
        """Get method summary using the mpks API"""
        url = f"{self.base_url}/{self.domain}/api/method-graph-paths/mpks"
        params = {
            "serviceName": service_name,
            "className": class_name,
            "profilingInfo": "true",
            "step": step
        }
        if method_name:
            params["methodName"] = method_name
        
        async with self.session.get(url, params=params) as response:
            response.raise_for_status()
            return await response.json()
    
    async def get_method_flows(self, service_name: str, class_name: str, 
                              method_name: Optional[str] = None, step: str = "1m") -> List[Dict[str, Any]]:
        """Get flow IDs for a specific method or all methods in a class"""
        url = f"{self.base_url}/{self.domain}/api/method-graph-paths/flows"
        params = {
            "serviceName": service_name,
            "className": class_name,
            "step": step
        }
        if method_name:
            params["methodName"] = method_name
        
        async with self.session.get(url, params=params) as response:
            response.raise_for_status()
            return await response.json()
    
    async def get_multiple_flow_details(self, service_name: str, flow_ids: List[int], step: str = "1m") -> Dict[str, Any]:
        """Get detailed flow information for multiple flow IDs"""
        url = f"{self.base_url}/{self.domain}/api/method-graph-paths/flow-details"
        
        params_list = [("serviceName", service_name), ("step", step)]
        for flow_id in flow_ids:
            params_list.append(("flowIds", str(flow_id)))
        
        async with self.session.get(url, params=params_list) as response:
            response.raise_for_status()
            return await response.json()
    
    async def get_hot_methods(self, service_name: str, cpu_threshold: float = 1.0, step: str = "1m") -> List[Dict[str, Any]]:
        """Get hot methods using the hot-methods API"""
        url = f"{self.base_url}/{self.domain}/api/method-graph-paths/hot-methods"
        params = {
            "serviceName": service_name,
            "cpuThreshold": cpu_threshold,
            "step": step
        }
        
        async with self.session.get(url, params=params) as response:
            response.raise_for_status()
            return await response.json()
    
    async def find_service_names(self, class_names: List[str]) -> Dict[str, Any]:
        """Find service names using a list of class names"""
        url = f"{self.base_url}/{self.domain}/api/method-graph-paths/find-service-name"
        payload = {"classNames": class_names}
        
        async with self.session.post(url, json=payload) as response:
            response.raise_for_status()
            return await response.json()

# Initialize the server
server = Server("codekarma-mcp-server")

@server.list_resources()
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

@server.read_resource()
async def handle_read_resource(uri: str) -> str:
    """Read production analytics resource content"""
    if uri == "production://capabilities":
        return '''
{
  "description": "Production Code Analytics - Analyze real application performance and usage patterns",
  "capabilities": [
    {
      "name": "Service Discovery", 
      "description": "Find service names from class names visible in your IDE when service name is unknown",
      "metrics": ["Service name matching", "Domain identification", "Class-to-service mapping"]
    },
    {
      "name": "Production Usage Analysis", 
      "description": "Analyze method execution patterns and throughput in production",
      "metrics": ["QPS", "Error rates", "Latency", "Active vs inactive methods"]
    },
    {
      "name": "Production Call Flow Analysis",
      "description": "Analyze how methods call each other in production with performance metrics and hot method identification",
      "metrics": ["Call patterns", "Aggregated QPS", "Method relationships", "HTTP endpoints", "Performance bottlenecks", "Hot method annotations"]
    },
    {
      "name": "Hot Method Detection",
      "description": "Identify CPU-intensive methods consuming significant resources",
      "metrics": ["CPU utilization %", "Execution frequency", "Performance impact"]
    }
  ],
  "benefits": [
    "Data-driven optimization decisions",
    "Production usage validation",
    "Information to write data driven production use-case based tests",
    "Risk assessment for code changes",
    "Performance bottleneck identification",
    "Automatic service discovery from class names"
  ]
}
'''
    elif uri == "production://metrics":
        return '''
{
  "performance_metrics": {
    "throughput": {
      "qps": "Queries per second - request frequency",
      "qpm": "Queries per minute - sustained load measurement"
    },
    "quality": {
      "error_rate": "Percentage of failed executions",
      "latency_ms": "Average response time in milliseconds"
    },
    "resource_usage": {
      "cpu_utilization_percent": "CPU consumption percentage (hot methods)",
      "execution_count": "Total number of method invocations"
    }
  },
  "call_flow_analysis": {
    "call_patterns": "How methods call each other in production",
    "flow_ids": "Unique identifiers for specific execution paths", 
    "http_endpoints": "API endpoints that trigger method executions",
    "aggregated_metrics": "Combined performance data across all flows"
  },
  "status_indicators": {
    "inactive_methods": "Methods with zero production usage (potential dead code)",
    "active_methods": "Methods with production traffic",
    "hot_methods": "Methods exceeding CPU utilization thresholds"
  }
}
'''
    elif uri == "production://use-cases":
        return '''
{
  "service_discovery": {
    "scenario": "Don't know the service name but have class names from your IDE",
    "approach": "Use class names visible in your IDE to automatically discover which services contain those classes. Provide 10-20 class names for best matching accuracy.",
    "tools": ["find_service_names"],
    "example": "Provide class names like ['com.example.UserService', 'com.example.OrderController', 'com.example.DatabaseUtil'] to find matching service names"
  },
  "understanding_code_flows": {
    "scenario": "Understanding how code flows in production",
    "approach": "Analyze production call flows to understand how methods call each other and how they are used in production",
    "tools": ["get_production_call_flows"]
  },
  "writing_production_centered_tests": {
    "scenario": "Writing production centered tests",
    "approach": "Analyze production call flows to understand how methods call each other and how they are used in production",
    "tools": ["get_production_call_flows"]
  },
  "dead_code_cleanup": {
    "scenario": "Reduce codebase complexity by removing unused code",
    "approach": "Identify methods with zero production usage and validate they can be safely removed",
    "tools": ["get_production_usage"]
  },
  "performance_optimization": {
    "scenario": "Application is slow, need to identify bottlenecks",
    "approach": "Use get_hot_methods to find CPU-intensive operations, then analyze production call flows to understand impact and patterns",
    "tools": ["get_hot_methods", "get_production_call_flows"]
  },
  "code_review": {
    "scenario": "Planning to modify a critical method, assess impact first", 
    "approach": "Analyze production usage and call flow patterns to understand dependencies and usage",
    "tools": ["get_production_usage", "get_production_call_flows"]
  },
  "api_optimization": {
    "scenario": "Optimize high-traffic API endpoints",
    "approach": "Find hot methods in call flows, analyze throughput patterns to optimize critical paths",
    "tools": ["get_hot_methods", "get_production_call_flows"]
  },
  "deployment_planning": {
    "scenario": "Plan safe deployment of performance improvements",
    "approach": "Understand current production patterns and call flow relationships before optimization changes",
    "tools": ["get_production_usage", "get_hot_methods", "get_production_call_flows"]
  },
  "workflow_with_unknown_service": {
    "scenario": "Complete workflow when service name is unknown",
    "approach": "1) Use find_service_names with class names from IDE to discover services, 2) Use discovered service names with other production analysis tools",
    "tools": ["find_service_names", "get_production_usage", "get_production_call_flows", "get_hot_methods"],
    "example": "find_service_names(['com.example.UserService']) → get_production_usage(service_name='discovered-service', class_name='com.example.UserService')"
  }
}
'''
    else:
        raise ValueError(f"Unknown resource: {uri}")

@server.list_tools()
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
        # Note: Individual call hierarchy tool disabled to avoid confusion with unified tree
        # Uncomment below to re-enable individual flow tree analysis
        # Tool(
        #     name="get_production_method_call_hierarchy",
        #     description="Get production method call hierarchy showing individual execution flow trees",
        #     inputSchema={
        #         "type": "object",
        #         "properties": {
        #             "service_name": {"type": "string", "description": "Name of the service"},
        #             "class_name": {"type": "string", "description": "Full class name"},
        #             "method_name": {"type": "string", "description": "Optional: specific method name"},
        #             "step": {"type": "string", "description": "Time window (default: '1m')", "default": "1m"}
        #         },
        #         "required": ["service_name", "class_name"]
        #     }
        # ),
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

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle tool calls"""
    try:
        # For server.py (local), we use default domain 'test'
        async with NexusClient(domain="test") as client:
            if name == "get_production_usage":
                usage_report = await get_production_usage_impl(
                    client,
                    arguments["service_name"],
                    arguments["class_name"],
                    arguments.get("method_name"),
                    arguments.get("step", "1m")
                )
                return [types.TextContent(type="text", text=usage_report)]
            
            # Individual call hierarchy tool disabled - use unified execution tree instead
            # elif name == "get_production_method_call_hierarchy":
            #     hierarchy_report = await get_production_method_call_hierarchy_impl(
            #         client,
            #         arguments["service_name"],
            #         arguments["class_name"],
            #         arguments.get("method_name"),
            #         arguments.get("step", "1m")
            #     )
            #     return [types.TextContent(type="text", text=hierarchy_report)]
            
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

async def get_production_usage_impl(client: NexusClient, service_name: str, 
                                   class_name: str, method_name: Optional[str] = None, 
                                   step: str = "1m") -> str:
    """Get production usage information for methods using mpks API"""
    try:
        # Use the cleaner mpks API for method summary
        method_summaries = await client.get_method_summary(service_name, class_name, method_name, step)
        
        if not method_summaries:
            if method_name:
                return f"## Method Analysis Result\n\n**Method:** `{method_name}`\n**Production Status:** ❌ INACTIVE - This method is not invoked in production"
            else:
                return f"No production data found for {class_name}"
        
        report = []
        report.append(f"# Production Usage Report")
        report.append(f"**Service:** {service_name}")
        report.append(f"**Class:** {class_name}")
        if method_name:
            report.append(f"**Method:** {method_name}")
        report.append("")
        
        total_methods = len(method_summaries)
        active_methods = 0
        
        for method_summary in method_summaries:
            method_display_name = method_summary["methodNameOnly"]
            full_signature = method_summary["methodName"]
            qps = method_summary.get("qps", 0)
            qpm = method_summary.get("qpm", 0)
            error_rate = method_summary.get("errorRate", 0)
            latency_ms = method_summary.get("latencyms", 0)
            cpu_utilization = method_summary.get("cpuUtilizationPercent", 0)
            counter_value = method_summary.get("counterValue", 0)
            
            report.append(f"## Method: `{method_display_name}`")
            report.append(f"**Full Signature:** `{full_signature}`")
            
            # If Nexus returned the method, it means it exists in production monitoring
            # (even with QPS=0, it's still being monitored/tracked)
            if True:  # All methods returned by Nexus are considered active/monitored
                active_methods += 1
                report.append(f"**Production Status:** ✅ ACTIVE")
                report.append(f"**Throughput (QPS):** {qps}")
                report.append(f"**Throughput (QPM):** {qpm}")
                report.append(f"**Error Rate:** {error_rate}%")
                
                # Add CPU utilization with hot method detection
                cpu_str = f"**CPU Utilization:** {cpu_utilization}%"
                if cpu_utilization > 0.1:
                    if cpu_utilization > 1.0:
                        cpu_str += " 🔥 HOT"
                report.append(cpu_str)
                
                # Check if it's a controller method (HTTP endpoint)
                if method_summary.get("controllerMethod", False):
                    http_route = method_summary.get("httpRoute", "N/A")
                    http_method = method_summary.get("httpMethod", "N/A")
                    report.append(f"**HTTP Endpoint:** {http_method} {http_route}")
            
            # Add method parameters if available
            if method_summary.get("methodParams"):
                params = ", ".join(method_summary["methodParams"])
                report.append(f"**Parameters:** {params}")
            
            report.append("")
        
        report.append("---")
        report.append(f"## Summary")
        report.append(f"- **Total Methods Analyzed:** {total_methods}")
        report.append(f"- **Active in Production:** {active_methods}")
        if not method_name:  # Only show this message when analyzing a full class
            report.append(f"- **Note:** Only the methods listed above are active in production. Any other methods in the class `{class_name.split('.')[-1]}` are inactive.")
        report.append(f"- **Production Activity Rate:** 100% (of monitored methods)")
        
        return "\n".join(report)
        
    except Exception as e:
        return f"Error getting production usage: {str(e)}"

async def get_production_method_call_hierarchy_impl(client: NexusClient, service_name: str, 
                                                   class_name: str, method_name: Optional[str] = None, 
                                                   step: str = "1m") -> str:
    """Get production method call hierarchy showing execution flow trees"""
    try:
        flows_data = await client.get_method_flows(service_name, class_name, method_name, step)
        
        if not flows_data:
            return f"No production data found for {class_name}"
        
        # Get hot methods for annotation
        hot_methods = await client.get_hot_methods(service_name, cpu_threshold=1.0, step=step)
        hot_methods_map = {}
        for hot_method in hot_methods:
            hot_class_name = hot_method.get("className")
            hot_method_name = hot_method.get("methodNameOnly")
            if hot_class_name and hot_method_name:
                key = f"{hot_class_name}::{hot_method_name}"
                hot_methods_map[key] = hot_method.get("cpuUtilizationPercent", 0)
        
        report = []
        report.append(f"# Production Method Call Hierarchy")
        report.append(f"**Service:** {service_name}")
        report.append(f"**Class:** {class_name}")
        if method_name:
            report.append(f"**Method:** {method_name}")
        report.append("")
        
        report.append("## What is a Flow?")
        report.append("A **Flow** represents a complete execution path that occurred in production. Each flow captures:")
        report.append("- The sequence of method calls in a specific execution thread")
        report.append("- Performance metrics (QPS, latency, error rates) for each method")
        report.append("- HTTP endpoints that triggered the execution (if applicable)")
        report.append("- Branching patterns where different code paths were taken")
        report.append("")
        
        all_flow_ids = set()
        method_to_flows = {}
        
        for method_data in flows_data:
            method_sig = method_data["methodSignature"]
            flow_ids = method_data["flowIds"]
            method_name_key = method_sig["methodNameOnly"]
            
            if flow_ids:
                method_to_flows[method_name_key] = {
                    "signature": method_sig,
                    "flow_ids": flow_ids
                }
                all_flow_ids.update(flow_ids)
        
        if not all_flow_ids:
            report.append("## No Active Flows Found")
            report.append("All methods in this class appear to be inactive in production.")
            return "\n".join(report)
        
        flow_ids_list = list(all_flow_ids)
        flow_details_dict = await client.get_multiple_flow_details(service_name, flow_ids_list, step)
        
        report.append(f"## Execution Flow Trees")
        report.append(f"Found {len(all_flow_ids)} unique execution flows involving this class")
        report.append("")
        
        # Process each flow detail (they come as a dictionary keyed by flow ID)
        processed_flows = 0
        for flow_id_str, flow_details in flow_details_dict.items():
            if processed_flows >= 10:  # Limit to first 10 flows for readability
                break
                
            report.append(f"### Flow #{flow_id_str}")
            
            # Extract flow summary from the root element
            flow_summary = extract_flow_summary(flow_details)
            if flow_summary:
                report.append(f"**Flow QPS:** {flow_summary.get('qps', 'N/A')}")
                report.append(f"**Flow Duration:** {flow_summary.get('duration', 'N/A')}ms")
                if flow_summary.get('http_endpoint'):
                    report.append(f"**Triggered by:** {flow_summary['http_endpoint']}")
            
            report.append("**Execution Tree:**")
            tree_lines = build_execution_tree(flow_details, class_name, hot_methods_map=hot_methods_map)
            for line in tree_lines:
                report.append(line)
            report.append("")
            processed_flows += 1
        
        if len(all_flow_ids) > 10:
            report.append(f"*Note: Showing first 10 flows out of {len(all_flow_ids)} total flows for readability*")
            report.append("")
        
        report.append("---")
        report.append("## Method Flow Participation Summary")
        for method_name_key, method_info in method_to_flows.items():
            flow_count = len(method_info["flow_ids"])
            report.append(f"- **{method_name_key}:** Participates in {flow_count} flows")
        
        return "\n".join(report)
        
    except Exception as e:
        return f"Error getting method call hierarchy: {str(e)}"

async def get_unified_execution_tree_impl(client: NexusClient, service_name: str, 
                                         class_name: str, method_name: Optional[str] = None, 
                                         step: str = "1m") -> str:
    """Get a unified execution tree that combines all flow trees into a single comprehensive view"""
    try:
        flows_data = await client.get_method_flows(service_name, class_name, method_name, step)
        
        if not flows_data:
            return f"No production data found for {class_name}"
        
        # Get hot methods for annotation
        hot_methods = await client.get_hot_methods(service_name, cpu_threshold=1.0, step=step)
        hot_methods_map = {}
        for hot_method in hot_methods:
            hot_class_name = hot_method.get("className")
            hot_method_name = hot_method.get("methodNameOnly")
            if hot_class_name and hot_method_name:
                key = f"{hot_class_name}::{hot_method_name}"
                hot_methods_map[key] = hot_method.get("cpuUtilizationPercent", 0)
        
        report = []
        report.append(f"# Unified Execution Tree")
        report.append(f"**Service:** {service_name}")
        report.append(f"**Class:** {class_name}")
        if method_name:
            report.append(f"**Method:** {method_name}")
        report.append("")
        
        report.append("## What is the Unified Tree?")
        report.append("The **Unified Tree** combines all execution flows into a single comprehensive view where:")
        report.append("- Each node shows **aggregated metrics** across all flows that pass through it")
        report.append("- **Flow IDs** are listed to show which specific executions contribute to each node")
        report.append("- **Branch patterns** reveal how different flows diverge at decision points")
        report.append("- **Hot paths** and **common execution patterns** become clearly visible")
        report.append("")
        
        all_flow_ids = set()
        for method_data in flows_data:
            flow_ids = method_data["flowIds"]
            if flow_ids:
                all_flow_ids.update(flow_ids)
        
        if not all_flow_ids:
            report.append("## No Active Flows Found")
            report.append("All methods in this class appear to be inactive in production.")
            return "\n".join(report)
        
        flow_ids_list = list(all_flow_ids)
        flow_details_dict = await client.get_multiple_flow_details(service_name, flow_ids_list, step)
        
        # Build unified tree by merging all flows
        unified_tree = build_unified_tree(flow_details_dict, class_name)
        
        report.append(f"## Unified Execution Tree")
        report.append(f"Aggregated view of {len(all_flow_ids)} execution flows")
        report.append("")
        report.append("**Legend:**")
        report.append("- **Bold methods** belong to the target class")
        report.append("- **QPS:** Aggregated queries per second across all flows")
        report.append("- **Flows:** List of flow IDs that pass through this node")
        report.append("- **Errors:** Aggregated error rate")
        report.append("- **[HTTP endpoints]** shown for controller methods")
        report.append("")
        
        if unified_tree:
            tree_lines = render_unified_tree(unified_tree, class_name, hot_methods_map=hot_methods_map)
            for line in tree_lines:
                report.append(line)
        else:
            report.append("No unified tree could be constructed from the available flows.")
        
        report.append("")
        report.append("---")
        report.append("## Flow Statistics")
        report.append(f"- **Total Flows Analyzed:** {len(all_flow_ids)}")
        report.append(f"- **Unique Execution Paths:** {count_unique_paths(unified_tree) if unified_tree else 0}")
        report.append(f"- **Flow IDs:** {', '.join(map(str, sorted(all_flow_ids)))}")
        
        return "\n".join(report)
        
    except Exception as e:
        return f"Error getting unified execution tree: {str(e)}"

async def get_hot_methods_impl(client: NexusClient, service_name: str, step: str = "1m") -> str:
    """Get hot methods with high CPU utilization"""
    try:
        hot_methods = await client.get_hot_methods(service_name, cpu_threshold=1.0, step=step)
        
        if not hot_methods:
            return f"## Hot Methods Analysis\n\n**Service:** {service_name}\n\n**Result:** No hot methods found (no methods exceed 1% CPU utilization threshold)"
        
        report = []
        report.append(f"# Hot Methods Report")
        report.append(f"**Service:** {service_name}")
        report.append(f"**CPU Threshold:** ≥ 1.0%")
        report.append(f"**Time Window:** {step}")
        report.append("")
        
        report.append("## What are Hot Methods?")
        report.append("**Hot Methods** are methods with high CPU utilization that may be performance bottlenecks:")
        report.append("- Methods consuming significant CPU resources in production")
        report.append("- Potential candidates for optimization")
        report.append("- May indicate inefficient algorithms or resource-intensive operations")
        report.append("")
        
        report.append(f"## Hot Methods Found ({len(hot_methods)})")
        report.append("")
        
        # Sort by CPU utilization descending
        hot_methods_sorted = sorted(hot_methods, key=lambda x: x.get("cpuUtilizationPercent", 0), reverse=True)
        
        for i, method in enumerate(hot_methods_sorted, 1):
            class_name = method.get("className", "Unknown")
            method_name = method.get("methodNameOnly", "Unknown")
            full_signature = method.get("methodName", "Unknown")
            cpu_utilization = method.get("cpuUtilizationPercent", 0)
            qps = method.get("qps", 0)
            qpm = method.get("qpm", 0)
            error_rate = method.get("errorRate", 0)
            counter_value = method.get("counterValue", 0)
            
            simple_class = class_name.split('.')[-1] if class_name else 'Unknown'
            
            report.append(f"### {i}. `{simple_class}.{method_name}` 🔥")
            report.append(f"**Full Class:** `{class_name}`")
            report.append(f"**Full Signature:** `{full_signature}`")
            report.append(f"**CPU Utilization:** {cpu_utilization:.3f}%")
            report.append(f"**Throughput (QPS):** {qps:,.2f}")
            report.append(f"**Throughput (QPM):** {qpm:,.2f}")
            report.append(f"**Total Invocations:** {counter_value:,.2f}")
            
            if error_rate > 0:
                report.append(f"**Error Rate:** {error_rate:.2f}%")
            
            # Add method parameters if available
            if method.get("methodParams"):
                params = ", ".join(method["methodParams"])
                report.append(f"**Parameters:** {params}")
            
            # Check if it's a controller method (HTTP endpoint)
            if method.get("controllerMethod", False):
                http_route = method.get("httpRoute", "N/A")
                http_method = method.get("httpMethod", "N/A")
                report.append(f"**HTTP Endpoint:** {http_method} {http_route}")
            
            report.append("")
        
        report.append("---")
        report.append("## Summary & Recommendations")
        total_cpu = sum(method.get("cpuUtilizationPercent", 0) for method in hot_methods)
        report.append(f"- **Total Hot Methods:** {len(hot_methods)}")
        report.append(f"- **Combined CPU Impact:** {total_cpu:.3f}%")
        report.append(f"- **Primary Optimization Target:** `{hot_methods_sorted[0].get('className', '').split('.')[-1]}.{hot_methods_sorted[0].get('methodNameOnly', '')}` ({hot_methods_sorted[0].get('cpuUtilizationPercent', 0):.3f}% CPU)")
        report.append("")
        report.append("**Optimization Recommendations:**")
        report.append("1. Profile the highest CPU methods for algorithmic improvements")
        report.append("2. Consider caching for frequently called methods")
        report.append("3. Review database queries and I/O operations in hot paths")
        report.append("4. Monitor these methods after optimization to measure impact")
        
        return "\n".join(report)
        
    except Exception as e:
        return f"Error getting hot methods: {str(e)}"

async def find_service_names_impl(client: NexusClient, class_names: List[str]) -> str:
    """Find service names using a list of class names"""
    try:
        result = await client.find_service_names(class_names)
        
        report = []
        report.append("# Service Name Discovery")
        report.append("")
        
        # Show the input class names
        report.append(f"## Input Classes ({len(class_names)})")
        if len(class_names) <= 10:
            for i, class_name in enumerate(class_names, 1):
                simple_class = class_name.split('.')[-1] if '.' in class_name else class_name
                report.append(f"{i}. `{simple_class}` (Full: `{class_name}`)")
        else:
            for i in range(5):
                class_name = class_names[i]
                simple_class = class_name.split('.')[-1] if '.' in class_name else class_name
                report.append(f"{i+1}. `{simple_class}` (Full: `{class_name}`)")
            report.append(f"   ... and {len(class_names) - 5} more classes")
        report.append("")
        
        # Display results
        available = result.get("available", False)
        service_names = result.get("serviceNames", [])
        domain_name = result.get("domainName", "N/A")
        
        report.append("## Discovery Results")
        
        if available and service_names:
            report.append(f"✅ **Service Names Found:** {len(service_names)} matching service(s)")
            report.append(f"**Domain:** {domain_name}")
            report.append("")
            report.append("### Matching Services:")
            for i, service_name in enumerate(service_names, 1):
                report.append(f"{i}. `{service_name}`")
            
            report.append("")
            if len(service_names) > 1:
                report.append("### 🤖 LLM Instructions")
                report.append(f"**Multiple services found!** Please ask the user: *\"I found {len(service_names)} services that contain your classes: {', '.join(service_names)}. Which service would you like to analyze?\"* Wait for the user to specify which service name to use before proceeding with other production analysis tools.")
                report.append("")
            
            report.append("### Next Steps")
            if len(service_names) == 1:
                report.append("You can now use this service name with other production analysis tools:")
                report.append(f"- `get_production_usage(service_name=\"{service_names[0]}\", class_name=\"...\")`")
                report.append(f"- `get_production_call_flows(service_name=\"{service_names[0]}\", class_name=\"...\")`")
                report.append(f"- `get_hot_methods(service_name=\"{service_names[0]}\")`")
            else:
                report.append("Once the user selects a service, use it with other production analysis tools:")
                report.append("- `get_production_usage(service_name=\"[user-selected-service]\", class_name=\"...\")`")
                report.append("- `get_production_call_flows(service_name=\"[user-selected-service]\", class_name=\"...\")`")
                report.append("- `get_hot_methods(service_name=\"[user-selected-service]\")`")
            
        elif available and not service_names:
            report.append("⚠️ **Service Discovery:** API is available but no matching services found")
            report.append(f"**Domain:** {domain_name}")
            report.append("")
            report.append("**Possible reasons:**")
            report.append("- The provided class names might not exist in any monitored service")
            report.append("- Services containing these classes might not be actively monitored")
            report.append("- Class names might be misspelled or outdated")
            report.append("")
            report.append("**Suggestions:**")
            report.append("- Try with different class names from the codebase")
            report.append("- Ensure class names are fully qualified (with package names)")
            report.append("- Verify that the services are running and being monitored")
            
        else:
            report.append("❌ **Service Discovery:** API is not available or returned invalid response")
            report.append(f"**Domain:** {domain_name}")
            report.append("")
            report.append("**Possible issues:**")
            report.append("- Nexus service might be unavailable")
            report.append("- Service discovery feature might be disabled")
            report.append("- Network connectivity issues")
        
        return "\n".join(report)
        
    except Exception as e:
        return f"Error finding service names: {str(e)}"

def find_method_in_flow(flow_data: Dict[str, Any], method_hash: int) -> Optional[Dict[str, Any]]:
    """Recursively find a method in the flow tree by its hash"""
    def search_recursive(node):
        if isinstance(node, dict):
            if 'element' in node and node['element'].get('methodDetailsHash') == method_hash:
                return node['element']
            for value in node.values():
                result = search_recursive(value)
                if result:
                    return result
        elif isinstance(node, list):
            for item in node:
                result = search_recursive(item)
                if result:
                    return result
        return None
    
    return search_recursive(flow_data)

def extract_flow_summary(flow_data: Dict[str, Any]) -> Dict[str, Any]:
    """Extract high-level summary information from flow data"""
    summary = {}
    
    if 'element' in flow_data:
        element = flow_data['element']
        summary['qps'] = element.get('qps', 0)
        summary['duration'] = element.get('latencyms', 0)
        
        # Look for HTTP endpoint info in the root or children
        http_endpoint = find_http_endpoint_in_flow(flow_data)
        if http_endpoint:
            summary['http_endpoint'] = http_endpoint
    
    return summary

def find_http_endpoint_in_flow(flow_data: Dict[str, Any]) -> Optional[str]:
    """Recursively search for HTTP endpoint information in the flow"""
    if 'element' in flow_data:
        element = flow_data['element']
        if element.get('controllerMethod'):
            http_method = element.get('httpMethod', '')
            http_route = element.get('httpRoute', '')
            if http_method and http_route:
                return f"{http_method} {http_route}"
    
    # Search in children
    children_dict = flow_data.get('children', {})
    for child in children_dict.values():
        result = find_http_endpoint_in_flow(child)
        if result:
            return result
    
    return None

def build_execution_tree(flow_data: Dict[str, Any], target_class: str, prefix: str = "", is_last: bool = True, hot_methods_map: Optional[Dict[str, float]] = None) -> List[str]:
    """Build a text-based tree representation of the execution flow"""
    lines = []
    
    if 'element' in flow_data:
        element = flow_data['element']
        class_name = element.get('className', '')
        method_name = element.get('methodNameOnly', element.get('methodName', ''))
        qps = element.get('qps', 0)
        error_rate = element.get('errorRate', 0)
        method_hash = element.get('methodDetailsHash')
        
        # Store original method name for hot method lookup
        original_method_name = method_name
        
        # Clean up method name if it includes signature for display
        if '(' in method_name:
            method_name = method_name.split('(')[0]
        
        simple_class = class_name.split('.')[-1] if class_name else 'Unknown'
        tree_symbol = "└── " if is_last else "├── "
        
        # Format metrics
        qps_str = f"{qps:.2f}" if isinstance(qps, (int, float)) and qps > 0 else "0"
        
        # Format error rates
        error_str = f", Errors: {error_rate:.1f}%" if error_rate > 0 else ""
        
        # Check if this method is hot and add CPU annotation
        cpu_annotation = ""
        if hot_methods_map and class_name and original_method_name:
            method_key = f"{class_name}::{original_method_name}"
            if method_key in hot_methods_map:
                cpu_percent = hot_methods_map[method_key]
                cpu_annotation = f", CPU: {cpu_percent:.2f}% 🔥"
        
        # Highlight methods from the target class and show HTTP endpoints
        if target_class in class_name:
            method_display = f"**{simple_class}.{method_name}** (QPS: {qps_str}{error_str}{cpu_annotation})"
        else:
            method_display = f"{simple_class}.{method_name} (QPS: {qps_str}{error_str}{cpu_annotation})"
        
        # Add HTTP endpoint info if this is a controller method
        if element.get('controllerMethod', False):
            http_method = element.get('httpMethod', '')
            http_route = element.get('httpRoute', '')
            if http_method and http_route:
                method_display += f" [{http_method} {http_route}]"
        
        lines.append(f"{prefix}{tree_symbol}{method_display}")
        
        # Handle children - they are in a dictionary with MPK keys
        children_dict = flow_data.get('children', {})
        if children_dict:
            new_prefix = prefix + ("    " if is_last else "│   ")
            children_list = list(children_dict.values())
            for i, child in enumerate(children_list):
                is_child_last = (i == len(children_list) - 1)
                child_lines = build_execution_tree(child, target_class, new_prefix, is_child_last, hot_methods_map)
                lines.extend(child_lines)
    
    return lines

class UnifiedNode:
    """Represents a node in the unified execution tree"""
    def __init__(self, method_hash: int, element: Dict[str, Any]):
        self.method_hash = method_hash
        self.class_name = element.get('className', '')
        self.method_name = element.get('methodNameOnly', element.get('methodName', ''))
        self.http_method = element.get('httpMethod', '')
        self.http_route = element.get('httpRoute', '')
        self.controller_method = element.get('controllerMethod', False)
        
        # Aggregated metrics
        self.flow_ids = set()
        self.total_qps = 0.0
        self.total_error_rate = 0.0
        self.occurrence_count = 0
        
        # Children (keyed by method hash)
        self.children = {}
        
        # Add initial data
        self.add_occurrence(element)
    
    def add_occurrence(self, element: Dict[str, Any]):
        """Add data from another occurrence of this method"""
        qps = element.get('qps', 0)
        error_rate = element.get('errorRate', 0)
        
        self.total_qps += qps
        self.total_error_rate += error_rate
        self.occurrence_count += 1
    
    def add_flow_id(self, flow_id: str):
        """Add a flow ID that passes through this node"""
        self.flow_ids.add(flow_id)
    
    def get_average_error_rate(self) -> float:
        """Get average error rate across all occurrences"""
        return self.total_error_rate / self.occurrence_count if self.occurrence_count > 0 else 0
    
    def get_simple_class_name(self) -> str:
        """Get simplified class name"""
        return self.class_name.split('.')[-1] if self.class_name else 'Unknown'
    
    def get_method_signature(self) -> str:
        """Get a unique signature for this method"""
        return f"{self.class_name}::{self.method_name}"

def build_unified_tree(flow_details_dict: Dict[str, Any], target_class: str = "") -> Optional[UnifiedNode]:
    """Build a unified tree by merging all flow trees"""
    if not flow_details_dict:
        return None
    
    # Find all root nodes and merge them
    root_nodes = {}
    
    for flow_id, flow_data in flow_details_dict.items():
        if 'element' in flow_data:
            root_element = flow_data['element']
            method_hash = root_element.get('methodDetailsHash')
            
            if method_hash is not None:
                if method_hash not in root_nodes:
                    root_nodes[method_hash] = UnifiedNode(method_hash, root_element)
                else:
                    root_nodes[method_hash].add_occurrence(root_element)
                
                root_nodes[method_hash].add_flow_id(flow_id)
                
                # Recursively merge children
                merge_children(root_nodes[method_hash], flow_data, flow_id)
    
    # If we have multiple root nodes, create a virtual root
    if len(root_nodes) == 1:
        return list(root_nodes.values())[0]
    elif len(root_nodes) > 1:
        # Create virtual root that encompasses all execution entry points
        virtual_root = UnifiedNode(-1, {
            'className': 'VirtualRoot',
            'methodNameOnly': 'MultipleEntryPoints',
            'methodName': 'MultipleEntryPoints',
            'qps': 0,
            'errorRate': 0
        })
        for root_node in root_nodes.values():
            virtual_root.children[root_node.method_hash] = root_node
            virtual_root.flow_ids.update(root_node.flow_ids)
        return virtual_root
    
    return None

def merge_children(parent_node: UnifiedNode, flow_data: Dict[str, Any], flow_id: str):
    """Recursively merge children into the unified tree"""
    children_dict = flow_data.get('children', {})
    
    for _, child_data in children_dict.items():
        if 'element' in child_data:
            child_element = child_data['element']
            child_hash = child_element.get('methodDetailsHash')
            
            if child_hash is not None:
                if child_hash not in parent_node.children:
                    parent_node.children[child_hash] = UnifiedNode(child_hash, child_element)
                else:
                    parent_node.children[child_hash].add_occurrence(child_element)
                
                parent_node.children[child_hash].add_flow_id(flow_id)
                
                # Recursively merge grandchildren
                merge_children(parent_node.children[child_hash], child_data, flow_id)

def render_unified_tree(root_node: UnifiedNode, target_class: str, prefix: str = "", is_last: bool = True, hot_methods_map: Optional[Dict[str, float]] = None) -> List[str]:
    """Render the unified tree as text"""
    lines = []
    
    simple_class = root_node.get_simple_class_name()
    method_name = root_node.method_name
    
    # Clean up method name if it includes signature
    if '(' in method_name:
        method_name = method_name.split('(')[0]
    
    tree_symbol = "└── " if is_last else "├── "
    
    # Format metrics
    qps_str = f"{root_node.total_qps:.2f}" if root_node.total_qps > 0 else "0"
    avg_error_rate = root_node.get_average_error_rate()
    error_str = f", Errors: {avg_error_rate:.1f}%" if avg_error_rate > 0 else ""
    
    # Check if this method is hot and add CPU annotation
    cpu_annotation = ""
    if hot_methods_map and root_node.class_name and root_node.method_name:
        # Use the original method name for lookup (before cleaning)
        original_method_name = root_node.method_name
        method_key = f"{root_node.class_name}::{original_method_name}"
        if method_key in hot_methods_map:
            cpu_percent = hot_methods_map[method_key]
            cpu_annotation = f", CPU: {cpu_percent:.2f}% 🔥"
    
    # Format flow IDs (limit to first 5 for readability)
    flow_ids_list = sorted(list(root_node.flow_ids))
    if len(flow_ids_list) > 5:
        flows_str = f"Flows: [{', '.join(map(str, flow_ids_list[:5]))}...+{len(flow_ids_list)-5}]"
    else:
        flows_str = f"Flows: [{', '.join(map(str, flow_ids_list))}]"
    
    # Highlight methods from the target class
    if target_class in root_node.class_name:
        method_display = f"**{simple_class}.{method_name}** (QPS: {qps_str}{error_str}{cpu_annotation}) {flows_str}"
    else:
        method_display = f"{simple_class}.{method_name} (QPS: {qps_str}{error_str}{cpu_annotation}) {flows_str}"
    
    # Add HTTP endpoint info if this is a controller method
    if root_node.controller_method and root_node.http_method and root_node.http_route:
        method_display += f" [{root_node.http_method} {root_node.http_route}]"
    
    lines.append(f"{prefix}{tree_symbol}{method_display}")
    
    # Handle children
    if root_node.children:
        new_prefix = prefix + ("    " if is_last else "│   ")
        children_list = list(root_node.children.values())
        # Sort children by total QPS (descending) to show hottest paths first
        children_list.sort(key=lambda x: x.total_qps, reverse=True)
        
        for i, child in enumerate(children_list):
            is_child_last = (i == len(children_list) - 1)
            child_lines = render_unified_tree(child, target_class, new_prefix, is_child_last, hot_methods_map)
            lines.extend(child_lines)
    
    return lines

def count_unique_paths(root_node: UnifiedNode) -> int:
    """Count the number of unique execution paths in the tree"""
    if not root_node:
        return 0
    
    if not root_node.children:
        return 1  # Leaf node = 1 path
    
    total_paths = 0
    for child in root_node.children.values():
        total_paths += count_unique_paths(child)
    
    return total_paths

async def main():
    """Main entry point for the MCP server"""
    import mcp.server.stdio
    
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="codekarma-mcp-server",
                server_version="2.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main()) 