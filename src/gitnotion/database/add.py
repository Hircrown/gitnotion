import typer
from typing_extensions import Annotated
from utils import get_db_data, save_db

app = typer.Typer()
add_app = typer.Typer()
app.add_typer(add_app, name="add")

@add_app.command("row")
def add_row(
    db_name: Annotated[
        str,
        typer.Argument(
            help="Name of the database to add data to",
            show_default=False
        )
    ]
):
    """
    Add a row to the specified database
    """

    data = get_db_data(db_name)
    if isinstance(data, FileNotFoundError):
        typer.secho(str(data), fg=typer.colors.RED)
        return
    headers = data.get("headers", [])
    # Just in case but it should never happen
    if not headers:
        typer.secho("Database is empty", fg=typer.colors.RED)
        return 
    row = [] 
    for header in headers:
        value = typer.prompt(f"Enter value for {header}")
        row.append(value)
    data["rows"].append(row)
    save_db(db_name, data)
    typer.secho(f"Data added to {db_name} database", fg=typer.colors.GREEN)


@add_app.command("rows")
def add_rows(
    db_name: Annotated[
        str,
        typer.Argument(
            help="Name of the database to add data to",
            show_default=False
        )
    ],
    n_rows: Annotated[
        int,
        typer.Argument(
            min=2,
            help="Number of rows to add to the database",
            show_default=False
        )
    ]
):
    """
    Add multiple rows to the specified database
    """

    data = get_db_data(db_name)
    if isinstance(data, FileNotFoundError):
        typer.secho(str(data), fg=typer.colors.RED)
        return
    headers = data.get("headers", [])
    # Just in case but it should never happen
    if headers == []:
        typer.secho("Database is empty", fg=typer.colors.RED)
        return 
    for i in range(n_rows):
        row = [] 
        typer.secho(f"\nRow {i+1}", fg=typer.colors.BRIGHT_YELLOW)
        for header in headers:
            value = typer.prompt(f"Enter value for {header}")
            row.append(value)
        data["rows"].append(row)
        save_db(db_name, data)
    typer.secho(f"Data added to {db_name} database", fg=typer.colors.GREEN)


@add_app.command("header")
def add_header(
    db_name: Annotated[
        str,
        typer.Argument(
            help="Name of the database to add data to",
            show_default=False
        )
    ],
    header: Annotated[
        str,
        typer.Argument(
            help="Header to add to the database",
            show_default=False
        )
    ]
):
    """
    Add a new header to the database
    """
    data = get_db_data(db_name)
    existing_headers = data["headers"]
    if isinstance(existing_headers, FileNotFoundError):
        typer.secho(str(existing_headers), fg=typer.colors.RED)
        return
    if header in existing_headers:
        typer.secho(f"{header} is already a header in {db_name}", fg=typer.colors.RED)
        return
    existing_headers.append(header)
    data["headers"] = existing_headers
    save_db(db_name, data)
    typer.secho(f"Adding {header} to {db_name} database", fg=typer.colors.GREEN)


@add_app.command("headers")
def add_header(
    db_name: Annotated[
        str,
        typer.Argument(
            help="Name of the database to add data to",
            show_default=False
        )
    ],
    headers: Annotated[
        list[str],
        typer.Argument(
            help="Headers to add to the database",
            show_default=False
        )
    ]
):
    """
    Add multiple headers to the database
    """
    data = get_db_data(db_name)
    existing_headers = data["headers"]
    duplicates_headers = [header for header in headers if header in existing_headers]
    unique_headers = [header for header in headers if header not in existing_headers]
    if isinstance(existing_headers, FileNotFoundError):
        typer.secho(str(existing_headers), fg=typer.colors.RED)
        return
    if duplicates_headers:
        typer.secho(f"{' '.join(duplicates_headers)} are already headers in {db_name}", fg=typer.colors.RED)
        if not unique_headers:
            typer.secho(f"All headers are already present in {db_name}", fg=typer.colors.RED)
            return
    existing_headers.extend(unique_headers)
    data["headers"] = existing_headers
    save_db(db_name, data)
    typer.secho(f"Adding {unique_headers} to {db_name} database", fg=typer.colors.GREEN)