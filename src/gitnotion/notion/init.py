import typer
from typing_extensions import Annotated
from .utils import init_db, db_title, db_headers, last_time_edited
from ..database.utils import save_db
from rich.prompt import Prompt, Confirm

app = typer.Typer(rich_help_panel="Notion Commands")


@app.command()
def init(
    db_url: Annotated[
        str,
        typer.Argument(
            help="Insert the [b orange1]full URL[/b orange1] of the database. " \
            "Make sure you have opened the database in [b orange1]full page view[/b orange1].",
            show_default=False
        )
    ]

):
    """
    Initialize a Notion database.
    First command to run to start interact with an existing Notion database
    """
    res = init_db(db_url)
    typer.echo(type(res))
    if isinstance(res, dict):
        title = db_title(res)
        data = {
            "headers": db_headers(res),
            "rows": [],
            "last time edited": last_time_edited(res)
        }
        if title == "No title":
            confirm = Confirm.ask(f"The database is called [b]{title}[/b] because no title was found\nWould you like to give it one now?\nOtherwise, it will be saved as [b]{title}[/b]")
            if confirm:
                title = Prompt.ask("Type the database title")
        save_db(title, data)
        typer.echo(f"The {title} database has been initialized successfully!\n \
                   Use the pull command to retrive all the rows")