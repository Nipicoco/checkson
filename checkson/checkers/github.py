"""
GitHub availability checker for usernames and repositories.
"""
import asyncio
from typing import Dict, List, Any, Tuple

from ..utils.config import GITHUB_API_URL
from ..utils.http import HTTPClient, AsyncRequestManager
from ..utils.terminal import format_status


class GitHubChecker:
    """Class for checking GitHub username and repository availability."""
    
    @staticmethod
    def check_username(name: str) -> Dict[str, Any]:
        """
        Check if a GitHub username is available.
        
        Args:
            name: The GitHub username to check
            
        Returns:
            Dict containing the name and status
        """
        url = f"{GITHUB_API_URL}/users/{name}"
        status_code, _ = HTTPClient.make_request(url)
        
        return {
            "name": name,
            "status": format_status(status_code, "Username"),
            "available": status_code == 404,
            "taken": status_code == 200,
            "error": status_code not in (200, 404)
        }

    @staticmethod
    def check_repo(org_or_user: str, repo_name: str) -> Dict[str, Any]:
        """
        Check if a GitHub repository name is available.
        
        Args:
            org_or_user: The GitHub organization or username
            repo_name: The repository name to check
            
        Returns:
            Dict containing the name and status
        """
        url = f"{GITHUB_API_URL}/repos/{org_or_user}/{repo_name}"
        status_code, _ = HTTPClient.make_request(url)
        
        return {
            "name": f"{org_or_user}/{repo_name}",
            "status": format_status(status_code, "Repository"),
            "available": status_code == 404,
            "taken": status_code == 200,
            "error": status_code not in (200, 404)
        }

    @staticmethod
    async def check_usernames_async(names: List[str]) -> List[Dict[str, Any]]:
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

    @staticmethod
    async def check_repos_async(org_or_user: str, repo_names: List[str]) -> List[Dict[str, Any]]:
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


# Exported compatibility functions
def check_github_username(name: str) -> Dict[str, Any]:
    """Check GitHub username (wrapper for GitHubChecker.check_username)."""
    return GitHubChecker.check_username(name)

def check_github_repo(org_or_user: str, repo_name: str) -> Dict[str, Any]:
    """Check GitHub repo (wrapper for GitHubChecker.check_repo)."""
    return GitHubChecker.check_repo(org_or_user, repo_name)

async def check_github_usernames_async(names: List[str]) -> List[Dict[str, Any]]:
    """Check multiple GitHub usernames (wrapper for GitHubChecker.check_usernames_async)."""
    return await GitHubChecker.check_usernames_async(names)

async def check_github_repos_async(org_or_user: str, repo_names: List[str]) -> List[Dict[str, Any]]:
    """Check multiple GitHub repos (wrapper for GitHubChecker.check_repos_async)."""
    return await GitHubChecker.check_repos_async(org_or_user, repo_names) 