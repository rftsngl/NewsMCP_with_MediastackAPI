"""
Ultra-Minimal FastMCP Server - Template Style
"""
import os
import sys

# Import app
try:
    from app import mcp
except ImportError as e:
    print(f"Error importing app: {e}")
    sys.exit(1)

if __name__ == "__main__":
    # Simple environment setup
    port = int(os.getenv("PORT", "8000"))
    
    print(f"Starting MCP Server on port {port}...")
    
    try:
        # Ultra-simple FastMCP run - let it handle everything
        mcp.run(
            transport="http",
            host="0.0.0.0", 
            port=port
        )
    except (RuntimeError, KeyboardInterrupt, SystemExit) as e:
        # The server may raise various runtime errors; catching all ensures graceful shutdown.
        print(f"Server error: {e}")
        sys.exit(1)
