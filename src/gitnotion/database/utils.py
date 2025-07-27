import os
import pickle
from rich.console import Console
from rich.table import Table

CONFIG_PATH = os.getcwd()
DB_PATH = f"{CONFIG_PATH}/.database"

d = {"headers": ["index", "task", "status", "due_date"]}

def check_exists(path: str) -> bool:
    return os.path.exists(path)

def save_db(db_name: str, data: dict):
    if not check_exists(DB_PATH):
        os.makedirs(DB_PATH)
    with open(f"{DB_PATH}/{db_name}.pkl", "wb") as f:
        pickle.dump(data, f)

def load_db(db_name: str) -> dict:
    if not check_exists(f"{DB_PATH}/{db_name}.pkl"):
        raise FileNotFoundError(f"Database '{db_name}' does not exist.")
    with open(f"{DB_PATH}/{db_name}.pkl", "rb") as f:
        return pickle.load(f)

def get_headers(db_name: str) -> list[str]:
    try:
        db = load_db(db_name)
        return db.get("headers", [])
    except FileNotFoundError as e:
        return e

def get_db_data(db_name: str) -> dict:
    try:
        data = load_db(db_name)
        return data
    except FileNotFoundError as e:
        return e
    
def get_db_names(path: str=DB_PATH) -> list[str]:
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"No database found")
    dbs = [file for file in os.listdir(path) if file.split(".")[-1] == "pkl"]
    names = list(map(lambda x: x.split(".")[0], dbs))
    return names

def rename_db(db_name: str, new_name: str):
    print(os.path.exists(f"{DB_PATH}/{db_name}.pkl"))
    if not os.path.exists(f"{DB_PATH}/{db_name}.pkl"):
        raise FileNotFoundError(f"Database '{db_name}' does not exist.")
    os.rename(f"{DB_PATH}/{db_name}.pkl", f"{DB_PATH}/{new_name}.pkl")

def delete_db(db_name: str):
    if not os.path.exists(f"{DB_PATH}/{db_name}.pkl"):
        raise FileNotFoundError(f"Database '{db_name}' does not exist.")
    os.remove(f"{DB_PATH}/{db_name}.pkl")


#--------------RICK UTILS----------------
def print_headers(title: str, headers: list[str], modified: list[str]=None):
    console = Console()
    table = Table(title=title, show_header=True, header_style="b deep_sky_blue1")
    for header in headers:
        if modified and header in modified:
            table.add_column(header, header_style="b spring_green2")
        else:
            table.add_column(header)
    console.print(table)

def print_table(title: str, headers: list[str], rows: list[list[str]],
               added_headers: list[str]=None, deleted_columns: list[str]=None,
               added_rows: list[int]=None, deleted_rows: list[int]=None,
               show_index: bool=False, show_headers: bool=True):
    console = Console()
    table = Table(title=title, show_header=show_headers, header_style="b deep_sky_blue1")
    if show_index:
        headers.insert(0, "Index")
    for header in headers:
        if deleted_columns and header in deleted_columns:
            table.add_column(header, style="b s red", justify="center")
        elif added_headers and header in added_headers:
            table.add_column(header, header_style="b spring_green2")
        else:
            table.add_column(header)

    for i, row in enumerate(rows):
        if show_index:
            if added_rows and i in added_rows:
                table.add_row(str(i), *[str(item) for item in row], style="b spring_green2")
            elif deleted_rows and i in deleted_rows:
                table.add_row(str(i), *[str(item) for item in row], style="b s red")
            else:
                table.add_row(str(i), *[str(item) for item in row])
        else:
            if added_rows and i in added_rows:
                table.add_row(*[str(item) for item in row], style="b spring_green2")
            elif deleted_rows and i in deleted_rows:
                table.add_row(*[str(item) for item in row], style="b s red")
            else:
                table.add_row(*[str(item) for item in row])

    console.print(table)

