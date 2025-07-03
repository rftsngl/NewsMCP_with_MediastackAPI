"""
MCP Tools for mediastack News API
"""
import os
import requests
from typing import Optional, Dict, Any, List
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
        raise Exception("MEDIASTACK_API_KEY environment variable is required")
    return api_key

# Helper function for API calls
def make_mediastack_request(endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Make a request to mediastack API with error handling
    """
    # Get API key only when making actual API calls (lazy loading)
    try:
        api_key = get_api_key()
    except Exception as e:
        raise Exception(f"Configuration Error: {str(e)}")
    
    # Add API key to params
    params['access_key'] = api_key
    
    # Remove None values from params
    params = {k: v for k, v in params.items() if v is not None}
    
    try:
        response = requests.get(f"{MEDIASTACK_BASE_URL}/{endpoint}", params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        raise Exception("API Request timed out. Please try again.")
    except requests.exceptions.HTTPError as e:
        error_data = {}
        try:
            error_data = response.json()
        except:
            pass
        
        if error_data.get('error'):
            error_msg = error_data['error'].get('message', str(e))
            error_code = error_data['error'].get('code', 'unknown')
            raise Exception(f"Mediastack API Error [{error_code}]: {error_msg}")
        else:
            raise Exception(f"HTTP Error: {str(e)}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Network Error: {str(e)}")

@mcp.tool()
def get_latest_news(
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
        raise Exception(f"Invalid sort option. Must be one of: {', '.join(valid_sort_options)}")
    
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
    
    return make_mediastack_request("news", params)

@mcp.tool()
def get_sources(
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
    
    return make_mediastack_request("sources", params) 