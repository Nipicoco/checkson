import os
import sys
import platform
import threading
import time
from typing import Dict, List, Any, Optional, Callable
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.table import Table
from rich.style import Style
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.live import Live
from rich.layout import Layout
from rich.align import Align
from rich import box

from ..utils.config import STYLE_CONFIG, AVAILABLE_INDICATOR, TAKEN_INDICATOR, ERROR_INDICATOR

# Create a single console instance for the application
console = Console()


class TerminalUI:
    """Class for handling terminal UI operations with consistent styling."""

    @staticmethod
    def clear_terminal() -> None:
        """Clear the terminal for a cleaner UI experience."""
        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")

    @staticmethod
    def print_header(title: str, clear: bool = True) -> None:
        """Print a styled header for the application."""
        if clear:
            TerminalUI.clear_terminal()
        
        console.print("\n")
        console.print(Panel(
            Text(title, style=STYLE_CONFIG["header"], justify="center"), 
            border_style=STYLE_CONFIG["header"],
            box=box.DOUBLE
        ))

    @staticmethod
    def print_subheader(text: str) -> None:
        """Print a styled subheader."""
        console.print(f"\n[{STYLE_CONFIG['subheader']}]{text}[/{STYLE_CONFIG['subheader']}]")

    @staticmethod
    def print_result_table(results: List[Dict[str, Any]], title: str) -> None:
        """Print results in a nicely formatted table."""
        table = Table(title=title, show_header=True, header_style="bold", box=box.ROUNDED)
        table.add_column("Name", style="cyan")
        table.add_column("Status", style="white")
        
        for result in results:
            name = result["name"]
            status = result["status"]
            
            if "Available" in status:
                status_style = STYLE_CONFIG["available"]
            elif "Taken" in status:
                status_style = STYLE_CONFIG["taken"]
            else:
                status_style = STYLE_CONFIG["error"]
                
            table.add_row(name, Text(status, style=status_style))
        
        console.print(table)

    @staticmethod
    def print_summary(total: int, available: int, taken: int, errors: int) -> None:
        """Print a summary of results."""
        console.print(Panel(
            f"[bold]Summary:[/bold]\n"
            f"[{STYLE_CONFIG['normal']}]Total checked: {total}[/{STYLE_CONFIG['normal']}]\n"
            f"[{STYLE_CONFIG['available']}]Available: {available}[/{STYLE_CONFIG['available']}]\n"
            f"[{STYLE_CONFIG['taken']}]Taken: {taken}[/{STYLE_CONFIG['taken']}]\n"
            f"[{STYLE_CONFIG['error']}]Errors: {errors}[/{STYLE_CONFIG['error']}]",
            title="Results",
            border_style=STYLE_CONFIG["info"],
            box=box.ROUNDED
        ))

    @staticmethod
    def create_progress_bar() -> Progress:
        """Create a custom progress bar with spinner for async operations."""
        return Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(bar_width=40, complete_style="green", finished_style="bold green"),
            TaskProgressColumn(),
            "[progress.percentage]{task.percentage:>3.0f}%",
            console=console,
            expand=True
        )
    
    @staticmethod
    def smart_menu(title: str, options: List[Dict[str, Any]]) -> str:
        """
        Display a menu that supports both keyboard navigation and number input.
        Compatible with both Windows and Mac/Linux.
        
        Args:
            title: The title of the menu
            options: List of dictionaries with 'name', 'description', and 'value' keys
            
        Returns:
            The value of the selected option
        """
        TerminalUI.clear_terminal()
        selected = 0
        
        def render_menu() -> str:
            menu_text = f"[bold]{title}[/bold]\n\n"
            for i, opt in enumerate(options):
                style = "bold magenta" if i == selected else "cyan"
                prefix = "→" if i == selected else " "
                menu_text += f"{prefix} [bold]{i+1})[/bold] [{style}]{opt['name']}[/{style}]: {opt['description']}\n"
            
            menu_text += "\n[dim]Navigation: Enter number or use Up/Down/W/S/J/K keys[/dim]"
            return menu_text
        
        while True:
            # Clear and redraw the menu
            TerminalUI.clear_terminal()
            console.print(Panel(
                render_menu(),
                title="Menu",
                border_style=STYLE_CONFIG["info"],
                box=box.ROUNDED
            ))
            
            # Get input
            console.print("[bold magenta]Your choice:[/bold magenta] ", end="")
            
            # Read user input
            try:
                key = console.input()
                
                # Numeric choice (direct selection)
                if key.isdigit():
                    idx = int(key) - 1
                    if 0 <= idx < len(options):
                        return options[idx]["value"]
                    else:
                        console.print("[yellow]Invalid option. Please try again.[/yellow]")
                        time.sleep(1)
                
                # Arrow key navigation (special keys and alternatives)
                elif key == "KEY_UP" or key.lower() == "w" or key == "k":
                    selected = max(0, selected - 1)
                elif key == "KEY_DOWN" or key.lower() == "s" or key == "j":
                    selected = min(len(options) - 1, selected + 1)
                elif key == "KEY_ENTER" or key == "\r" or key == "\n" or key == "":
                    return options[selected]["value"]
                
                # Handle escape key or 'q' for cancellation
                elif key == "KEY_ESCAPE" or key.lower() == "q":
                    raise KeyboardInterrupt
                    
            except KeyboardInterrupt:
                console.print("[yellow]Operation cancelled by user[/yellow]")
                sys.exit(0)
            except Exception:
                # For any other errors, just redraw the menu
                continue

    @staticmethod
    def format_status(status_code: int, service_type: str = "Username") -> str:
        """Format status based on HTTP response code."""
        if status_code == 404:
            return f"{AVAILABLE_INDICATOR} Available"
        elif status_code == 200:
            return f"{TAKEN_INDICATOR} Taken"
        else:
            return f"{ERROR_INDICATOR} Error ({status_code})"


