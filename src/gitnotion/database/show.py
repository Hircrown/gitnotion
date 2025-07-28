import typer
from typing import Optional
from typing_extensions import Annotated
from rich.console import Console
from rich.table import Table
from .utils import get_db_data, print_table

app = typer.Typer()

@app.command()#mostra il database passando il nome. aggiunta di flag come --headers --columns, --row --
def show(
    db_name: Annotated[
        str,
        typer.Argument(
            help="Name of the database to show",
            show_default=False
        )
    ],
    headers: Annotated[
        bool,
        typer.Option(
            help="Show the headers of the database",
            show_default=False
        )
    ] = False,
    columns: Annotated[
        Optional[list[str]],
        typer.Option(
            help="Show specific columns of the database",
            show_default=False
        )
    ] = None,
    rows: Annotated[
        tuple[int, int] | None,
        typer.Option(
            help="Show a specific number of rows from the database",
            show_default=False
        )
    ] = None,
    # Click supports nargs but Typer does not, so I can use a callback function 
    # to allow the user to pass an int. I had to use -n to modify the default 10 rows
    head: Annotated[
        bool,
        typer.Option(
            help="Show the first 10 rows of the database",
            show_default=False,
        )
    ] = None,
    tail: Annotated[
        bool,
        typer.Option(
            help="Show the last 10 rows of the database",
            show_default=False
        )
    ] = False,
    n: Annotated[
        Optional[int],
        typer.Option("-n",
            help="Number of rows to show. Must be used with --head or --tail to modify the default 10 rows",
            show_default=False
        )
    ] = None,
    index: Annotated[
        bool,
        typer.Option(
            help="Show the index of the database",
            show_default=False
        )
    ] = True
):
    """
    Show the current database data
    """
    data = get_db_data(db_name)
    if isinstance(data, FileNotFoundError):
        typer.secho(str(data), fg=typer.colors.RED)
        return
    db_headers = data.get("headers")
    db_rows = data.get("rows", [])
    if headers:
        # Just in case but it should never happen   
        if not db_headers:
            typer.secho("Database is empty", fg=typer.colors.RED)
            return
        db_rows = []
        index = False
    if columns:
        db_headers = columns
    if rows:
        db_rows = db_rows[rows[0]:rows[1]]
        index = False
    if head:
        if n:
            db_rows = db_rows[:n]
        else:
            db_rows = db_rows[:10]
    if tail:
        if n:
            db_rows = db_rows[-n:]
        else:
            db_rows = db_rows[-10:]

    print_table(db_name, db_headers, db_rows, show_index=index)