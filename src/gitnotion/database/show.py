import typer
from typing import Optional
from typing_extensions import Annotated
from rich.console import Console
from rich.table import Table
from utils import get_headers

app = typer.Typer()

@app.command()#mostra il database passando il nome. aggiunta di flag come --headers --columns, --row --
def show(
    db_name: Annotated[
        str,
        typer.Argument(
            help="Name of the database to show"
        )
    ],
    headers: Annotated[
        bool,
        typer.Option(
            help="Show the headers of the database"
        )
    ],
    columns: Annotated[
        Optional[list[str]],
        typer.Option(
            help="Show specific columns of the database"
        )
    ],
    rows: Annotated[
        Optional[int],
        typer.Option(
            help="Show a specific number of rows from the database"
        )
    ]
):
    """
    Show the current database data
    """
    if headers:
        headers = get_headers(db_name)
        if isinstance(headers, FileNotFoundError):
            typer.secho(str(headers), fg=typer.colors.RED)
            return
        #L'evenienza [] non dovrebbe mai verificarsi    
        if headers == []:
            typer.secho("Database is empty", fg=typer.colors.RED)
            return
        typer.echo(f"Current database headers: {headers}")