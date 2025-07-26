import typer
from database import app as db

app = typer.Typer()

app.add_typer(db)


if __name__ == "__main__":
    app()