#!/usr/bin/env python3
"""
Entry point for the Checkson application.
Provides an interactive terminal UI when run directly.
"""
import sys
import os
import typer
import time
from typing import List, Optional, Dict, Any
import traceback
from rich.traceback import install
from rich.panel import Panel
from rich.text import Text
from rich import box

from checkson.cli.main import app
from checkson.utils.terminal import console, TerminalUI
from checkson.__init__ import __version__

# Install rich traceback handler for better error reporting
install(show_locals=False)


class ChecksonApp:
    """Main application class for Checkson interactive mode."""
    
    def __init__(self):
        """Initialize the application."""
        self.menu_options = [
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
    
    def show_header(self):
        """Display the application header."""
        TerminalUI.clear_terminal()
        TerminalUI.print_header(f"✨ Checkson v{__version__} ✨", clear=False)
        
        # Add a description panel
        console.print(Panel(
            Text("A fast, user-friendly availability checker for GitHub usernames,\nrepositories, and domain names.", 
                 style="cyan", justify="center"),
            border_style="blue",
            box=box.ROUNDED
        ))
    
    def show_help(self):
        """Show help information and return to menu."""
        TerminalUI.clear_terminal()
        os.system(f"{sys.executable} {__file__} --help")
        
        console.print("\n[bold cyan]Press Enter to return to the main menu...[/bold cyan]")
        input()
        self.run()
    
    def run_command(self, command: str):
        """Run a Checkson command and handle return to menu."""
        TerminalUI.clear_terminal()
        cmd = f"{sys.executable} {__file__} {command} --interactive"
        console.print(f"[dim]Running: {cmd}[/dim]\n")
        
        result = os.system(cmd)
        if result != 0:
            console.print(f"[bold yellow]Command completed with exit code {result}[/bold yellow]")
        
        # Ask if user wants to return to main menu
        console.print("\n[bold cyan]Return to main menu? (y/n)[/bold cyan] ", end="")
        response = input().lower()
        return response == "" or response.startswith("y")
    
    def exit_app(self):
        """Exit the application with a goodbye message."""
        console.print("[yellow]Goodbye! Thanks for using Checkson.[/yellow]")
        sys.exit(0)
    
    def handle_menu_choice(self, choice: str) -> bool:
        """
        Handle the user's menu selection.
        
        Args:
            choice: The selected menu option value
            
        Returns:
            True if should continue running, False to exit
        """
        if choice == "exit":
            self.exit_app()
            return False
        elif choice == "help":
            self.show_help()
            return True
        else:
            # Run the selected command
            return self.run_command(choice)
    
    def run(self):
        """Run the interactive application main loop."""
        try:
            # Show header and menu
            self.show_header()
            
            # Get user selection
            choice = TerminalUI.smart_menu("Please select an option:", self.menu_options)
            
            # Handle selection
            should_continue = self.handle_menu_choice(choice)
            
            # Continue if needed
            if should_continue:
                self.run()
            else:
                self.exit_app()
                
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            console.print("\n[yellow]Operation cancelled. Goodbye![/yellow]")
            sys.exit(0)
        except Exception as e:
            console.print(f"\n[bold red]An error occurred:[/bold red] {str(e)}")
            console.print("\nIf this issue persists, please report it on GitHub.")
            time.sleep(2)  # Give user time to read the error
            sys.exit(1)


# Function to run the interactive mode (callable from other modules)
def run_interactive_mode():
    """Run the application in interactive mode with a menu-based UI."""
    app_instance = ChecksonApp()
    app_instance.run()


def main():
    """Main entry point for the application."""
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


if __name__ == "__main__":
    main()
