import typer
from typing_extensions import Annotated
from .utils import query_db
from ..database.utils import get_db_data
from rich import print_json

app = typer.Typer()

@app.command(rich_help_panel="Notion Commands")
def pull(
    db_name: Annotated[
        str,
        typer.Argument(
            help="Name of the database to retrive data from",
            show_default=False
        )
    ]
):
    """
    Pull changes from a Notion database [b red]Not implemented yet[/b red]
    """
    data = get_db_data(db_name)
    if isinstance(data, FileNotFoundError):
        typer.secho(str(data), fg=typer.colors.RED)
        return
    db_id = data.get("id", [])
    if not db_id:
        return
    data_notion = query_db(db_id)
    typer.echo(data_notion)
    print_json(data_notion)