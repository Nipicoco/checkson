"""
Domain name availability checker.
"""
import socket
from typing import Dict, List, Any
import asyncio

from ..utils.terminal import format_status
from ..utils.http import AsyncRequestManager


class DomainChecker:
    """Class for checking domain name availability."""
    
    @staticmethod
    def check_domain(domain: str) -> Dict[str, Any]:
        """
        Basic check if a domain is available by attempting DNS resolution.
        Note: This is a simple check and not 100% reliable for domain availability.
        
        Args:
            domain: The domain name to check
            
        Returns:
            Dict containing the domain and status
        """
        try:
            # Try to resolve the domain
            socket.gethostbyname(domain)
            # If we get here, the domain exists
            return {
                "name": domain,
                "status": "❌ Taken",
                "available": False,
                "taken": True,
                "error": False
            }
        except socket.gaierror:
            # If we get a DNS error, the domain likely doesn't exist
            return {
                "name": domain,
                "status": "✅ Available",
                "available": True,
                "taken": False,
                "error": False
            }
        except Exception as e:
            # Other errors
            return {
                "name": domain,
                "status": f"⚠️ Error ({str(e)})",
                "available": False,
                "taken": False,
                "error": True
            }
    
    @staticmethod
    async def check_domain_async(domain: str) -> Dict[str, Any]:
        """
        Async wrapper for domain check.
        
        Args:
            domain: The domain name to check
            
        Returns:
            Dict containing check results
        """
        return await asyncio.to_thread(DomainChecker.check_domain, domain)
    
    @staticmethod
    async def check_domains_async(domains: List[str]) -> List[Dict[str, Any]]:
        """
        Check multiple domains concurrently.
        
        Args:
            domains: List of domain names to check
            
        Returns:
            List of dictionaries with check results
        """
        # Create tasks for each domain
        tasks = [DomainChecker.check_domain_async(domain) for domain in domains]
        
        # Run all tasks concurrently
        return await asyncio.gather(*tasks)


# Exported compatibility functions
def check_domain(domain: str) -> Dict[str, Any]:
    """Check domain availability (wrapper for DomainChecker.check_domain)."""
    return DomainChecker.check_domain(domain)

async def check_domain_async(domain: str) -> Dict[str, Any]:
    """Async domain check (wrapper for DomainChecker.check_domain_async)."""
    return await DomainChecker.check_domain_async(domain)

async def check_domains_async(domains: List[str]) -> List[Dict[str, Any]]:
    """Check multiple domains (wrapper for DomainChecker.check_domains_async)."""
    return await DomainChecker.check_domains_async(domains) 