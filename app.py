"""
Ultra-Minimal MCP Tools - Template Style
"""
import os
import asyncio
from typing import Optional, Dict, Any

import requests
from fastmcp import FastMCP
from dotenv import load_dotenv

# Initialize FastMCP
mcp = FastMCP("Mediastack News MCP Server")

def get_api_key() -> str:
    """Get API key from environment"""
    load_dotenv()
    api_key = os.getenv("MEDIASTACK_API_KEY")
    if not api_key:
        raise ValueError("MEDIASTACK_API_KEY environment variable is required")
    return api_key

async def make_api_request(endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Make API request to mediastack"""
    # Add API key
    params['access_key'] = get_api_key()
    
    # Clean params
    params = {k: v for k, v in params.items() if v is not None}
    
    # Make request
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(
        None,
        lambda: requests.get(f"https://api.mediastack.com/v1/{endpoint}", params=params, timeout=15)
    )
    response.raise_for_status()
    return response.json()

@mcp.tool()
async def get_latest_news(
    keywords: Optional[str] = None,
    sources: Optional[str] = None,
    countries: Optional[str] = None,
    languages: Optional[str] = None,
    categories: Optional[str] = None,
    date: Optional[str] = None,
    sort: Optional[str] = None,
    limit: Optional[int] = 25,
    offset: Optional[int] = None
) -> Dict[str, Any]:
    """
    Fetches the most recent news stories from mediastack.
    
    Args:
        keywords: Search terms to filter news
        sources: News sources, comma-separated
        countries: Country codes, comma-separated
        languages: Language codes, comma-separated
        categories: News categories, comma-separated
        date: Date or date range (YYYY-MM-DD)
        sort: Sort order (published_desc, published_asc, popularity)
        limit: Maximum results (1-100), default 25
        offset: Pagination offset, default 0
    
    Returns:
        JSON response from mediastack API
    """
    # Validate limit
    if limit is not None:
        limit = min(max(1, limit), 100)
    
    params = {
        "keywords": keywords,
        "sources": sources,
        "countries": countries,
        "languages": languages,
        "categories": categories,
        "date": date,
        "sort": sort,
        "limit": limit,
        "offset": offset
    }
    
    return await make_api_request("news", params)

@mcp.tool()
async def get_sources(
    search: Optional[str] = None,
    sources: Optional[str] = None,
    countries: Optional[str] = None,
    languages: Optional[str] = None,
    categories: Optional[str] = None,
    limit: Optional[int] = 25,
    offset: Optional[int] = None
) -> Dict[str, Any]:
    """
    List available news sources from mediastack.
    
    Args:
        search: Search term to filter sources
        sources: Specific sources, comma-separated
        countries: Country codes, comma-separated
        languages: Language codes, comma-separated
        categories: News categories, comma-separated
        limit: Maximum results (1-100), default 25
        offset: Pagination offset, default 0
    
    Returns:
        JSON response from mediastack API
    """
    # Validate limit
    if limit is not None:
        limit = min(max(1, limit), 100)
    
    params = {
        "search": search,
        "sources": sources,
        "countries": countries,
        "languages": languages,
        "categories": categories,
        "limit": limit,
        "offset": offset
    }
    
    return await make_api_request("sources", params)
