"""
MCP Tools for mediastack News API
"""
import os
import requests
from typing import Optional, Dict, Any, List
from fastmcp import FastMCP
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastMCP
mcp = FastMCP("Mediastack News MCP Server")

# API Configuration
MEDIASTACK_API_KEY = os.getenv("MEDIASTACK_API_KEY", "7fe3726d5472d411890c696256371833")
MEDIASTACK_BASE_URL = "https://api.mediastack.com/v1"

# Helper function for API calls
def make_mediastack_request(endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Make a request to mediastack API with error handling
    """
    # Add API key to params
    params['access_key'] = MEDIASTACK_API_KEY
    
    # Remove None values from params
    params = {k: v for k, v in params.items() if v is not None}
    
    try:
        response = requests.get(f"{MEDIASTACK_BASE_URL}/{endpoint}", params=params)
        response.raise_for_status()
        return response.json()
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
    countries: Optional[str] = None,
    languages: Optional[str] = None,
    categories: Optional[str] = None,
    limit: Optional[int] = 20
) -> Dict[str, Any]:
    """
    Fetches the most recent news stories from mediastack.
    
    Args:
        keywords: Search terms to filter news (optional)
        countries: Two-letter country code(s), comma-separated (optional)
        languages: Language code(s), comma-separated (optional)
        categories: News category - business, entertainment, general, health, science, sports, technology (comma-separated, optional)
        limit: Maximum number of results, default 20 (optional)
    
    Returns:
        JSON response from mediastack API containing news articles
    """
    # Validate limit
    if limit is not None:
        limit = min(max(1, limit), 100)  # Cap between 1 and 100
    
    params = {
        "keywords": keywords,
        "countries": countries,
        "languages": languages,
        "categories": categories,
        "limit": limit
    }
    
    return make_mediastack_request("news", params)

@mcp.tool()
def get_sources(
    search: Optional[str] = None,
    countries: Optional[str] = None,
    languages: Optional[str] = None,
    categories: Optional[str] = None,
    limit: Optional[int] = 20
) -> Dict[str, Any]:
    """
    List available news sources from mediastack.
    
    Args:
        search: Free-text search term to filter sources (optional)
        countries: Two-letter country code(s), comma-separated (optional)
        languages: Language code(s), comma-separated (optional)
        categories: News category - business, entertainment, general, health, science, sports, technology (comma-separated, optional)
        limit: Maximum number of results, default 20 (optional)
    
    Returns:
        JSON response from mediastack API containing news sources
    """
    # Validate limit
    if limit is not None:
        limit = min(max(1, limit), 100)  # Cap between 1 and 100
    
    params = {
        "search": search,
        "countries": countries,
        "languages": languages,
        "categories": categories,
        "limit": limit
    }
    
    return make_mediastack_request("sources", params) 