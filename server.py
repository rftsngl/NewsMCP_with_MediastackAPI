"""
FastMCP Server for mediastack News API - HTTP version for Smithery deployment
"""
import os
import asyncio
import signal
import sys
from app import mcp

async def shutdown_handler():
    """Graceful shutdown handler"""
    print("Shutting down server...")
    sys.exit(0)

if __name__ == "__main__":
    # Get configuration from environment
    api_key = os.getenv("MEDIASTACK_API_KEY")
    if api_key:
        print(f"Using API key: {api_key[:10]}...")
    else:
        print("No API key found - will validate on tool execution (lazy loading)")
    
    # Get port from environment (Smithery sets this)
    port = int(os.getenv("PORT", 8000))
    
    print(f"Starting Mediastack MCP Server on port {port}...")
    print("Server is running in HTTP mode for Smithery deployment")
    print(f"MCP endpoint will be available at: http://0.0.0.0:{port}/mcp")
    
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, lambda s, f: asyncio.create_task(shutdown_handler()))
    signal.signal(signal.SIGTERM, lambda s, f: asyncio.create_task(shutdown_handler()))
    
    try:
        # Start FastMCP with built-in HTTP server and optimized settings
        # This will automatically create the /mcp endpoint that Smithery expects
        mcp.run(
            transport="http",
            host="0.0.0.0",
            port=port,
            path="/mcp",
            # Add timeout configurations
            timeout=30,
            max_message_size=1024*1024  # 1MB
        )
    except Exception as e:
        print(f"Server startup failed: {e}")
        sys.exit(1)
    