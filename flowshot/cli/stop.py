import typer
from rich import print
from flowshot.core.storage import Storage
from flowshot.core.recorder import Recorder


def stop():
    """
    Stop recording and capture new commands.
    """
    storage = Storage()
    recorder = Recorder(storage)

    if not recorder.is_recording():
        print("[yellow]Not currently recording.[/yellow]")
        raise typer.Exit(code=1)

    try:
        flow = recorder.stop()
        count = len(flow.commands)
        print(f"[green]Recording stopped.[/green]")
        print(f"Captured [bold]{count}[/bold] commands.")
        if count > 0:
            print("Run [bold]flowshot list[/bold] to review or [bold]flowshot export[/bold] to save.")
    except Exception as e:
        print(f"[red]Error stopping recording:[/red] {e}")
        raise typer.Exit(code=1)
