"""
Main CLI entry point for the Checkson application.
"""
import asyncio
import typer
from typing import List, Optional
from pathlib import Path
import sys
import time

from rich.prompt import Prompt, Confirm

from ..utils.terminal import (
    print_header, 
    print_subheader, 
    print_result_table, 
    print_summary,
    create_progress_bar,
    console,
    clear_terminal
)
from ..checkers.github import (
    check_github_username,
    check_github_usernames_async,
    check_github_repo,
    check_github_repos_async
)
from ..checkers.domains import check_domain, check_domains_async
from ..__init__ import __version__

# Create Typer app with rich formatting
app = typer.Typer(
    help="✨ Checkson - A fast and user-friendly availability checker ✨",
    add_completion=False,
    rich_markup_mode="rich"
)


@app.callback()
def callback(
    version: Optional[bool] = typer.Option(
        None, "--version", "-v", help="Show version and exit", is_flag=True
    )
):
    """
    🔍 [bold blue]Checkson[/bold blue] - Check the availability of usernames, repositories, and domains.
    
    A fast, modern CLI tool with beautiful terminal UI.
    """
    # Show the header
    print_header(f"✨ Checkson v{__version__} ✨")
    
    # Show version and exit if requested
    if version:
        console.print(f"[bold]Checkson[/bold] version: [cyan]{__version__}[/cyan]")
        raise typer.Exit()


@app.command()
def github(
    usernames: List[str] = typer.Argument(
        None, 
        help="GitHub usernames to check"
    ),
    input_file: Optional[Path] = typer.Option(
        None, 
        "--file", 
        "-f", 
        help="File containing usernames to check (one per line)"
    ),
    async_mode: bool = typer.Option(
        True, 
        "--async/--sync", 
        help="Use async mode for faster checking"
    ),
    interactive: bool = typer.Option(
        False, 
        "--interactive", 
        "-i", 
        help="Interactive mode"
    )
):
    """
    🔍 Check GitHub username availability.
    
    Quickly find out if GitHub usernames are available for registration.
    """
    names_to_check = []
    
    # Load from file if specified
    if input_file:
        try:
            with open(input_file, 'r') as f:
                file_names = [line.strip() for line in f if line.strip()]
                names_to_check.extend(file_names)
        except Exception as e:
            console.print(f"[bold red]Error reading file:[/bold red] {str(e)}")
            raise typer.Exit(1)
    
    # Add names from arguments
    if usernames:
        names_to_check.extend(usernames)
    
    # Interactive mode if no names provided or explicitly requested
    if not names_to_check or interactive:
        print_subheader("Enter GitHub usernames to check (empty line to finish):")
        while True:
            name = Prompt.ask("[bold cyan]Username[/bold cyan]")
            if not name:
                break
            names_to_check.append(name)
    
    if not names_to_check:
        console.print("[bold yellow]No usernames to check.[/bold yellow]")
        raise typer.Exit(0)
    
    # Display what we're checking
    print_subheader(f"Checking {len(names_to_check)} GitHub usernames...")
    
    # Start the check
    start_time = time.time()
    results = []
    
    if async_mode and len(names_to_check) > 1:
        # Use async for multiple names
        with create_progress_bar() as progress:
            task = progress.add_task("Checking usernames...", total=len(names_to_check))
            
            async def run_async_check():
                nonlocal results
                results = await check_github_usernames_async(names_to_check)
                progress.update(task, completed=len(names_to_check))
            
            asyncio.run(run_async_check())
    else:
        # Use sync for a single name or if async mode is disabled
        with create_progress_bar() as progress:
            task = progress.add_task("Checking usernames...", total=len(names_to_check))
            
            for name in names_to_check:
                result = check_github_username(name)
                results.append(result)
                progress.update(task, advance=1)
    
    # Calculate stats
    available = sum(1 for r in results if r.get('available', False))
    taken = sum(1 for r in results if r.get('taken', False))
    errors = sum(1 for r in results if r.get('error', False))
    
    # Print results
    elapsed = time.time() - start_time
    print_result_table(results, f"GitHub Username Results (completed in {elapsed:.2f}s)")
    print_summary(len(results), available, taken, errors)


