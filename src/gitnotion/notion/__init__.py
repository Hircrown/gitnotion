import typer
from .clone import app as clone
from .commit import app as commit
from .init import app as init
from .merge import app as merge
from .pull import app as pull
from .push import app as push

app = typer.Typer()

app.add_typer(clone)
app.add_typer(commit)
app.add_typer(init)
app.add_typer(merge)
app.add_typer(pull)
app.add_typer(push)
