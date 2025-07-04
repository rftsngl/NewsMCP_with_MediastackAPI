"""
JSON-RPC 2.0 Uyumlu MCP Server
"""
import os
import sys
import json
import inspect
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.routing import Route
import uvicorn

# Import app
try:
    from app import mcp
except ImportError as e:
    print(f"Error importing app: {e}")
    sys.exit(1)

def create_jsonrpc_response(result=None, error=None, request_id=None):
    """JSON-RPC 2.0 uyumlu response oluştur"""
    response = {
        "jsonrpc": "2.0",
        "id": request_id
    }
    
    if error:
        response["error"] = {
            "code": error.get("code", -32000),
            "message": error.get("message", "Internal error"),
            "data": error.get("data")
        }
    else:
        response["result"] = result
    
    return response

def parse_jsonrpc_request(body):
    """JSON-RPC 2.0 request'ini parse et"""
    try:
        request = json.loads(body)
    except json.JSONDecodeError:
        return None, {"code": -32700, "message": "Parse error"}
    
    # JSON-RPC 2.0 validation
    if request.get("jsonrpc") != "2.0":
        return None, {"code": -32600, "message": "Invalid Request"}
    
    if "method" not in request:
        return None, {"code": -32600, "message": "Invalid Request"}
    
    return request, None

def get_tool_schema(tool_func):
    """Tool'un schema'sını çıkar"""
    # Signature'dan parametreleri al
    sig = inspect.signature(tool_func)
    properties = {}
    required = []
    
    for param_name, param in sig.parameters.items():
        if param_name == 'self':
            continue
            
        properties[param_name] = {
            "type": "string",  # Basit bir varsayım
            "description": f"Parameter {param_name}"
        }
        
        # Required parametreler (default value olmayan)
        if param.default == inspect.Parameter.empty:
            required.append(param_name)
    
    return {
        "type": "object",
        "properties": properties,
        "required": required
    }

async def handle_tools_list(request_id):
    """tools/list metodunu handle et"""
    tools = []
    
    # FastMCP instance'ından tool'ları al
    try:
        fastmcp_tools = await mcp.get_tools()
        # fastmcp_tools bir dict, values() ile tool'ları al
        for tool in fastmcp_tools.values():
            # to_mcp_tool() metodunu kullan - bu MCP formatına dönüştürür
            mcp_tool = tool.to_mcp_tool()
            tools.append({
                "name": mcp_tool.name,
                "description": mcp_tool.description or f"Tool: {mcp_tool.name}",
                "inputSchema": mcp_tool.inputSchema or {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            })
    except Exception as e:
        print(f"Error getting tools: {e}")
        import traceback
        traceback.print_exc()
    
    return create_jsonrpc_response(
        result={"tools": tools},
        request_id=request_id
    )

async def handle_tools_call(params, request_id):
    """tools/call metodunu handle et"""
    tool_name = params.get("name")
    arguments = params.get("arguments", {})
    
    if not tool_name:
        return create_jsonrpc_response(
            error={"code": -32602, "message": "Invalid params: missing tool name"},
            request_id=request_id
        )
    
    # Tool'u bul ve çağır
    try:
        fastmcp_tools = await mcp.get_tools()
        if tool_name in fastmcp_tools:
            tool_func = fastmcp_tools[tool_name]
            # Tool'u çağır
            result = await tool_func(**arguments)
            
            return create_jsonrpc_response(
                result={"content": [{"type": "text", "text": str(result)}]},
                request_id=request_id
            )
        else:
            return create_jsonrpc_response(
                error={"code": -32601, "message": f"Tool not found: {tool_name}"},
                request_id=request_id
            )
    except Exception as e:
        return create_jsonrpc_response(
            error={"code": -32603, "message": f"Tool execution failed: {str(e)}"},
            request_id=request_id
        )

async def handle_initialize(params, request_id):
    """initialize metodunu handle et"""
    return create_jsonrpc_response(
        result={
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {}
            },
            "serverInfo": {
                "name": "Mediastack News MCP Server",
                "version": "1.0.0"
            }
        },
        request_id=request_id
    )

async def handle_ping(request_id):
    """ping metodunu handle et - server'ın canlı olduğunu gösterir"""
    return create_jsonrpc_response(
        result={"status": "pong"},
        request_id=request_id
    )

async def mcp_handler(request):
    """MCP JSON-RPC 2.0 handler"""
    if request.method == "POST":
        body = await request.body()
        
        # JSON-RPC request'ini parse et
        json_request, error = parse_jsonrpc_request(body.decode())
        
        if error:
            return JSONResponse(
                create_jsonrpc_response(error=error, request_id=None),
                status_code=400
            )
        
        method = json_request.get("method")
        params = json_request.get("params", {})
        request_id = json_request.get("id")
        
        # Method'a göre handle et
        if method == "tools/list":
            response = await handle_tools_list(request_id)
        elif method == "tools/call":
            response = await handle_tools_call(params, request_id)
        elif method == "initialize":
            response = await handle_initialize(params, request_id)
        elif method == "ping":
            response = await handle_ping(request_id)
        else:
            response = create_jsonrpc_response(
                error={"code": -32601, "message": f"Method not found: {method}"},
                request_id=request_id
            )
        
        return JSONResponse(response)
    
    elif request.method == "GET":
        # Basit health check
        return JSONResponse({
            "status": "ok", 
            "server": "Mediastack News MCP Server",
            "endpoints": ["/mcp"]
        })
    
    else:
        return JSONResponse({"error": "Method not allowed"}, status_code=405)

# Starlette app
app = Starlette(
    routes=[
        Route("/mcp", mcp_handler, methods=["GET", "POST"]),
    ]
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    
    print(f"Starting JSON-RPC 2.0 MCP Server on port {port}...")
    print(f"MCP endpoint available at: http://localhost:{port}/mcp")
    
    # Tool'ları kontrol et
    async def check_tools():
        try:
            tools = await mcp.get_tools()
            print(f"Tools available: {list(tools.keys())}")
            return len(tools)
        except Exception as e:
            print(f"Error checking tools: {e}")
            return 0
    
    # Async kontrol
    import asyncio
    try:
        tool_count = asyncio.run(check_tools())
        print(f"Server ready with {tool_count} tools")
    except Exception as e:
        print(f"Startup error: {e}")
    
    try:
        uvicorn.run(app, host="0.0.0.0", port=port)
    except (RuntimeError, KeyboardInterrupt, SystemExit) as e:
        print(f"Server error: {e}")
        sys.exit(1)
