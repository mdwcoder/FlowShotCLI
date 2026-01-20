import typer
from rich import print
from flowshot.core.storage import Storage


def drop(index: int):
    """
    Remove a command by its index.
    """
    storage = Storage()
    flow = storage.current_flow
    
    if not flow:
        print("[yellow]No active flow found.[/yellow]")
        raise typer.Exit(code=1)
        
    if flow.remove_command(index):
        storage.save_flow(flow)
        print(f"[green]Dropped command at index {index}.[/green]")
    else:
        print(f"[red]Index {index} out of range.[/red]")
        raise typer.Exit(code=1)
