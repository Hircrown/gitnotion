import typer
from typing_extensions import Annotated
from rich.prompt import Confirm
from utils import delete_db, get_db_data, save_db, print_rows, print_headers

app = typer.Typer()
delete_app = typer.Typer()
app.add_typer(delete_app, name="delete")



@delete_app.command("db")
def delete_database(
    db_name: Annotated[
        str,
        typer.Argument(
            help="Name of the database to delete",
            show_default=False
        )
    ],
    force: Annotated[
        bool,
        typer.Option(
            "--force", "-f",
            help="Force delete the database without confirmation",
            show_default=False
        )
    ] = False
):
    """
    Delete a database by its name
    """
    if not force:
        confirm = Confirm.ask("[bold red]Are you sure you want to delete this database?\n"
                              f"This action cannot be undone[/bold red]")
        if not confirm:
            typer.secho("Database deletion cancelled.", fg=typer.colors.YELLOW)
            return
    try:
        delete_db(db_name)
        typer.secho(f"Database '{db_name}' deleted successfully.", fg=typer.colors.GREEN)
    except FileNotFoundError as e:
        typer.secho(str(e), fg=typer.colors.RED)
        return
    

@delete_app.command("row")
def delete_row(
    db_name: Annotated[
        str,
        typer.Argument(
            help="Name of the database to delete a row from",
            show_default=False
        )
    ],
    row_index: Annotated[
        int,
        typer.Argument(
            min=0,
            help="Index of the row to delete",
            show_default=False
        )
    ],
    force: Annotated[
        bool,
        typer.Option(
            "--force", "-f",
            help="Force delete the row without confirmation",
            show_default=False,
        )
    ] = False,
    show_table: Annotated[
        bool,
        typer.Option(
            help="Show the changes in a table format",
            show_default=False
        )
    ] = True
):
    """
    Delete a specific row from the database
    """
    if not force:
        confirm = Confirm.ask("[bold red]Are you sure you want to delete this row?\n"
                    f"This action cannot be undone[/bold red]")
        if not confirm:
            typer.secho("Row deletion cancelled.", fg=typer.colors.YELLOW)
            return
    data = get_db_data(db_name)
    if isinstance(data, FileNotFoundError):
        typer.secho(str(data), fg=typer.colors.RED)
        return
    
    headers = data.get("headers", [])
    existing_rows = data.get("rows", [])
    initial_row = existing_rows.copy()
    if not existing_rows:
        typer.secho("No rows found in the database.", fg=typer.colors.RED)
        return
    if row_index >= len(existing_rows):
        typer.secho(f"Row index {row_index} is out of range.", fg=typer.colors.RED)
        return

    existing_rows.pop(row_index)
    data["rows"] = existing_rows
    save_db(db_name, data)
    typer.secho(f"Row {row_index} deleted successfully from database '{db_name}'.", fg=typer.colors.GREEN)
    if show_table:
        print_rows(db_name, headers, initial_row, deleted=[row_index])