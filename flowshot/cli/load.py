import typer
from rich import print
from flowshot.core.storage import Storage
import json
from flowshot.core.flow import Flow

app = typer.Typer()

@app.command()
def load(name: str = typer.Argument(..., help="Flow name or file path"),
         file: bool = typer.Option(False, "--file", "-f", help="Load from standalone JSON file")):
    """
    Load a saved flow.
    If --file is used, loads from the specified JSON file.
    Otherwise, loads from internal storage by name.
    """
    storage = Storage()
    
    target_flow = None
    
    if file:
        # Load from artifact
        try:
            with open(name, "r") as f:
                content = f.read()
                target_flow = Flow.model_validate_json(content)
            # We save it to storage so it becomes the current flow?
            # Or just set it as current flow without saving to DB yet?
            # "Allow executing a flow file via CLI" -> Load implies making it active.
            # Let's save it to storage with its ID so it becomes active.
            storage.save_flow(target_flow)
        except Exception as e:
            print(f"[red]Error loading file:[/red] {e}")
            raise typer.Exit(code=1)

    else:
        # Find flow by name
        for flow in storage.data.flows.values():
            if flow.name == name:
                target_flow = flow
                break
                
        if not target_flow:
            print(f"[red]Flow '{name}' not found.[/red]")
            print("Available flows:")
            for f in storage.data.flows.values():
                print(f" - {f.name} ({f.id[:8]})")
            raise typer.Exit(code=1)
        
    storage.update_recorder_state(
        is_recording=storage.data.recorder_state.is_recording, 
        current_flow_id=target_flow.id
    )
    
    if storage.data.recorder_state.is_recording:
        print(f"[yellow]Warning: You are currently recording. Switched active context to '{target_flow.name}'.[/yellow]")
    else:
        if file:
            print(f"[green]Imported and loaded flow from file '{name}'.[/green]")
        else:
            print(f"[green]Loaded flow '{name}'.[/green]")
