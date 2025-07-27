import os
import typer 
from typing_extensions import Annotated
from .utils import get_db_names

app = typer.Typer()

@app.command()
def list():
    """
    List all databases
    """
    try:
        names = get_db_names()
        typer.echo(f"Database names: {names}")
    except FileNotFoundError as e:
        typer.secho(str(e), fg=typer.colors.RED)

    