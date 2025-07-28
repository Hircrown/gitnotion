import typer
from .add import app as add
from .change import app as change
from .create import app as create
from .delete import app as delete
from .list import app as list
from .rename import app as rename
from .show import app as show


app = typer.Typer()

app.add_typer(add)
app.add_typer(change)
app.add_typer(create)
app.add_typer(delete)
app.add_typer(list)
app.add_typer(rename)
app.add_typer(show)