from rich import print
from flowshot.core.storage import Storage
from flowshot.core.flow import Command

def step(name: str):
    """
    Insert a conceptual step/section marker into the flow.
    """
    storage = Storage()
    flow = storage.current_flow
    
    if not flow:
        print("[yellow]No active flow found.[/yellow]")
        return # Typer exit handled by caller if needed, or we just return
        
    # Steps are just commands with type="step"
    # We append it to the end of the flow commands list
    cmd = Command(cmd=name, type="step")
    flow.commands.append(cmd)
    storage.save_flow(flow)
    
    print(f"[green]Added step:[/green] {name}")
