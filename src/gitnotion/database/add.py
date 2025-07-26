import typer
from typing_extensions import Annotated
from utils import get_db_data, save_db

app = typer.Typer()

@app.command()
def add(
    db_name: Annotated[
        str,
        typer.Argument(
            help="Name of the database to add data to"
        )
    ],
):
    """
    Add data to the specified database.
    """
    # headers = get_headers(db_name)
    # if isinstance(headers, FileNotFoundError):
    #     typer.secho(str(headers), fg=typer.colors.RED)
    #     return
    data = get_db_data(db_name)
    if isinstance(data, FileNotFoundError):
        typer.secho(str(data), fg=typer.colors.RED)
        return
    headers = data.get("headers", [])
    # Just in case but it should never happen
    if headers == []:
        typer.secho("Database is empty", fg=typer.colors.RED)
        return 
    row = [] 
    for header in headers:
        value = typer.prompt(f"Enter value for {header}")
        row.append(value)
    data["rows"].append(row)
    save_db(db_name, data)
    typer.secho(f"Data added to {db_name} database", fg=typer.colors.GREEN)