import typer
from rich import print
from flowshot.core.storage import Storage


def status():
    """
    Show current recording status.
    """
    storage = Storage()
    state = storage.data.recorder_state

    if state.is_recording:
        print(f"[green]Recording is ACTIVE.[/green]")
        if state.current_flow_id:
             print(f"Current Flow ID: {state.current_flow_id}")
        if state.history_file_path:
             print(f"Watching: {state.history_file_path}")
    else:
        print("[yellow]Recording is INACTIVE.[/yellow]")
        if state.current_flow_id:
             print(f"Last modified flow: {state.current_flow_id}")
