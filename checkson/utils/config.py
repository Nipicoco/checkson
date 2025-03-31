"""
Configuration module for Checkson application.
"""
import os
from typing import Dict, Optional
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()


@dataclass
class APIConfig:
    """API configuration settings."""
    # GitHub API configuration
    GITHUB_API_URL: str = "https://api.github.com"
    GITHUB_TOKEN: Optional[str] = os.getenv("GITHUB_TOKEN")
    
    # Default headers for API requests
    DEFAULT_HEADERS: Dict[str, str] = None
    
    def __post_init__(self):
        """Initialize calculated fields after initialization."""
        # Initialize headers with token if available
        self.DEFAULT_HEADERS = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "Checkson-Availability-Checker/1.0.0",
        }
        
        if self.GITHUB_TOKEN:
            self.DEFAULT_HEADERS["Authorization"] = f"Bearer {self.GITHUB_TOKEN}"


@dataclass
class RateLimitConfig:
    """Rate limiting configuration settings."""
    # Rate limiting configuration
    REQUEST_DELAY: float = 0.1  # seconds between requests in sequential mode
    MAX_CONCURRENT_REQUESTS: int = 10  # maximum number of concurrent requests in async mode
    REQUEST_TIMEOUT: int = 5  # default timeout for all requests (seconds)


@dataclass
class UIConfig:
    """Terminal UI configuration settings."""
    # Terminal styling configuration
    STYLE_CONFIG: Dict[str, str] = None
    
    # Result indicators
    AVAILABLE_INDICATOR: str = "✅"
    TAKEN_INDICATOR: str = "❌"
    ERROR_INDICATOR: str = "⚠️"
    
    def __post_init__(self):
        """Initialize calculated fields after initialization."""
        self.STYLE_CONFIG = {
            "available": "bold green",
            "taken": "bold red",
            "error": "bold yellow",
            "header": "bold blue",
            "subheader": "blue",
            "normal": "white",
            "info": "cyan",
            "prompt": "bold magenta",
        }


# Create global configuration instances
api_config = APIConfig()
rate_limit_config = RateLimitConfig()
ui_config = UIConfig()

# Exported variables for backward compatibility
GITHUB_API_URL = api_config.GITHUB_API_URL
GITHUB_TOKEN = api_config.GITHUB_TOKEN
DEFAULT_HEADERS = api_config.DEFAULT_HEADERS

REQUEST_DELAY = rate_limit_config.REQUEST_DELAY
MAX_CONCURRENT_REQUESTS = rate_limit_config.MAX_CONCURRENT_REQUESTS
REQUEST_TIMEOUT = rate_limit_config.REQUEST_TIMEOUT

STYLE_CONFIG = ui_config.STYLE_CONFIG
AVAILABLE_INDICATOR = ui_config.AVAILABLE_INDICATOR
TAKEN_INDICATOR = ui_config.TAKEN_INDICATOR
ERROR_INDICATOR = ui_config.ERROR_INDICATOR 