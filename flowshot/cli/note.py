import typer
from rich import print
from typing import Optional
from flowshot.core.storage import Storage


def note(text: str, index: Optional[int] = None):
    """
    Add a note to a command.
    If index is not provided, adds note to the last command.
    """
    storage = Storage()
    flow = storage.current_flow
    
    if not flow:
        print("[yellow]No active flow found.[/yellow]")
        raise typer.Exit(code=1)
        
    if not flow.commands:
        print("[yellow]Flow is empty. Cannot add note.[/yellow]")
        raise typer.Exit(code=1)

    target_index = index if index is not None else len(flow.commands) - 1
    
    if flow.add_note_to_command(target_index, text):
        storage.save_flow(flow)
        print(f"[green]Added note to command {target_index}.[/green]")
    else:
        print(f"[red]Index {target_index} out of range.[/red]")
        raise typer.Exit(code=1)
