# CodeKarma MCP Server

A **Model Context Protocol (MCP)** server that provides production insights and code analysis capabilities using your Nexus instrumentation data. Analyze real production flows, identify hot methods, generate test cases, and make data-driven decisions about your code.

## ⚡ Quick Start Reference

**🏠 Local Setup (Development)**
```bash
./setup.sh                    # Install dependencies & setup venv
python3 quick_test.py         # Test all tools with real data
./run_server.sh               # Start local server (stdio)
```

**🌐 Remote Setup (Docker)**
```bash
cp env-example .env           # Copy environment template
./restart-server.sh           # Build & start Docker container
./generate-config.sh          # Generate client config (interactive)
./test-mcp-server.sh          # Test remote server via HTTP
```

**🔧 Quick Commands**
- `./restart-server.sh` - Restart Docker container
- `./generate-config.sh` - Create MCP client configs (Direct or nginx proxy)
- `python3 quick_test.py` - Test all 4 tools locally
- `curl http://localhost:8547/health` - Check Docker server health

---

## 🚀 Deployment Options

### **🏠 Local Server** (Original)
- Direct Python execution
- Uses stdio transport  
- For local development and testing

### **🌐 Remote Server** (New!)
- HTTP/JSON-RPC transport with flexible authentication
- Docker containerized  
- For shared team access and production use
- **Port**: 8547 (non-common port)
- **Authentication**: Two models supported:
  - **Direct**: ck-domain header (no auth needed)
  - **nginx Proxy**: Bearer token (nginx validates and adds ck-domain)

## 🚀 Features

- **🔥 Hot Method Detection** - Identify CPU-intensive methods above configurable thresholds  
- **📊 Production Usage Analysis** - Get real-time insights about method execution patterns
- **🌳 Flow Tree Visualization** - View individual and aggregated execution flow trees
- **⚡ Performance Optimization** - Get CPU utilization insights and optimization recommendations
- **🎯 Data-Driven Development** - Make code changes based on real production usage

## 📋 Prerequisites

- **Python 3.8+**
- **Nexus service** running on `http://localhost:8081`
- **Instrumented Java application** with production flow data

## ⚡ Quick Start

### 🏠 Local Server Setup

#### 1. **Setup** (One Command)
```bash
git clone <your-repo>
cd ck-mcp-server
./setup.sh
```

#### 2. **Test the Server**
```bash
python3 quick_test.py
```

#### 3. **Configure Claude Desktop**
Add this to your Claude Desktop `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "nexus": {
      "command": "python3",
      "args": ["/absolute/path/to/ck-mcp-server/server.py"],
      "env": {}
    }
  }
}
```

#### 4. **Start Using**
```bash
./run_server.sh
```

### 🌐 Remote Server Setup (Recommended for Teams)

#### 1. **Deploy with Docker**
```bash
# Copy environment template
cp env-example .env
# Edit .env with your Nexus endpoint if needed

# Start the server
docker-compose up -d --build

# Or use the simple restart script
./restart-server.sh
```

#### 2. **Generate Client Configuration**
```bash
# Interactive configuration generator
./generate-config.sh
```

**Two Connection Models:**
1. **Direct Connection**: Uses ck-domain header, connects directly to MCP server (port 8547)
2. **nginx Proxy**: Uses Bearer token, connects through nginx (nginx validates token and adds ck-domain)

**Options:**
- **Connection Type**: Choose Direct or nginx Proxy  
- **Client Type**: Choose Windsurf or Claude Desktop/Cursor
- **Domain Examples**: test, production, staging, or custom

**Script will output ready-to-use JSON config** for your specific deployment!

#### 3. **Verify Connection**
```bash
# Health check
curl http://localhost:8547/health

# Test with domain header
curl -X POST http://localhost:8547/mcp \
  -H "Content-Type: application/json" \
  -H "ck-domain: test" \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}'
```

## 🛠️ Available Tools

### 1. **`find_service_names`** 🔍
Find service names from a list of class names visible in your IDE. This tool helps discover which services contain the specified classes when the service name is unknown.

**Parameters:**
- `class_names` (required): Array of fully qualified class names (e.g., `['com.example.service.UserService', 'com.example.util.DatabaseUtil']`)

