"""
FastMCP Server for mediastack News API - HTTP version for Smithery deployment
"""
import os
import sys
from app import mcp



if __name__ == "__main__":
    # Get configuration from environment
    api_key = os.getenv("MEDIASTACK_API_KEY")
    if api_key:
        print(f"Using API key: {api_key[:10]}...")
    else:
        print("No API key found - will validate on tool execution (lazy loading)")
    
    # Get port from environment (Smithery sets this)
    port = int(os.getenv("PORT", "8003"))
    
    print(f"Starting Mediastack MCP Server on port {port}...")
    print("Server is running in HTTP mode for Smithery deployment")
    print(f"MCP endpoint will be available at: http://0.0.0.0:{port}/mcp")
    
    
    try:
        # Start FastMCP with built-in HTTP server
        # This will automatically create the /mcp endpoint that Smithery expects
        mcp.run(
            transport="http",
            host="0.0.0.0",
            port=port,
            path="/mcp"
        )
    except (OSError, RuntimeError) as e:
        print(f"Server startup failed: {e}")
        sys.exit(1)
    