import typer
import os
import shutil
import subprocess
from rich import print
from rich.prompt import Confirm
from flowshot.core.storage import Storage
from flowshot.core.validator import Validator


def _shell_executable() -> str | None:
    if os.name == "nt":
        return os.environ.get("COMSPEC") or shutil.which("cmd")
    return os.environ.get("SHELL") or shutil.which("bash") or shutil.which("sh")


def play(
    start_index: int = typer.Option(0, help="Start from specific index"),
    auto_approve: bool = typer.Option(False, "--yes", "-y", help="Auto-approve non-destructive commands")
):
    """
    Interactively play back the recorded flow.
    """
    storage = Storage()
    flow = storage.current_flow
    validator = Validator()
    
    if not flow:
        print("[yellow]No active flow found.[/yellow]")
        raise typer.Exit(code=1)

    commands_to_run = flow.commands[start_index:]
    if not commands_to_run:
        print("[yellow]No commands to play.[/yellow]")
        return

    print(f"[bold]Starting playback of flow:[/bold] {flow.name}")
    print(f"Queue: {len(commands_to_run)} items")
    
    for idx, cmd_obj in enumerate(commands_to_run):
        actual_idx = start_index + idx
        
        if cmd_obj.type == "step":
            print(f"\n[bold blue]--- Step: {cmd_obj.cmd} ---[/bold blue]")
            continue
            
        cmd = cmd_obj.cmd
        print(f"\n[cyan]({actual_idx}) Next:[/cyan] {cmd}")
        
        # Validate
        warnings = validator.validate_command(cmd)
        is_destructive = False
        for w in warnings:
            print(f"[red bold]WARNING:[/red bold] {w}")
            if "Destructive" in w:
                is_destructive = True
        
        # Helper logic for auto-approve
        # We only auto-approve if NOT destructive
        if auto_approve and not is_destructive:
            should_run = True
        else:
            should_run = Confirm.ask("Execute this command?", default=True)
            
        if should_run:
            try:
                print(f"[dim]Running...[/dim]")
                # Use shell=True to support pipes/redirects captured in history
                subprocess.run(cmd, shell=True, check=True, executable=_shell_executable())
            except subprocess.CalledProcessError as e:
                print(f"[red]Command failed with exit code {e.returncode}[/red]")
                if not Confirm.ask("Continue execution?", default=False):
                    print("[red]Playback aborted.[/red]")
                    break
        else:
            print("[yellow]Skipped.[/yellow]")
            
    print("\n[green]Playback complete.[/green]")
