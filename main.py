import typer
from flowshot.cli import start, stop, status, list, drop, note, export, save, load

app = typer.Typer(
    name="flowshot",
    help="FlowShotCLI: Terminal workflow recorder and script generator.",
    no_args_is_help=True
)

app.command(name="start")(start.start)
app.command(name="stop")(stop.stop)
app.command(name="status")(status.status)
app.command(name="list")(list.list_commands)
app.command(name="drop")(drop.drop)
app.command(name="note")(note.note)
app.command(name="export")(export.export)
app.command(name="save")(save.save)
app.command(name="load")(load.load)

# Phase 2 Commands
from flowshot.cli import step, play
app.command(name="step")(step.step)
app.command(name="play")(play.play)

# AI Commands (Conditional)
from flowshot.core.ai import AI
if AI().is_available():
    from flowshot.cli import ai_cmds
    app.command(name="explain")(ai_cmds.explain)
    app.command(name="summarize")(ai_cmds.summarize)
    app.command(name="title")(ai_cmds.title)

if __name__ == "__main__":
    app()
