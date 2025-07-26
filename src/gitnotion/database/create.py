import typer
from typing_extensions import Annotated
from utils import check_exists, save_db, DB_PATH

app = typer.Typer()

#questa testa con tutto anche i due flag combinati e fuziona
@app.command()
def create(
    name: Annotated[
        str, typer.Argument(
            help="Database name" #mi creerà problemi avere un nome con lo spazio?
        )
    ],
    headers: Annotated[
        list[str],
        typer.Argument(
            help="Database headers"
        )
    ],
    overwrite: Annotated[
        bool,
        typer.Option(
            "--overwrite", "-o",
            help="Force the creation of the database by overwriting the current database"
        )
    ] = False,
    force: Annotated[
        bool,
        typer.Option(
            "--force", "-f",
            help="Force the database overwrite without asking for confirmation. It needs to be used with --overwrite",
        )
    ] = False
):
    """
    Create a new database with the specified headers
    """
    if check_exists(f"{DB_PATH}/{name}.pkl"):
        if not overwrite:
            typer.echo(f"The {name} database already exists\n" +
                       "Use the --overwrite flag to overwrite the existing database")
            return
        if overwrite:
            if not force:                
                confirm = typer.confirm(f"Are you sure you want to overwrite {name}? This operation cannot be undone.",
                                       abort=True)
            typer.echo(f"Overwriting the {name} database...")
    # When the database is created, it will be a dictionary with headers and rows
    db = {"headers": headers,
          "rows": []}    
    save_db(name, db)
    typer.echo(f"Name: {name}, Headers: {headers}")

