import os
from notion_client import Client
from notion_client.helpers import get_id
from notion_client import APIErrorCode, APIResponseError


def get_notion_client(NOTION_TOKEN=os.getenv("NOTION_TOKEN")):
    if NOTION_TOKEN:
        return Client(auth=NOTION_TOKEN)
    else:
        raise ValueError("NOTION_TOKEN is not set. Please set it in your environment variables.")    


def init_db(db_link: str) -> dict | str:
    try:
        notion = get_notion_client()
        db_id = get_id(db_link)
        data = notion.databases.retrieve(db_id)
        return data
    except ValueError as e:
        return(f"Error initializing Notion client: {e}")
    except APIResponseError as error:
        if error.code == APIErrorCode.Unauthorized:
            return f"NOTION_TOKEN invalid"
        elif error.code == APIErrorCode.RestrictedResource:
            msg = (
                "Given your Notion token, you don't have the permission to perform this operation\n"
                "Probably you are not the owner."
            )
            return msg
        elif error.code == APIErrorCode.ObjectNotFound:
            return "Object not found. Check that the database is connected to the Project API on the Notion website.\n" \
                    "Visit the site: https://www.notion.so/profile/integrations"
        else:
            return error
                    
def db_title(db: dict) -> str:
    return db["title"][0]["plain_text"] if db["title"] else "No title"

def db_headers(db: dict) -> list[str]:
    return list(db["properties"].keys())

def db_headers_type(db: dict) -> list[tuple[str, str]]:
    headers_type = []
    for property in db["properties"].keys():
        type = db["properties"][property]["type"]
        headers_type.append((property, type))
    return headers_type

def last_time_edited(db: dict) -> str:
    return db["last_edited_time"]

