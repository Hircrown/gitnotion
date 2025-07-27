import typer
from typing_extensions import Annotated
from rich.prompt import Confirm
import copy
from .utils import delete_db, get_db_data, save_db, print_table

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
    initial_row = copy.deepcopy(existing_rows)
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
        print_table(db_name, headers, initial_row, deleted_rows=[row_index])


@delete_app.command("rows")
def delete_row(
    db_name: Annotated[
        str,
        typer.Argument(
            help="Name of the database to delete a row from",
            show_default=False
        )
    ],
    rows_index: Annotated[
        list[int],
        typer.Argument(
            min=0,
            help="List of indices of the rows to delete",
            show_default=False
        )
    ],
    force: Annotated[
        bool,
        typer.Option(
            "--force", "-f",
            help="Force delete the rows without confirmation",
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
    Delete specific rows from the database
    """
    if not force:
        confirm = Confirm.ask("[bold red]Are you sure you want to delete these rows?\n"
                    f"This action cannot be undone[/bold red]")
        if not confirm:
            typer.secho("Rows deletion cancelled.", fg=typer.colors.YELLOW)
            return
    data = get_db_data(db_name)
    if isinstance(data, FileNotFoundError):
        typer.secho(str(data), fg=typer.colors.RED)
        return
    
    headers = data.get("headers", [])
    existing_rows = data.get("rows", [])
    deleted_rows = []
    if not existing_rows:
        typer.secho("No rows found in the database.", fg=typer.colors.RED)
        return
    for row_index in rows_index:
        if row_index >= len(existing_rows):
            typer.secho(f"Row index {row_index} is out of range.", fg=typer.colors.RED)
            return
        deleted_rows.append(existing_rows[row_index])
    remaining_rows = [row for row in existing_rows if row not in deleted_rows]

    data["rows"] = remaining_rows
    save_db(db_name, data)
    typer.secho(f"Rows {rows_index} deleted successfully from database '{db_name}'.", fg=typer.colors.GREEN)
    if show_table:
        print_table(db_name, headers, existing_rows, deleted_rows=rows_index)

@delete_app.command("column")
def delete_column(
    db_name: Annotated[
        str,
        typer.Argument(
            help="Name of the database to delete a column from",
            show_default=False
        )
    ],
    column_name: Annotated[
        str,
        typer.Argument(
            help="Name of the column to delete",
            show_default=False
        )
    ],
    force: Annotated[
        bool,
        typer.Option(
            "--force", "-f",
            help="Force delete the column without confirmation",
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
    Delete a specific column from the database
    """
    if not force:
        confirm = Confirm.ask("[bold red]Are you sure you want to delete this column?\n"
                    f"This action cannot be undone[/bold red]")
        if not confirm:
            typer.secho("Column deletion cancelled.", fg=typer.colors.YELLOW)
            return
    data = get_db_data(db_name)
    if isinstance(data, FileNotFoundError):
        typer.secho(str(data), fg=typer.colors.RED)
        return
    
    headers = data.get("headers", [])
    initial_headers = headers.copy()
    existing_rows = data.get("rows", [])
    initial_rows = copy.deepcopy(existing_rows)
    
    if column_name not in headers:
        typer.secho(f"Column '{column_name}' does not exist in the database.", fg=typer.colors.RED)
        return

    index = headers.index(column_name)
    headers.pop(index)
    
    for row in existing_rows:
        try:
            row.pop(index)
        # If the pop index is out of range, it means the value for the column is missing
        # This can happen if the column was added later and some rows don't have that column
        # So we just skip that row
        except IndexError:
            continue

    data["headers"] = headers
    data["rows"] = existing_rows
    save_db(db_name, data)
    
    typer.secho(f"Column '{column_name}' deleted successfully from database '{db_name}'.", fg=typer.colors.GREEN)
    
    if show_table:
            print_table(db_name, initial_headers, initial_rows, deleted_columns=[column_name])

@delete_app.command("columns")
def delete_columns(
    db_name: Annotated[
        str,
        typer.Argument(
            help="Name of the database to delete columns from",
            show_default=False
        )
    ],
    columns: Annotated[
        list[str],
        typer.Argument(
            help="List of column names to delete",
            show_default=False
        )
    ],
    force: Annotated[
        bool,
        typer.Option(
            "--force", "-f",
            help="Force delete the columns without confirmation",
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
    Delete specific columns from the database
    """
    if not force:
        confirm = Confirm.ask("[bold red]Are you sure you want to delete these columns?\n"
                    f"This action cannot be undone[/bold red]")
        if not confirm:
            typer.secho("Columns deletion cancelled.", fg=typer.colors.YELLOW)
            return
    data = get_db_data(db_name)
    if isinstance(data, FileNotFoundError):
        typer.secho(str(data), fg=typer.colors.RED)
        return
    
    headers = data.get("headers", [])
    initial_headers = headers.copy()
    existing_rows = data.get("rows", [])
    initial_rows = copy.deepcopy(existing_rows)

    
    for column_name in columns:
        if column_name not in headers:
            typer.secho(f"Column '{column_name}' does not exist in the database.", fg=typer.colors.RED)
            continue
        
        index = headers.index(column_name)
        headers.pop(index)
        
        for row in existing_rows:
            try:
                row.pop(index)
            except IndexError:
                continue
    data["headers"] = headers
    data["rows"] = existing_rows
    save_db(db_name, data)

    typer.secho(f"Columns '{', '.join(columns)}' deleted successfully from database '{db_name}'.", fg=typer.colors.GREEN)
    if show_table:
        print_table(db_name, initial_headers, initial_rows, deleted_columns=columns)