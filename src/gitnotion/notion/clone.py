import typer
from typing_extensions import Annotated

app = typer.Typer()

@app.command(rich_help_panel="Notion Commands")
def clone():
    """
    Clone a Notion database [b red]Not implemented yet[/b red]
    """
              
    pass