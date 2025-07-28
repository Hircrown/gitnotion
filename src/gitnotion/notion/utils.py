import os
from notion_client import Client
from notion_client.helpers import get_id
from notion_client import APIErrorCode, APIResponseError


def get_notion_client(NOTION_TOKEN=os.getenv("NOTION_TOKEN")):
    if NOTION_TOKEN:
        return Client(auth=NOTION_TOKEN)
    else:
        raise ValueError("NOTION_TOKEN is not set. Please set it in your environment variables.")    


def init_db(db_link: str) -> tuple[dict | str, str]:
    try:
        notion = get_notion_client()
        db_id = get_id(db_link)
        data = notion.databases.retrieve(db_id)
        return (data, db_id)
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

def query_db(db_id: str) -> dict:
    try:
        notion = get_notion_client()
        data = notion.databases.query(db_id)
        return data
    except Exception as e:
        return e
    
def get_row_data(headers: list[str], data: dict) -> list[str]:
    rows = data["results"]
    #It seems that the first result is the last row added
    #Still don't know what's the max row retrivable
    rows_values = []
    for row in rows:
        row_values = []
        for header in headers:
            type = row["properties"][header]["type"]
            elm = row["properties"][header][type]
            if elm != [] and elm != None:
                if type == "title" or type == "rich_text":
                    row_values.append(elm[0]["plain_text"])
                elif type == "unique_id":
                    row_values.append(elm["number"])
                elif type == "email" or type == "checkbox" or type== "number" or type == "phone_number" or type == "url":
                    row_values.append(elm)
                elif type == "select" or type == "status":
                    row_values.append(elm["name"]) 
                elif type == "date":
                    start = elm["start"]
                    end = elm["end"]
                    time_zone = elm["time_zone"]
                    row_values.append((start, end, time_zone))
                elif type == "files":
                    #row_values.append(elm[0]["file"]["url"])
                    row_values.append(elm[0]["name"])
                elif type == "multi_select":
                    values = []
                    for e in elm:
                        values.append(e["name"])
                    row_values.append(values)
            else:
                row_values.append(None)
        rows_values.append(row_values)
    return rows_values

