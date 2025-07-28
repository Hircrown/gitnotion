import typer
from gitnotion.database import app as db
from gitnotion.notion import app as notion

app = typer.Typer(rich_markup_mode="rich")

app.add_typer(db)
app.add_typer(notion, rich_help_panel="Notion")


if __name__ == "__main__":
    app()