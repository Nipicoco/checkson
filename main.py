#!/usr/bin/env python3
"""
Entry point for the Checkson application.
Provides an interactive terminal UI when run directly.
"""
import sys
import os
import typer
import time
from typing import List, Optional
import traceback
from rich.traceback import install

from checkson.cli.main import app
from checkson.utils.terminal import clear_terminal, interactive_menu, print_header, console
from checkson.__init__ import __version__

# Install rich traceback handler for better error reporting
install(show_locals=False)

def run_interactive_mode():
    """Run the application in interactive mode with a menu-based UI."""
    clear_terminal()
    print_header(f"✨ Checkson v{__version__} ✨", clear=False)
    
    options = [
        {
            "name": "🔍 GitHub Usernames", 
            "description": "Check availability of GitHub usernames",
            "value": "github"
        },
        {
            "name": "📁 GitHub Repositories", 
            "description": "Check if repositories exist under an owner",
            "value": "repo"
        },
        {
            "name": "🌐 Domain Names", 
            "description": "Check if domain names are available",
            "value": "domain"
        },
        {
            "name": "❓ Help", 
            "description": "Show help information",
            "value": "help"
        },
        {
            "name": "❌ Exit", 
            "description": "Exit the application",
            "value": "exit"
        }
    ]
    
    try:
        choice = interactive_menu(options)
        
        if choice == "exit":
            console.print("[yellow]Goodbye! Thanks for using Checkson.[/yellow]")
            sys.exit(0)
        elif choice == "help":
            # Show help and then return to menu
            clear_terminal()
            os.system(f"{sys.executable} {__file__} --help")
            
            console.print("\n[bold cyan]Press Enter to return to the main menu...[/bold cyan]")
            input()
            run_interactive_mode()
        else:
            # Run the selected command in interactive mode
            clear_terminal()
            command = f"{sys.executable} {__file__} {choice} --interactive"
            console.print(f"[dim]Running: {command}[/dim]\n")
            
            result = os.system(command)
            if result != 0:
                console.print(f"[bold yellow]Command completed with exit code {result}[/bold yellow]")
            
            # Ask if user wants to return to main menu
            console.print("\n[bold cyan]Return to main menu? (y/n)[/bold cyan] ", end="")
            response = input().lower()
            if response == "" or response.startswith("y"):
                run_interactive_mode()
            else:
                console.print("[yellow]Goodbye! Thanks for using Checkson.[/yellow]")
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        console.print("\n[yellow]Operation cancelled. Goodbye![/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[bold red]An error occurred:[/bold red] {str(e)}")
        console.print("\nIf this issue persists, please report it on GitHub.")
        time.sleep(2)  # Give user time to read the error
        sys.exit(1)

if __name__ == "__main__":
    try:
        # If no command line arguments are provided, run in interactive mode
        if len(sys.argv) == 1:
            run_interactive_mode()
        else:
            # Otherwise, pass control to the Typer app
            app()
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        console.print("\n[yellow]Operation cancelled. Goodbye![/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[bold red]An error occurred:[/bold red] {str(e)}")
        sys.exit(1)
