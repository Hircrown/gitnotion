import typer
from typing_extensions import Annotated

app = typer.Typer()

@app.command()
def delete():
    typer.echo("Delete command")