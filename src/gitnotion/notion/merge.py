import typer
from typing_extensions import Annotated

app = typer.Typer()

@app.command("merge", rich_help_panel="Notion Commands")
def merge_databases():
    """
    Merge two databases [b red]Not implemented yet[/b red]
    """
    pass