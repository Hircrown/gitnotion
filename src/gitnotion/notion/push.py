import typer
from typing_extensions import Annotated

app = typer.Typer()

@app.command(name="push", rich_help_panel="Notion Commands")
def push_changes():
    """
    Push changes to a Notion database [b red]Not implemented yet[/b red]
    """
    pass