**Usage:**
- When you don't know the service name but have class names from your IDE
- Provide 10-20 class names for optimal matching accuracy
- If multiple services are found, the tool will prompt you to ask the user which service to analyze
- Use discovered service names with other production analysis tools

**Example Workflows:**

**Single Service Found:**
```
1. "Find services for these classes: com.example.UserService, com.example.OrderController"
2. → Returns: ["my-microservice"] 
3. "Analyze production usage for my-microservice"
```

**Multiple Services Found:**
```
1. "Find services for these classes: com.example.UserService, com.example.OrderController" 
2. → Returns: ["my-microservice", "order-service", "user-service"]
3. → LLM asks: "I found 3 services... Which service would you like to analyze?"
4. User responds: "Let's analyze my-microservice"
5. "Analyze production usage for my-microservice"
```

### 2. **`get_production_usage`**
Get production usage information for methods including throughput and activity status.

**Parameters:**
- `service_name` (required): Name of the service (e.g., 'codetrails')
- `class_name` (required): Full class name
- `method_name` (optional): Specific method name
- `step` (optional): Time window (default: '1m')

### 3. **`get_production_call_flows`**
Analyze production method call patterns and flows with aggregated performance metrics and hot method annotations.

**Parameters:**
- `service_name` (required): Name of the service
- `class_name` (required): Full class name
- `method_name` (optional): Specific method name
- `step` (optional): Time window (default: '1m')

### 4. **`get_hot_methods`** 🔥
Get details about hot methods that have high CPU utilization in production (above 1% CPU threshold).

**Parameters:**
- `service_name` (required): Name of the service
- `step` (optional): Time window (default: '1m')

## 💡 Usage Examples

### Service Discovery (New!)
```
"I can see these classes in my IDE: UserService, OrderController, PaymentService, DatabaseUtil. Which services do they belong to?"
```
- Automatically discovers service names from class names
- No need to manually know service names
- Sets up other tools for further analysis

### Complete Workflow (Unknown Service)
```
1. "Find services for: com.example.UserService, com.example.OrderController"
2. "Analyze production usage for [discovered-service] UserService class"
3. "Show hot methods in [discovered-service]"
```
- Start with class names from your IDE
- Discover services automatically
- Dive into production analysis

### Hot Method Analysis
```
"Show me all hot methods in the codetrails service"
```
- Identifies CPU-intensive methods
- Shows CPU utilization percentages  
- Provides optimization recommendations

### Production Flow Analysis
```
"Analyze the production usage for OrderUtil class in codetrails service"
```
- Shows QPS, error rates, latency for each method
- Identifies active vs inactive methods
- Highlights HTTP endpoints

### Execution Tree Visualization
```
"Show me the call flows for OrderController in codetrails"
```
- Displays aggregated flow trees
- Shows CPU annotations for hot methods (🔥)
- Includes flow IDs and metrics

### Combined Analysis
```
"Get the call flows for OrderUtil and highlight any hot methods"
```
- Shows comprehensive flow analysis
- Annotates hot methods with CPU utilization
- Provides context about flow patterns

## 🎯 Key Features in Detail

### **🔥 Hot Method Detection**
- **CPU Threshold**: Automatically detects methods above 1% CPU utilization
- **Performance Impact**: Shows actual CPU consumption percentages
- **Optimization Targeting**: Prioritizes optimization efforts on high-impact methods
- **Visual Indicators**: Hot methods marked with 🔥 in flow trees

### **📊 Flow Tree Annotations**
- **Individual Flows**: Shows hot methods in each execution path
- **Unified Trees**: Aggregates CPU data across all flows
- **Visual Clarity**: `CPU: X.XX% 🔥` annotations in tree output
- **Context Aware**: Matches methods by className + methodName

### **⚡ Production Insights**  
- **Real-time Data**: Live production metrics from Nexus
- **HTTP Endpoints**: Shows which endpoints trigger hot methods
- **Error Correlation**: Combines CPU usage with error rates
- **Throughput Analysis**: QPS/QPM data alongside CPU metrics

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Claude UI     │────│   MCP Server     │────│   Nexus API     │
│                 │    │                  │    │                 │
│ Natural Lang    │    │ - Tool Handlers  │    │ - Flow Data     │
│ Queries         │    │ - Hot Methods    │    │ - CPU Metrics   │
│                 │    │ - Tree Builders  │    │ - Production    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

