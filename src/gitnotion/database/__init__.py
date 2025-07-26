import typer
from .add import app as add
from .create import app as create
from .delete import app as delete
from .show import app as show



app = typer.Typer()
app.add_typer(add)
app.add_typer(create)
app.add_typer(delete)
app.add_typer(show)