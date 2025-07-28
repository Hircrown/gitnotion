import typer
from typing_extensions import Annotated

app = typer.Typer()

@app.command("commit", rich_help_panel="Notion Commands")
def commit_changes():
    """
    Commit changes to a Notion database [b red]Not implemented yet[/b red]
    """
    pass
        