**Components:**
- **NexusClient**: Async HTTP client for Nexus API calls
- **Hot Methods Engine**: CPU threshold detection and annotation
- **Tree Builders**: Flow tree construction and visualization
- **Analysis Functions**: Production usage insights and recommendations

## 🧪 Testing

### **Local Testing**
```bash
# Test all tools with real API
python3 quick_test.py

# Test raw APIs only  
python3 quick_test.py --raw
```

### **What Gets Tested:**
- ✅ All 4 MCP tools (service discovery, usage analysis, call flows, hot methods)
- ✅ Raw Nexus API connectivity (find-service-name, mpks, flows, flow-details, hot-methods)
- ✅ Service discovery from class names
- ✅ Hot method detection and annotation
- ✅ Real production data integration

### **Sample Test Output:**
```markdown
🚀 Quick MCP Tools Test
==========================================

0️⃣ SERVICE DISCOVERY TOOL
------------------------------

# Service Name Discovery

## Input Classes (4)
1. `OrderUtil` (Full: `com.example.codetrails.orders.util.OrderUtil`)
2. `OrderServiceImpl` (Full: `com.example.codetrails.orders.service.impl.OrderServiceImpl`)
3. `OrderController` (Full: `com.example.codetrails.orders.controller.OrderController`)
4. `RequestLogFilter` (Full: `com.example.codetrails.config.RequestLogFilter`)

## Discovery Results
✅ **Service Names Found:** 1 matching service(s)
**Domain:** test

### Matching Services:
1. `codetrails`

### Next Steps
You can now use these service name(s) with other production analysis tools:
- `get_production_usage(service_name="codetrails", class_name="...")`
- `get_production_call_flows(service_name="codetrails", class_name="...")`
- `get_hot_methods(service_name="codetrails")`

==================================================

3️⃣ HOT METHODS TOOL
------------------------------

# Hot Methods Report
**Service:** codetrails
**CPU Threshold:** ≥ 1.0%

## Hot Methods Found (1)

### 1. `OrderServiceImpl.compareCharactersExpensively` 🔥
**CPU Utilization:** 1.611%
**Throughput (QPS):** 1,723,283.72
**Optimization Target:** Primary candidate for performance improvement
```

## 📁 Project Structure

```
ck-mcp-server/
├── server.py                   # Local MCP server (stdio)
├── remote_server.py            # Remote MCP server (HTTP/JSON-RPC)
├── quick_test.py               # Comprehensive testing script  
├── setup.sh                    # One-command local setup
├── restart-server.sh           # Simple Docker container restart
├── test-mcp-server.sh          # Remote server testing script
├── run_server.sh               # Local server runner  
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker image configuration
├── docker-compose.yml          # Docker Compose setup
├── .dockerignore              # Docker build exclusions
├── env-example                 # Environment variables template
├── mcp-config.json            # Local MCP configuration (uses env vars)
├── generate-config.sh         # Interactive MCP client config generator
├── README.md                   # This documentation
└── nexus-api.md               # API reference
```

**Key Configuration Files:**
- **`mcp-config.json`**: For local server (Claude Desktop) - sets `CK_NEXUS_ENDPOINT` env var
- **`generate-config.sh`**: Interactive script to generate remote MCP client configs
- **`.env`**: Docker Compose environment variables

## 🔧 Configuration

### **Logging Level**
Control the verbosity of server logs using the `LOG_LEVEL` environment variable:

**Available Levels:** DEBUG, INFO, WARNING, ERROR, CRITICAL

**Default:** INFO (shows INFO, WARNING, ERROR, CRITICAL)

**To see debug logs:**
```bash
# For Docker/remote server - add to .env file:
LOG_LEVEL=DEBUG

# For local server:
export LOG_LEVEL=DEBUG
./run_server.sh
```

**What each level shows:**
- `DEBUG`: All logs including debug messages (most verbose)
- `INFO`: Informational messages and above (default)
- `WARNING`: Warning messages and above
- `ERROR`: Error messages only
- `CRITICAL`: Critical errors only

