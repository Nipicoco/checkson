import os
from typing import Dict, Optional
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# API configuration
GITHUB_API_URL = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# HTTP request headers with rate limiting
DEFAULT_HEADERS: Dict[str, str] = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "Checkson-Availability-Checker/1.0.0",
}

if GITHUB_TOKEN:
    DEFAULT_HEADERS["Authorization"] = f"Bearer {GITHUB_TOKEN}"

# Rate limiting configuration
REQUEST_DELAY = 0.1  # seconds between requests in sequential mode
MAX_CONCURRENT_REQUESTS = 10  # maximum number of concurrent requests in async mode

# Terminal styling configuration
STYLE_CONFIG = {
    "available": "bold green",
    "taken": "bold red",
    "error": "bold yellow",
    "header": "bold blue",
    "subheader": "blue",
    "normal": "white",
    "info": "cyan",
    "prompt": "bold magenta",
}

# Result indicators
AVAILABLE_INDICATOR = "✅"
TAKEN_INDICATOR = "❌"
ERROR_INDICATOR = "⚠️"

# Default timeout for all requests (seconds)
REQUEST_TIMEOUT = 5 