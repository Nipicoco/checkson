"""
GitHub availability checker for usernames and repositories.
"""
import asyncio
from typing import Dict, List, Any, Tuple

from ..utils.config import GITHUB_API_URL
from ..utils.http import make_request, AsyncRequestManager
from ..utils.terminal import format_status


def check_github_username(name: str) -> Dict[str, Any]:
    """
    Check if a GitHub username is available.
    
    Args:
        name: The GitHub username to check
        
    Returns:
        Dict containing the name and status
    """
    url = f"{GITHUB_API_URL}/users/{name}"
    status_code, _ = make_request(url)
    
    return {
        "name": name,
        "status": format_status(status_code, "Username"),
        "available": status_code == 404,
        "taken": status_code == 200,
        "error": status_code not in (200, 404)
    }


def check_github_repo(org_or_user: str, repo_name: str) -> Dict[str, Any]:
    """
    Check if a GitHub repository name is available.
    
    Args:
        org_or_user: The GitHub organization or username
        repo_name: The repository name to check
        
    Returns:
        Dict containing the name and status
    """
    url = f"{GITHUB_API_URL}/repos/{org_or_user}/{repo_name}"
    status_code, _ = make_request(url)
    
    return {
        "name": f"{org_or_user}/{repo_name}",
        "status": format_status(status_code, "Repository"),
        "available": status_code == 404,
        "taken": status_code == 200,
        "error": status_code not in (200, 404)
    }


async def check_github_usernames_async(names: List[str]) -> List[Dict[str, Any]]:
    """
    Check multiple GitHub usernames concurrently.
    
    Args:
        names: List of GitHub usernames to check
        
    Returns:
        List of dictionaries with check results
    """
    request_manager = AsyncRequestManager()
    urls = [f"{GITHUB_API_URL}/users/{name}" for name in names]
    
    results = await request_manager.batch_get(urls)
    
    # Process results
    processed_results = []
    for i, (url, status_code, _) in enumerate(results):
        name = names[i]
        processed_results.append({
            "name": name,
            "status": format_status(status_code, "Username"),
            "available": status_code == 404,
            "taken": status_code == 200,
            "error": status_code not in (200, 404)
        })
    
    return processed_results


async def check_github_repos_async(org_or_user: str, repo_names: List[str]) -> List[Dict[str, Any]]:
    """
    Check multiple GitHub repository names concurrently.
    
    Args:
        org_or_user: The GitHub organization or username
        repo_names: List of repository names to check
        
    Returns:
        List of dictionaries with check results
    """
    request_manager = AsyncRequestManager()
    urls = [f"{GITHUB_API_URL}/repos/{org_or_user}/{name}" for name in repo_names]
    
    results = await request_manager.batch_get(urls)
    
    # Process results
    processed_results = []
    for i, (url, status_code, _) in enumerate(results):
        name = f"{org_or_user}/{repo_names[i]}"
        processed_results.append({
            "name": name,
            "status": format_status(status_code, "Repository"),
            "available": status_code == 404,
            "taken": status_code == 200,
            "error": status_code not in (200, 404)
        })
    
    return processed_results 