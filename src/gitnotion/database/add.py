import typer
from typing_extensions import Annotated
from utils import get_db_data  

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
    for header in headers:
        value = typer.prompt(f"Enter value for {header}")
        data["db"][header] = value
    save_db(db_name, data)
    typer.echo(f"Data added to {db_name} database", fg=typer.colors.GREEN)