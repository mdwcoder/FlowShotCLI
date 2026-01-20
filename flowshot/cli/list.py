import typer
from rich.console import Console
from rich.table import Table
from flowshot.core.storage import Storage


console = Console()

def list_commands():
    """
    List commands in the current flow.
    """
    storage = Storage()
    flow = storage.current_flow
    
    if not flow:
        console.print("[yellow]No active flow found.[/yellow]")
        return
        
    if not flow.commands:
        console.print("[yellow]Current flow is empty.[/yellow]")
        return
        
    table = Table(title=f"Flow: {flow.name} ({flow.id[:8]})")
    table.add_column("Index", justify="right", style="cyan", no_wrap=True)
    table.add_column("Command", style="white")
    table.add_column("Note", style="italic green")
    
    for idx, cmd in enumerate(flow.commands):
        note_str = cmd.note if cmd.note else ""
        table.add_row(str(idx), cmd.cmd, note_str)
        
    console.print(table)
