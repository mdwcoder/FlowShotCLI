import typer
from rich import print
from rich.prompt import Confirm
from typing import Optional
from flowshot.core.storage import Storage
from flowshot.core.exporter import Exporter
from flowshot.core.sanitizer import Sanitizer
from flowshot.core.variables import VariableDetector
from flowshot.core.validator import Validator

def export(
    bash: bool = typer.Option(False, "--bash", help="Export as Bash script"),
    zsh: bool = typer.Option(False, "--zsh", help="Export as Zsh script"),
    stdout: bool = typer.Option(False, "--stdout", help="Print to stdout instead of file"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview without saving"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output filename"),
    preset: str = typer.Option("local", help="Export preset: local, ci, safe"),
    with_vars: bool = typer.Option(False, "--with-vars", help="Detect and extract variables")
):
    """
    Export the current flow to a shell script.
    """
    if bash and zsh:
        print("[red]Cannot specify both --bash and --zsh[/red]")
        raise typer.Exit(code=1)
        
    target_shell = "zsh" if zsh else "bash"
    
    storage = Storage()
    flow = storage.current_flow
    
    if not flow:
        print("[yellow]No active flow found.[/yellow]")
        raise typer.Exit(code=1)
        
    if not flow.commands:
        print("[yellow]Flow is empty.[/yellow]")
        raise typer.Exit(code=1)

    # Validation
    validator = Validator()
    results = validator.validate_flow(flow)
    if results:
        print("[bold red]Validation Warnings:[/bold red]")
        for idx, cmd, warning in results:
            print(f"  Item {idx} ('{cmd}'): {warning}")
        
        if not Confirm.ask("Proceed with export?", default=False):
            raise typer.Exit(code=1)

    # Variables Detection
    variables = {}
    if with_vars:
        detector = VariableDetector()
        found = detector.detect_variables(flow)
        if found:
            print(f"[cyan]Detected potentially reusable variables:[/cyan]")
            for k, v in found.items():
                print(f"  {k} = {v}")
            if Confirm.ask("Extract these variables?"):
                variables = found

    # Sanitize first
    sanitizer = Sanitizer()
    safe_flow = sanitizer.sanitize_flow(flow)
    
    # Generate content
    exporter = Exporter()
    script_content = exporter.export(safe_flow, shell=target_shell, preset=preset, variables=variables)
    
    if stdout or dry_run:
        print(script_content)
        return

    # Determine filename
    filename = output
    if not filename:
        ext = "sh" if target_shell == "bash" else "zsh"
        filename = f"flow_{flow.id[:8]}.{ext}"
        
    try:
        with open(filename, "w") as f:
            f.write(script_content)
            # Make executable
            import os
            import stat
            st = os.stat(filename)
            os.chmod(filename, st.st_mode | stat.S_IEXEC)
            
        print(f"[green]Exported to {filename}[/green] (Preset: {preset})")
    except Exception as e:
        print(f"[red]Error saving file:[/red] {e}")
        raise typer.Exit(code=1)
