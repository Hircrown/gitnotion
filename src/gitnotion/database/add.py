import typer
from typing_extensions import Annotated

app = typer.Typer()

@app.command()
def add():
    typer.echo("Add command")