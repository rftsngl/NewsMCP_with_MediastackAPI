"""
FastMCP Server for mediastack News API
"""
from app import mcp

if __name__ == "__main__":
    # Start the FastMCP server using stdio transport
    # MCP servers communicate via stdin/stdout, not HTTP
    print("Starting Mediastack MCP Server...")
    print("Server is using stdio transport (stdin/stdout)")
    print("Press Ctrl+C to stop the server")
    
    # Run the server - it will communicate via stdio
    mcp.run()
    