import typer
from typing import Optional
from typing_extensions import Annotated
from rich.console import Console
from rich.table import Table
from utils import get_db_data

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
        Optional[int],
        typer.Option(
            help="Show a specific number of rows from the database",
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
    if headers:
        headers = data.get("headers")
        # Just in case but it should never happen   
        if headers == []:
            typer.secho("Database is empty", fg=typer.colors.RED)
            return
        typer.echo(f"Current database headers: {headers}")
    elif columns:
        pass
    elif rows:
        pass
    else:
        console = Console()
        table = Table(title = db_name,show_header=True, header_style="bold deep_sky_blue1")
        headers = data.get("headers", [])
        if index:
            headers.insert(0, "Index")
        for header in headers:
            table.add_column(header)

        for i, row in enumerate(data.get("rows", [])):
            if index:
                table.add_row(str(i), *[str(item) for item in row])
            else:
                table.add_row(*[str(item) for item in row])
        
        console.print(table)