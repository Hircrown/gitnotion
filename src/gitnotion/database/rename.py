import typer
from typing_extensions import Annotated
from utils import get_db_data, save_db, get_db_names, rename_db

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
