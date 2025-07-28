import typer
from typing_extensions import Annotated
from .utils import get_db_data, save_db
from rich import print

app = typer.Typer()

@app.command()
def change(
    db_name: Annotated[
        str,
        typer.Argument(
            help="Name of the database where the value to be changed resides",
            show_default=False
        )
    ],
    header: Annotated[
        str,
        typer.Argument(
            help="Name of the column where the value to be changed resides",
            show_default=False
        )
    ],
    row_index: Annotated[
        int,
        typer.Argument(
            help="The index of the row where the value to be changed resides"
        )
    ],
    value: Annotated[
        str,
        typer.Argument(
            help="The new value",
            show_default=False
        )
    ]
):
    
    """
    Change the value of a specific cell
    """
    data = get_db_data(db_name)
    if isinstance(data, FileNotFoundError):
        typer.secho(str(data), fg=typer.colors.RED)
        return
    headers = data.get("headers", [])
    rows = data.get("rows", [])
    if header not in headers:
        typer.secho(f"Header '{header}' does not exist in {db_name}", fg=typer.colors.RED)
        return
    if not rows:
        typer.secho("No rows found in the database.", fg=typer.colors.RED)
        return
    if row_index >= len(rows):
        typer.secho(f"Row index {row_index} is out of range.", fg=typer.colors.RED)
        return

    header_index = headers.index(header)
    old_value = rows[row_index][header_index]
    rows[row_index][header_index] = value
    data["rows"] = rows
    save_db(db_name, data)
    print(f"The value [b green]{old_value}[/b green] has been changed to the value [b green]{value}[/b green]")
