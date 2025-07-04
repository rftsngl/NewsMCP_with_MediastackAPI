"""
Ultra-Minimal FastMCP Server - Template Style
"""
import os
import sys
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse, Response
from starlette.routing import Route
import uvicorn

# Import app
try:
    from app import mcp
except ImportError as e:
    print(f"Error importing app: {e}")
    sys.exit(1)

async def mcp_handler(request):
    """Handle MCP requests on /mcp endpoint"""
    method = request.method
    
    if method == "GET":
        # Return tools list for discovery - no auth required
        try:
            tools = []
            # Try to get tools from FastMCP instance
            if hasattr(mcp, '_tools'):
                for tool_name, tool_func in mcp._tools.items():
                    tools.append({
                        "name": tool_name,
                        "description": getattr(tool_func, "__doc__", "") or "No description",
                        "inputSchema": {
                            "type": "object",
                            "properties": {},
                            "required": []
                        }
                    })
            else:
                # Fallback - just return some basic info
                tools = [
                    {
                        "name": "get_latest_news",
                        "description": "Fetches the most recent news stories from mediastack",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "keywords": {"type": "string", "description": "Search terms to filter news"}
                            }
                        }
                    },
                    {
                        "name": "get_sources",
                        "description": "List available news sources from mediastack",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "search": {"type": "string", "description": "Search term to filter sources"}
                            }
                        }
                    }
                ]
            
            return JSONResponse({"tools": tools})
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
    
    elif method in ["POST", "DELETE"]:
        # Handle actual MCP protocol calls
        # This would need proper MCP protocol implementation
        return JSONResponse({"message": "MCP protocol handler"})
    
    else:
        return Response(status_code=405)

# Create Starlette app with MCP endpoint
app = Starlette(
    routes=[
        Route("/mcp", mcp_handler, methods=["GET", "POST", "DELETE"]),
    ]
)

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    # Simple environment setup
    port = int(os.getenv("PORT", "8000"))
    
    print(f"Starting MCP Server on port {port}...")
    print(f"MCP endpoint available at: http://localhost:{port}/mcp")
    
    try:
        uvicorn.run(app, host="0.0.0.0", port=port)
    except (RuntimeError, KeyboardInterrupt, SystemExit) as e:
        # The server may raise various runtime errors; catching all ensures graceful shutdown.
        print(f"Server error: {e}")
        sys.exit(1)
