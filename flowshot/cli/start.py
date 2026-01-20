import typer
from rich import print
from flowshot.core.storage import Storage
from flowshot.core.recorder import Recorder


def start():
    """
    Start recording shell commands. 
    Reads from your shell history file.
    """
    storage = Storage()
    recorder = Recorder(storage)

    if recorder.is_recording():
        print("[red]Already recording![/red] Run [bold]flowshot stop[/bold] first.")
        raise typer.Exit(code=1)

    try:
        hist_path = recorder.start()
        print(f"[green]FlowShot recording started![/green]")
        print(f"Watching history file: [blue]{hist_path}[/blue]")
        print("Run commands in your shell, then [bold]flowshot stop[/bold] when done.")
    except Exception as e:
        print(f"[red]Error starting recording:[/red] {e}")
        raise typer.Exit(code=1)
