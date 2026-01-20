import typer
from rich import print
from flowshot.core.storage import Storage

app = typer.Typer()

@app.command()
def save(name: str = typer.Argument(..., help="Flow name or file path"), 
         file: bool = typer.Option(False, "--file", "-f", help="Save as standalone JSON file")):
    """
    Save the current flow.
    If --file is used, saves to the specified path (as JSON).
    Otherwise, saves to internal storage with the given name.
    """
    storage = Storage()
    flow = storage.current_flow
    
    if not flow:
        print("[yellow]No active flow found.[/yellow]")
        raise typer.Exit(code=1)

    if file:
        # Save as artifact
        path = name
        if not path.endswith(".flow.json"):
            path += ".flow.json"
        try:
            with open(path, "w") as f:
                  f.write(flow.model_dump_json(indent=2))
            print(f"[green]Flow saved to file: {path}[/green]")
        except Exception as e:
            print(f"[red]Error saving file:[/red] {e}")
            raise typer.Exit(code=1)
    else:
        # Internal save
        old_name = flow.name
        flow.name = name
        storage.save_flow(flow)
        
        print(f"[green]Flow saved as '{name}'[/green]")
