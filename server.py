"""
FastMCP Server for mediastack News API - HTTP version for Smithery deployment
"""
import os
import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from app import mcp
import json
from typing import Dict, Any

# Create FastAPI app
app = FastAPI(title="Mediastack MCP Server")

def parse_config_from_query(query_params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse Smithery configuration from query parameters using dot-notation
    Example: ?MEDIASTACK_API_KEY=abc123 -> {"MEDIASTACK_API_KEY": "abc123"}
    """
    config = {}
    for key, value in query_params.items():
        # Handle dot-notation for nested properties
        keys = key.split('.')
        current = config
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        current[keys[-1]] = value
    return config

@app.get("/mcp")
async def mcp_get(request: Request):
    """
    Handle GET requests to /mcp endpoint for tool discovery
    This is where lazy loading is crucial - no API validation here
    """
    try:
        # Parse configuration from query parameters
        config = parse_config_from_query(dict(request.query_params))
        
        # Set environment variables from config if provided
        if "MEDIASTACK_API_KEY" in config:
            os.environ["MEDIASTACK_API_KEY"] = config["MEDIASTACK_API_KEY"]
        
        # Get tools list without validating API key (lazy loading)
        tools_response = await mcp.handle_request({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {}
        })
        
        return JSONResponse(content=tools_response)
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Failed to get tools: {str(e)}"}
        )

@app.post("/mcp")
async def mcp_post(request: Request):
    """
    Handle POST requests to /mcp endpoint for tool execution
    """
    try:
        # Parse configuration from query parameters
        config = parse_config_from_query(dict(request.query_params))
        
        # Set environment variables from config
        if "MEDIASTACK_API_KEY" in config:
            os.environ["MEDIASTACK_API_KEY"] = config["MEDIASTACK_API_KEY"]
        
        # Get request body
        body = await request.json()
        
        # Handle the MCP request
        response = await mcp.handle_request(body)
        
        return JSONResponse(content=response)
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"MCP request failed: {str(e)}"}
        )

@app.delete("/mcp")
async def mcp_delete():
    """
    Handle DELETE requests to /mcp endpoint
    """
    return JSONResponse(content={"status": "ok"})

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy", "service": "Mediastack MCP Server"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print(f"Starting Mediastack MCP Server on port {port}...")
    print("Server is running in HTTP mode for Smithery deployment")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=port,
        log_level="info"
    )
    