import typer
from typing_extensions import Annotated
from .utils import get_db_data, save_db, print_table
app = typer.Typer()
add_app = typer.Typer()
app.add_typer(add_app, name="add", help="Add data to a database")


@add_app.command("row")
def add_row(
    db_name: Annotated[
        str,
        typer.Argument(
            help="Name of the database to add data to",
            show_default=False
        )
    ],
    show_table: Annotated[
        bool,
        typer.Option(
            help="Show the changes in a table format",
            show_default=False
        )
    ] = True
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
    all_rows = data.get("rows", [])
    index = len(all_rows) - 1
    save_db(db_name, data)
    typer.secho(f"Data added to {db_name} database", fg=typer.colors.GREEN)
    if show_table:
        print_table(db_name, headers, all_rows, added_rows=[index])



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
    ],
    show_table: Annotated[
        bool,
        typer.Option(
            help="Show the changes in a table format",
            show_default=False
        )
    ] = True
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
    if not headers:
        typer.secho("Database is empty", fg=typer.colors.RED)
        return 
    rows = []
    for i in range(n_rows):
        row = [] 
        typer.secho(f"\nRow {i+1}", fg=typer.colors.BRIGHT_YELLOW)
        for header in headers:
            value = typer.prompt(f"Enter value for {header}")
            row.append(value)
        rows.append(row)
    data["rows"].extend(rows)
    all_rows = data.get("rows", [])
    index = list(range(len(all_rows) - n_rows, len(all_rows)))
    print(index)
    save_db(db_name, data)
    typer.secho(f"Data added to {db_name} database", fg=typer.colors.GREEN)
    if show_table:
        print_table(db_name, headers, all_rows, added_rows=index)


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
    ],
    show_table: Annotated[
        bool,
        typer.Option(
            help="Show the changes in a table format",
            show_default=False
        )
    ] = True
):
    """
    Add a new header to the database
    """
    data = get_db_data(db_name)
    if isinstance(data, FileNotFoundError):
        typer.secho(str(data), fg=typer.colors.RED)
        return
    existing_headers = data.get("headers", [])
    if header in existing_headers:
        typer.secho(f"{header} is already a header in {db_name}", fg=typer.colors.RED)
        return
    existing_headers.append(header)
    data["headers"] = existing_headers
    save_db(db_name, data)
    typer.secho(f"Adding {header} to {db_name} database", fg=typer.colors.GREEN)
    if show_table:
        print_table(db_name, existing_headers, [], added_headers=[header])


@add_app.command("headers")
def add_headers(
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
    ],
    show_table: Annotated[
        bool,
        typer.Option(
            help="Show the changes in a table format",
            show_default=False
        )
    ] = True
):
    """
    Add multiple headers to the database
    """
    data = get_db_data(db_name)
    if isinstance(data, FileNotFoundError):
        typer.secho(str(data), fg=typer.colors.RED)
        return
    existing_headers = data.get("headers", [])
    duplicates_headers = [header for header in headers if header in existing_headers]
    unique_headers = [header for header in headers if header not in existing_headers]
    if duplicates_headers:
        typer.secho(f"{' '.join(duplicates_headers)} are already headers in {db_name}", fg=typer.colors.RED)
        if not unique_headers:
            typer.secho(f"All headers are already present in {db_name}", fg=typer.colors.RED)
            return
    existing_headers.extend(unique_headers)
    data["headers"] = existing_headers
    save_db(db_name, data)
    typer.secho(f"Adding {unique_headers} to {db_name} database", fg=typer.colors.GREEN)
    if show_table:
        print_table(db_name, existing_headers, [], added_headers=unique_headers)