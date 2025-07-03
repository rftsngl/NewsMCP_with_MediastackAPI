"""
MCP Tools for mediastack News API
"""
import os
import asyncio
from typing import Optional, Dict, Any

import requests
from fastmcp import FastMCP

# Initialize FastMCP
mcp = FastMCP("Mediastack News MCP Server")

# API Configuration - Lazy loaded
MEDIASTACK_BASE_URL = "https://api.mediastack.com/v1"

def get_api_key() -> str:
    """
    Get API key lazily - only when actually needed for API calls
    """
    api_key = os.getenv("MEDIASTACK_API_KEY")
    if not api_key:
        raise ValueError("MEDIASTACK_API_KEY environment variable is required")
    return api_key

# Helper function for API calls
async def make_mediastack_request(endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Make a request to mediastack API with error handling
    """
    # Get API key only when making actual API calls (lazy loading)
    try:
        api_key = get_api_key()
    except Exception as e:
        raise RuntimeError(f"Configuration Error: {str(e)}") from e
    
    # Add API key to params
    params['access_key'] = api_key
    
    # Remove None values from params
    params = {k: v for k, v in params.items() if v is not None}
    
    try:
        # Run requests in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        
        # Add session configuration for better performance
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'MediastackMCP/1.0',
            'Accept': 'application/json',
            'Connection': 'keep-alive'
        })
        
        response = await loop.run_in_executor(
            None, 
            lambda: session.get(f"{MEDIASTACK_BASE_URL}/{endpoint}", params=params, timeout=10)
        )
        response.raise_for_status()
        
        # Validate response is JSON
        try:
            result = response.json()
            return result
        except ValueError as e:
            raise ValueError(f"Invalid JSON response from API: {str(e)}") from e
            
    except requests.exceptions.Timeout as exc:
        raise TimeoutError("API Request timed out after 10 seconds. Please try again.") from exc
    except requests.exceptions.ConnectionError as exc:
        raise ConnectionError("Failed to connect to mediastack API. Please check your internet connection.") from exc
    except requests.exceptions.HTTPError as e:
        error_data = {}
        try:
            error_data = response.json()
        except (ValueError, KeyError):
            pass
        
        if error_data.get('error'):
            error_msg = error_data['error'].get('message', str(e))
            error_code = error_data['error'].get('code', 'unknown')
            raise RuntimeError(f"Mediastack API Error [{error_code}]: {error_msg}") from e
        else:
            raise RuntimeError(f"HTTP Error {response.status_code}: {str(e)}") from e
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Network Error: {str(e)}") from e
    except Exception as e:
        if "Configuration Error" in str(e):
            raise e  # Re-raise configuration errors as-is
        raise RuntimeError(f"Unexpected error: {str(e)}") from e

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
        keywords: Search terms to filter news. Use - to exclude terms (e.g., "bitcoin -ethereum") (optional)
        sources: Include/exclude news sources, comma-separated. Use - to exclude (e.g., "cnn,bbc" or "cnn,-fox") (optional)
        countries: Two-letter country code(s), comma-separated. Use - to exclude (e.g., "us,gb" or "us,-ca") (optional)
        languages: Language code(s), comma-separated. Use - to exclude (e.g., "en,es" or "en,-de") (optional)
        categories: News categories, comma-separated. Options: business, entertainment, general, health, science, sports, technology. Use - to exclude (optional)
        date: Date or date range. Format: YYYY-MM-DD or YYYY-MM-DD,YYYY-MM-DD for range (optional)
        sort: Sort order. Options: published_desc (default), published_asc, popularity (optional)
        limit: Maximum number of results (1-100), default 25 (optional)
        offset: Pagination offset, default 0 (optional)
    
    Returns:
        JSON response from mediastack API containing news articles
    """
    # Validate limit
    if limit is not None:
        limit = min(max(1, limit), 100)  # Cap between 1 and 100
    
    # Validate sort parameter
    valid_sort_options = ['published_desc', 'published_asc', 'popularity']
    if sort is not None and sort not in valid_sort_options:
        raise ValueError(f"Invalid sort option. Must be one of: {', '.join(valid_sort_options)}")
    
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
    
    return await make_mediastack_request("news", params)

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
        search: Free-text search term to filter sources (optional)
        sources: Include/exclude specific sources, comma-separated. Use - to exclude (optional)
        countries: Two-letter country code(s), comma-separated. Use - to exclude (optional)
        languages: Language code(s), comma-separated. Use - to exclude (optional)
        categories: News categories, comma-separated. Options: business, entertainment, general, health, science, sports, technology. Use - to exclude (optional)
        limit: Maximum number of results (1-100), default 25 (optional)
        offset: Pagination offset, default 0 (optional)
    
    Returns:
        JSON response from mediastack API containing news sources
    """
    # Validate limit
    if limit is not None:
        limit = min(max(1, limit), 100)  # Cap between 1 and 100
    
    params = {
        "search": search,
        "sources": sources,
        "countries": countries,
        "languages": languages,
        "categories": categories,
        "limit": limit,
        "offset": offset
    }
    
    return await make_mediastack_request("sources", params) 