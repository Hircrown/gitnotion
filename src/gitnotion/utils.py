import os
import pickle

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
