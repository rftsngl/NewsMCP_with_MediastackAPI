"""
FastMCP Server for mediastack News API - HTTP version for Smithery deployment
"""
import os
import sys
import logging
import locale

# Set UTF-8 encoding to prevent Windows issues
if sys.platform == 'win32':
    # Force UTF-8 encoding on Windows
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    # Set locale to handle encoding issues
    try:
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_ALL, 'C.UTF-8')
        except locale.Error:
            pass  # Use default locale

# Configure logging
logging.basicConfig(level=logging.INFO, encoding='utf-8')
logger = logging.getLogger(__name__)

# Import app after setting encoding
try:
    from app import mcp
except (ImportError, ModuleNotFoundError, SyntaxError) as e:
    logger.error("Failed to import app: %s", e)
    logger.error("This might be due to encoding issues or missing dependencies")
    sys.exit(1)

if __name__ == "__main__":
    # Get configuration from environment - but don't validate API key at startup
    api_key = os.getenv("MEDIASTACK_API_KEY", "").strip()
    if api_key:
        logger.info("API key configured (starts with: %s...)", api_key[:8])
    else:
        logger.warning("No API key found - will validate on tool execution (lazy loading)")
    
    # Get port from environment (Smithery sets this)
    try:
        port = int(os.getenv("PORT", "8003"))
    except ValueError:
        logger.error("Invalid PORT environment variable")
        port = 8003
    
    logger.info("Starting Mediastack MCP Server on port %s...", port)
    logger.info("Server is running in HTTP mode for Smithery deployment")
    logger.info("MCP endpoint will be available at: http://0.0.0.0:%s/mcp", port)
    
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
        logger.error("Server startup failed: %s", e)
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        sys.exit(0)
    except (ValueError, TypeError, AttributeError) as e:
        logger.error("Unexpected error: %s", e)
        sys.exit(1)