# Exported utility functions that maintain backward compatibility
def clear_terminal():
    """Clear the terminal (wrapper for TerminalUI.clear_terminal)."""
    return TerminalUI.clear_terminal()

def print_header(title: str, clear: bool = True):
    """Print header (wrapper for TerminalUI.print_header)."""
    return TerminalUI.print_header(title, clear)

def print_subheader(text: str):
    """Print subheader (wrapper for TerminalUI.print_subheader)."""
    return TerminalUI.print_subheader(text)

def print_result_table(results: List[Dict[str, Any]], title: str):
    """Print result table (wrapper for TerminalUI.print_result_table)."""
    return TerminalUI.print_result_table(results, title)

def print_summary(total: int, available: int, taken: int, errors: int):
    """Print summary (wrapper for TerminalUI.print_summary)."""
    return TerminalUI.print_summary(total, available, taken, errors)

def create_progress_bar():
    """Create progress bar (wrapper for TerminalUI.create_progress_bar)."""
    return TerminalUI.create_progress_bar()

def format_status(status_code: int, service_type: str = "Username"):
    """Format status (wrapper for TerminalUI.format_status)."""
    return TerminalUI.format_status(status_code, service_type)


def interactive_menu(options: List[Dict[str, Any]]) -> str:
    """
    Interactive menu that works across platforms.
    
    Args:
        options: List of dictionaries with 'name', 'description', and 'value' keys
        
    Returns:
        The value of the selected option
    """
    TerminalUI.print_header("Checkson - Availability Checker")
    return TerminalUI.smart_menu("Please select an option:", options)


def select_menu(title: str, options: List[str], default_index: int = 0) -> int:
    """
    Display an interactive selection menu and return the selected index.
    
    Args:
        title: The title of the menu
        options: List of option strings to display
        default_index: The initially selected index
        
    Returns:
        Selected index
    """
    # Convert simple options list to the format required by smart_menu
    menu_options = [
        {"name": option, "description": "", "value": i}
        for i, option in enumerate(options)
    ]
    
    # Use smart_menu and return the index
    return TerminalUI.smart_menu(title, menu_options) 