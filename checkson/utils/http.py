"""
HTTP utilities for making API requests efficiently.
"""
import time
import asyncio
import httpx
import requests
from typing import Dict, List, Tuple, Any, Optional

from ..utils.config import DEFAULT_HEADERS, REQUEST_DELAY, REQUEST_TIMEOUT, MAX_CONCURRENT_REQUESTS


class HTTPClient:
    """HTTP client for making both synchronous and asynchronous requests."""
    
    @staticmethod
    def make_request(url: str, headers: Optional[Dict[str, str]] = None) -> Tuple[int, Dict[str, Any]]:
        """
        Make a synchronous HTTP request with rate limiting.
        
        Args:
            url: The URL to request
            headers: Optional custom headers
            
        Returns:
            Tuple of (status_code, response_data)
        """
        try:
            response = requests.get(
                url,
                headers=headers or DEFAULT_HEADERS,
                timeout=REQUEST_TIMEOUT
            )
            time.sleep(REQUEST_DELAY)  # Simple rate limiting
            return response.status_code, response.json() if response.status_code == 200 else {}
        except requests.exceptions.RequestException as e:
            # Return an error code for request exceptions
            return 500, {"error": str(e)}


class AsyncRequestManager:
    """Manages asynchronous HTTP requests with rate limiting and concurrency control."""
    
    def __init__(self, max_concurrent: int = MAX_CONCURRENT_REQUESTS, 
                 headers: Optional[Dict[str, str]] = None):
        """
        Initialize the async request manager.
        
        Args:
            max_concurrent: Maximum number of concurrent requests
            headers: Custom headers to use for all requests
        """
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.headers = headers or DEFAULT_HEADERS
    
    async def get(self, url: str) -> Tuple[str, int, Dict[str, Any]]:
        """
        Make an async HTTP request with rate limiting.
        
        Args:
            url: The URL to request
            
        Returns:
            Tuple of (url, status_code, response_data)
        """
        async with self.semaphore:  # Limit concurrent requests
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(
                        url, 
                        headers=self.headers,
                        timeout=REQUEST_TIMEOUT
                    )
                    
                    data = {}
                    if response.status_code == 200:
                        data = response.json()
                    
                    # Add a small delay for rate limiting
                    await asyncio.sleep(REQUEST_DELAY)
                    return url, response.status_code, data
            except httpx.RequestError as e:
                return url, 500, {"error": str(e)}
    
    async def batch_get(self, urls: List[str]) -> List[Tuple[str, int, Dict[str, Any]]]:
        """
        Execute multiple requests concurrently with rate limiting.
        
        Args:
            urls: List of URLs to request
            
        Returns:
            List of (url, status_code, response_data) tuples
        """
        tasks = [self.get(url) for url in urls]
        return await asyncio.gather(*tasks)


# Exported compatibility functions
def make_request(url: str, headers: Optional[Dict[str, str]] = None) -> Tuple[int, Dict[str, Any]]:
    """Make a synchronous HTTP request (wrapper for HTTPClient.make_request)."""
    return HTTPClient.make_request(url, headers) 