### **Domain-Based Routing**
The server uses the `ck-domain` header to determine which Nexus API path to use:

**Generate MCP Client Configuration:**
```bash
# Use the interactive generator
./generate-config.sh

# Example output for direct connection:
{
  "mcpServers": {
    "codekarma-insights": {
      "url": "http://localhost:8547/mcp",
      "headers": {
        "ck-domain": "production"  // ← Direct to MCP server
      }
    }
  }
}

# Example output for nginx proxy:
{
  "mcpServers": {
    "codekarma-insights": {
      "url": "https://nginx-proxy.com/mcp",
      "headers": {
        "Authorization": "Bearer mcp_xxx"  // ← nginx validates this
      }
    }
  }
}
```

**Domain → API Path Mapping:**
- `ck-domain: "test"` → Nexus calls to `/test/api/method-graph-paths/...`
- `ck-domain: "production"` → Nexus calls to `/production/api/method-graph-paths/...`
- `ck-domain: "staging"` → Nexus calls to `/staging/api/method-graph-paths/...`

### **Nexus Connection**
Default: AWS ELB endpoint (see `server.py`)

**Recommended:** Set via environment variable:
```bash
export CK_NEXUS_ENDPOINT="http://your-nexus-server:8081"
```

**Docker/Kubernetes:**
```yaml
# In your .env file or Helm values
CK_NEXUS_ENDPOINT=http://your-nexus-server:8081
```

**Alternative:** Modify directly in `server.py`:
```python
class NexusClient:
    def __init__(self, base_url: str = "http://your-nexus:8081"):
```

### **CPU Threshold**  
Default: 1.0% for hot method detection

To change, modify in `server.py`:
```python
hot_methods = await client.get_hot_methods(service_name, cpu_threshold=2.0)
```

## 🐛 Troubleshooting

### **Connection Issues**
```
❌ Error: Connection refused
```
**Solution:** Ensure Nexus is running on localhost:8081

### **No Hot Methods Found**
```
No hot methods found (no methods exceed 1% CPU utilization threshold)
```
**Solution:** Check that your application has CPU-intensive operations or lower the threshold

### **Empty Flow Trees**
```
No production data found for ClassName
```
**Solution:** Verify class name exists and has production traffic

### **Missing CPU Annotations**
```
Flow trees show but no 🔥 indicators
```
**Solution:** Ensure hot methods API is working: `curl http://localhost:8081/{domain}/api/method-graph-paths/hot-methods?serviceName=yourservice&cpuThreshold=1`

## 🚀 Next Steps

1. **Deploy to Production**: Use with your production Nexus instance
2. **Custom Thresholds**: Adjust CPU thresholds for your environment  
3. **Integration**: Add to CI/CD pipelines for performance monitoring
4. **Optimization**: Use hot method data to prioritize performance improvements
5. **Monitoring**: Set up alerts for new hot methods in production

## 🤝 Contributing

1. **Add New Tools**: Extend `handle_list_tools()` and `handle_call_tool()`
2. **Enhance Analysis**: Add new metrics and insights to existing tools
3. **Improve Visualization**: Enhance tree rendering and annotations
4. **Testing**: Add test cases to `quick_test.py`

## 📊 API Endpoints Used

The server integrates with these Nexus endpoints (domain dynamically set via `ck-domain` header):
- `POST /{domain}/api/method-graph-paths/find-service-name` - Service discovery from class names
- `GET /{domain}/api/method-graph-paths/mpks` - Method summary with profiling info
- `GET /{domain}/api/method-graph-paths/flows` - Flow IDs for methods  
- `GET /{domain}/api/method-graph-paths/flow-details` - Detailed flow trees
- `GET /{domain}/api/method-graph-paths/hot-methods` - CPU-intensive methods

**Examples:**
- With `ck-domain: test` → `/test/api/method-graph-paths/mpks`
- With `ck-domain: production` → `/production/api/method-graph-paths/mpks`

---

**🔥 Ready to optimize your production code with data-driven insights!** 

Start by running `./setup.sh` and then `python3 quick_test.py` to see your hot methods in action.