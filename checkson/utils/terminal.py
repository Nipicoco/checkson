from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.table import Table
from rich.style import Style
from rich.text import Text

from typing import Dict, List, Any
from ..utils.config import STYLE_CONFIG, AVAILABLE_INDICATOR, TAKEN_INDICATOR, ERROR_INDICATOR

console = Console()

def create_progress_bar() -> Progress:
    """Create a custom progress bar with spinner for async operations."""
    return Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(bar_width=40),
        TaskProgressColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        console=console
    )

def print_header(title: str) -> None:
    """Print a styled header for the application."""
    console.print(Panel(
        Text(title, style=STYLE_CONFIG["header"], justify="center"), 
        border_style=STYLE_CONFIG["header"]
    ))

def print_subheader(text: str) -> None:
    """Print a styled subheader."""
    console.print(f"\n[{STYLE_CONFIG['subheader']}]{text}[/{STYLE_CONFIG['subheader']}]")

def print_result_table(results: List[Dict[str, Any]], title: str) -> None:
    """Print results in a nicely formatted table."""
    table = Table(title=title, show_header=True, header_style="bold")
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

def format_status(status_code: int, service_type: str = "Username") -> str:
    """Format status based on HTTP response code."""
    if status_code == 404:
        return f"{AVAILABLE_INDICATOR} Available"
    elif status_code == 200:
        return f"{TAKEN_INDICATOR} Taken"
    else:
        return f"{ERROR_INDICATOR} Error ({status_code})"

def print_summary(total: int, available: int, taken: int, errors: int) -> None:
    """Print a summary of results."""
    console.print(Panel(
        f"[bold]Summary:[/bold]\n"
        f"[{STYLE_CONFIG['normal']}]Total checked: {total}[/{STYLE_CONFIG['normal']}]\n"
        f"[{STYLE_CONFIG['available']}]Available: {available}[/{STYLE_CONFIG['available']}]\n"
        f"[{STYLE_CONFIG['taken']}]Taken: {taken}[/{STYLE_CONFIG['taken']}]\n"
        f"[{STYLE_CONFIG['error']}]Errors: {errors}[/{STYLE_CONFIG['error']}]",
        title="Results",
        border_style=STYLE_CONFIG["info"]
    )) 