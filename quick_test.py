#!/usr/bin/env python3
"""
Quick test script for MCP server tools
Simple way to test the tools with your actual data
"""

import asyncio
import sys
from server import NexusClient, get_production_usage_impl, get_unified_execution_tree_impl, get_hot_methods_impl, find_service_names_impl
# Note: get_production_method_call_hierarchy_impl is disabled to avoid confusion with unified tree

async def quick_test():
    """Quick test with real data"""
    print("🚀 Quick MCP Tools Test")
    print("=" * 40)
    
    # Test parameters - modify these for your actual data
    service_name = "codetrails"
    class_name = "com.example.codetrails.orders.util.OrderUtil"
    method_name = None  # Set to specific method name or None for all methods
    
    print(f"Testing with:")
    print(f"  Service: {service_name}")
    print(f"  Class: {class_name}")
    print(f"  Method: {method_name or 'All methods'}")
    print()
    
    async with NexusClient() as client:
        try:
            # Test 0: Find Service Names (New!)
            print("0️⃣ SERVICE DISCOVERY TOOL")
            print("-" * 30)
            
            # Test service discovery with sample class names
            test_class_names = [
                "com.example.codetrails.orders.util.OrderUtil",
                "com.example.codetrails.orders.service.impl.OrderServiceImpl",
                "com.example.codetrails.orders.controller.OrderController",
                "com.example.codetrails.config.RequestLogFilter"
            ]
            
            service_discovery_result = await find_service_names_impl(
                client, test_class_names
            )
            print(service_discovery_result)
            
            print("\n" + "="*50 + "\n")
            
            # Test 1: Production Usage
            print("1️⃣ PRODUCTION USAGE TOOL")
            print("-" * 30)
            
            usage_result = await get_production_usage_impl(
                client, service_name, class_name, method_name, "1m"
            )
            print(usage_result)
            
            print("\n" + "="*50 + "\n")
            
            # Test 2: Production Call Flows (comprehensive flow analysis)
            print("2️⃣ PRODUCTION CALL FLOWS TOOL")
            print("-" * 30)
            
            unified_result = await get_unified_execution_tree_impl(
                client, service_name, class_name, method_name, "1m"
            )
            print(unified_result)
            
            print("\n" + "="*50 + "\n")
            
            # Test 3: Hot Methods
            print("3️⃣ HOT METHODS TOOL")
            print("-" * 30)
            
            hot_methods_result = await get_hot_methods_impl(
                client, service_name, "1m"
            )
            print(hot_methods_result)
            
        except Exception as e:
            print(f"❌ Error: {e}")
            print(f"Exception type: {type(e).__name__}")
            import traceback
            traceback.print_exc()

async def test_raw_api():
    """Test raw API responses to debug issues"""
    print("🔍 RAW API TEST")
    print("=" * 40)
    
    service_name = "codetrails"
    class_name = "com.example.codetrails.orders.util.OrderUtil"
    
    async with NexusClient() as client:
        try:
            print("0. Testing Find Service Names API...")
            test_class_names = [
                "com.example.codetrails.orders.util.OrderUtil",
                "com.example.codetrails.orders.controller.OrderController",
                "com.example.codetrails.config.RequestLogFilter"
            ]
            find_service_response = await client.find_service_names(test_class_names)
            service_names = find_service_response.get('serviceNames', [])
            available = find_service_response.get('available', False)
            print(f"✅ Find Service Names API: Available={available}, Found {len(service_names)} services")
            for svc in service_names[:3]:  # Show first 3 services
                print(f"   - Service: {svc}")
            
            print("\n1. Testing MPKS API...")
            mpks_response = await client.get_method_summary(service_name, class_name)
            print(f"✅ MPKS API: {len(mpks_response)} methods found")
            for method in mpks_response[:2]:  # Show first 2 methods
                print(f"   - {method.get('methodNameOnly', 'Unknown')}: QPS={method.get('qps', 0)}")
            
            print("\n2. Testing Flows API...")
            flows_response = await client.get_method_flows(service_name, class_name)
            print(f"✅ Flows API: {len(flows_response)} methods with flows")
            
            # Collect some flow IDs
            flow_ids = []
            for method_data in flows_response:
                method_flow_ids = method_data.get("flowIds", [])
                if method_flow_ids:
                    flow_ids.extend(method_flow_ids[:2])
            
            if flow_ids:
                print(f"\n3. Testing Flow Details API with {len(flow_ids[:3])} flows...")
                flow_details = await client.get_multiple_flow_details(service_name, flow_ids[:3])
                print(f"✅ Flow Details API: {len(flow_details)} flow trees received")
                print(f"   Flow IDs: {list(flow_details.keys())}")
            else:
                print("\n3. No flows found for Flow Details API test")
            
            print("\n4. Testing Hot Methods API...")
            hot_methods_response = await client.get_hot_methods(service_name)
            print(f"✅ Hot Methods API: {len(hot_methods_response)} hot methods found")
            for hot_method in hot_methods_response[:3]:  # Show first 3 hot methods
                class_name = hot_method.get('className', 'Unknown')
                method_name = hot_method.get('methodNameOnly', 'Unknown')
                cpu_percent = hot_method.get('cpuUtilizationPercent', 0)
                simple_class = class_name.split('.')[-1] if class_name else 'Unknown'
                print(f"   - {simple_class}.{method_name}: CPU={cpu_percent:.3f}%")
                
        except Exception as e:
            print(f"❌ Raw API Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--raw":
        print("Running raw API test...\n")
        asyncio.run(test_raw_api())
    else:
        print("Running quick tool test...\n")
        print("💡 Use --raw flag to test raw API responses\n")
        asyncio.run(quick_test())