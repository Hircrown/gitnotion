import typer
from rich.prompt import Prompt, Confirm
from typing_extensions import Annotated
from utils import get_db_data, save_db, rename_db, print_headers

app = typer.Typer()
rename_app = typer.Typer()
app.add_typer(rename_app, name="rename")

#nome database
#nome header o headers

@rename_app.command("db")
def rename_database(
    db_name: Annotated[
        str,
        typer.Argument(
            help="Name of the database to rename",
            show_default=False
        )
    ],
    new_name: Annotated[
        str,
        typer.Argument(
            help="New name for the database",
            show_default=False
        )
    ]
):
    """
    Rename an existing database
    """
    try:
        rename_db(db_name, new_name)
        typer.secho(f"Database '{db_name}' renamed to '{new_name}'", fg=typer.colors.BRIGHT_GREEN)
    except FileNotFoundError as e:
        typer.secho(str(e), fg=typer.colors.RED)
        return
    
@rename_app.command("header")
def rename_header(
    db_name: Annotated[
        str,
        typer.Argument(
            help="Name of the database to rename header in",
            show_default=False
        )
    ],
    header: Annotated[
        str,
        typer.Argument(
            help="Header to rename",
            show_default=False
        )
    ],
    new_header: Annotated[
        str,
        typer.Argument(
            help="New name for the header",
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
    Rename a header in the database
    """
    data = get_db_data(db_name)
    if isinstance(data, FileNotFoundError):
        typer.secho(str(data), fg=typer.colors.RED)
        return
    headers = data.get("headers", [])
    if header not in headers:
        typer.secho(f"Header '{header}' does not exist in {db_name}", fg=typer.colors.RED)
        return
    if new_header in headers:
        confirm = Confirm.ask(f"There is already a header named '{new_header}' in {db_name}.\n"
                    f"[bold orange1]Are you sure you want to rename '{header}' to '{new_header}'?[/bold orange1]")
        if not confirm:
            return
    headers[headers.index(header)] = new_header
    data["headers"] = headers
    save_db(db_name, data)
    typer.secho(f"Header '{header}' renamed to '{new_header}' in {db_name}", fg=typer.colors.BRIGHT_GREEN)
    if show_table:
        print_headers(db_name, headers, [new_header])


@rename_app.command("headers")
def rename_headers(
    db_name: Annotated[
        str,
        typer.Argument(
            help="Name of the database to rename header in",
            show_default=False
        )
    ],
    headers: Annotated[
        list[str],
        typer.Argument(
            help="List of headers to rename",
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
    Rename a list of headers in the database
    """
    data = get_db_data(db_name)
    if isinstance(data, FileNotFoundError):
        typer.secho(str(data), fg=typer.colors.RED)
        return
    new_headers = []
    old_headers = data.get("headers", [])
    for header in headers:
        if header not in old_headers:
            typer.secho(f"Header '{header}' does not exist in {db_name}", fg=typer.colors.RED)
            return
        new_header = Prompt.ask(f"Change [bold orange1]{header}[/bold orange1] into")
        if new_header in old_headers:
            confirm = Confirm.ask(f"There is already a header named '{new_header}' in {db_name}.\n"
                        f"[bold orange1]Are you sure you want to rename '{header}' to '{new_header}'?[/bold orange1]")
            if not confirm:
                return
        new_headers.append(new_header)
        # Rename the header
        old_headers[old_headers.index(header)] = new_header
    data["headers"] = old_headers
    save_db(db_name, data)
    typer.secho(f"Headers '{' '.join(headers)}' renamed to '{' '.join(new_headers)}' in {db_name}", fg=typer.colors.BRIGHT_GREEN)
    if show_table:
        print_headers(db_name, old_headers, new_headers)