@app.command()
def repo(
    owner: str = typer.Option(
        ..., 
        "--owner", 
        "-o", 
        help="GitHub username or organization"
    ),
    names: List[str] = typer.Argument(
        None, 
        help="Repository names to check"
    ),
    input_file: Optional[Path] = typer.Option(
        None, 
        "--file", 
        "-f", 
        help="File containing repository names to check (one per line)"
    ),
    async_mode: bool = typer.Option(
        True, 
        "--async/--sync", 
        help="Use async mode for faster checking"
    ),
    interactive: bool = typer.Option(
        False, 
        "--interactive", 
        "-i", 
        help="Interactive mode"
    )
):
    """
    📁 Check GitHub repository availability.
    
    Check if repository names are available under a specific user or organization.
    """
    names_to_check = []
    
    # Load from file if specified
    if input_file:
        try:
            with open(input_file, 'r') as f:
                file_names = [line.strip() for line in f if line.strip()]
                names_to_check.extend(file_names)
        except Exception as e:
            console.print(f"[bold red]Error reading file:[/bold red] {str(e)}")
            raise typer.Exit(1)
    
    # Add names from arguments
    if names:
        names_to_check.extend(names)
    
    # Interactive mode if no names provided or explicitly requested
    if not names_to_check or interactive:
        print_subheader("Enter repository names to check (empty line to finish):")
        while True:
            name = Prompt.ask("[bold cyan]Repository name[/bold cyan]")
            if not name:
                break
            names_to_check.append(name)
    
    if not names_to_check:
        console.print("[bold yellow]No repository names to check.[/bold yellow]")
        raise typer.Exit(0)
    
    # Display what we're checking
    print_subheader(f"Checking {len(names_to_check)} repositories under {owner}...")
    
    # Start the check
    start_time = time.time()
    results = []
    
    if async_mode and len(names_to_check) > 1:
        # Use async for multiple names
        with create_progress_bar() as progress:
            task = progress.add_task("Checking repositories...", total=len(names_to_check))
            
            async def run_async_check():
                nonlocal results
                results = await check_github_repos_async(owner, names_to_check)
                progress.update(task, completed=len(names_to_check))
            
            asyncio.run(run_async_check())
    else:
        # Use sync for a single name or if async mode is disabled
        with create_progress_bar() as progress:
            task = progress.add_task("Checking repositories...", total=len(names_to_check))
            
            for name in names_to_check:
                result = check_github_repo(owner, name)
                results.append(result)
                progress.update(task, advance=1)
    
    # Calculate stats
    available = sum(1 for r in results if r.get('available', False))
    taken = sum(1 for r in results if r.get('taken', False))
    errors = sum(1 for r in results if r.get('error', False))
    
    # Print results
    elapsed = time.time() - start_time
    print_result_table(results, f"GitHub Repository Results (completed in {elapsed:.2f}s)")
    print_summary(len(results), available, taken, errors)


@app.command()
def domain(
    domains: List[str] = typer.Argument(
        None, 
        help="Domain names to check"
    ),
    input_file: Optional[Path] = typer.Option(
        None, 
        "--file", 
        "-f", 
        help="File containing domain names to check (one per line)"
    ),
    async_mode: bool = typer.Option(
        True, 
        "--async/--sync", 
        help="Use async mode for faster checking"
    ),
    interactive: bool = typer.Option(
        False, 
        "--interactive", 
        "-i", 
        help="Interactive mode"
    )
):
    """
    🌐 Check domain name availability.
    
    Find out if domain names are registered or available for purchase.
    """
    domains_to_check = []
    
    # Load from file if specified
    if input_file:
        try:
            with open(input_file, 'r') as f:
                file_domains = [line.strip() for line in f if line.strip()]
                domains_to_check.extend(file_domains)
        except Exception as e:
            console.print(f"[bold red]Error reading file:[/bold red] {str(e)}")
            raise typer.Exit(1)
    
    # Add domains from arguments
    if domains:
        domains_to_check.extend(domains)
    
    # Interactive mode if no domains provided or explicitly requested
    if not domains_to_check or interactive:
        print_subheader("Enter domain names to check (empty line to finish):")
        while True:
            domain = Prompt.ask("[bold cyan]Domain name[/bold cyan]")
            if not domain:
                break
            domains_to_check.append(domain)
    
    if not domains_to_check:
        console.print("[bold yellow]No domains to check.[/bold yellow]")
        raise typer.Exit(0)
    
    # Display what we're checking
    print_subheader(f"Checking {len(domains_to_check)} domains...")
    
    # Start the check
    start_time = time.time()
    results = []
    
    if async_mode and len(domains_to_check) > 1:
        # Use async for multiple domains
        with create_progress_bar() as progress:
            task = progress.add_task("Checking domains...", total=len(domains_to_check))
            
            async def run_async_check():
                nonlocal results
                results = await check_domains_async(domains_to_check)
                progress.update(task, completed=len(domains_to_check))
            
            asyncio.run(run_async_check())
    else:
        # Use sync for a single domain or if async mode is disabled
        with create_progress_bar() as progress:
            task = progress.add_task("Checking domains...", total=len(domains_to_check))
            
            for domain_name in domains_to_check:
                result = check_domain(domain_name)
                results.append(result)
                progress.update(task, advance=1)
    
    # Calculate stats
    available = sum(1 for r in results if r.get('available', False))
    taken = sum(1 for r in results if r.get('taken', False))
    errors = sum(1 for r in results if r.get('error', False))
    
    # Print results
    elapsed = time.time() - start_time
    print_result_table(results, f"Domain Results (completed in {elapsed:.2f}s)")
    print_summary(len(results), available, taken, errors)


if __name__ == "__main__":
    app() 