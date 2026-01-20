from rich import print
from flowshot.core.storage import Storage
from flowshot.core.ai import AI

def explain():
    """
    [AI] Explain what the current flow does.
    """
    storage = Storage()
    flow = storage.current_flow
    if not flow:
        print("[yellow]No flow to explain.[/yellow]")
        return
        
    ai = AI()
    print("[dim]Generating explanation...[/dim]")
    response = ai.explain(flow)
    print(f"\n[bold]Explanation:[/bold]\n{response}")

def summarize():
    """
    [AI] Summarize the flow in one sentence.
    """
    storage = Storage()
    flow = storage.current_flow
    if not flow:
        print("[yellow]No flow to summarize.[/yellow]")
        return
        
    ai = AI()
    print("[dim]Generating summary...[/dim]")
    response = ai.summarize(flow)
    print(f"\n[bold]Summary:[/bold] {response}")

def title():
    """
    [AI] Generate a filename for this flow.
    """
    storage = Storage()
    flow = storage.current_flow
    if not flow:
        print("[yellow]No flow to title.[/yellow]")
        return

    ai = AI()
    print("[dim]Generating title...[/dim]")
    response = ai.generate_title(flow)
    print(f"\n[bold]Suggested Title:[/bold] {response}")
