# Initialisation
import requests, json
import os
from dotenv import load_dotenv
from pprint import pprint

# Variables
# NOTION_SECRET_TOKEN = os.environ.get("NOTION_SECRET_TOKEN")
load_dotenv(f"{os.path.dirname(os.path.abspath(__file__))}/.env")
NOTION_SECRET_TOKEN = os.getenv("NOTION_SECRET_TOKEN")

databaseID ="ed2e50bfb968462caab35b9330690eb6"
headers = {
    "Authorization": f"Bearer {NOTION_SECRET_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}


def postDatabase(databaseID=databaseID, headers=headers, payload=None):
    readUrl = f"https://api.notion.com/v1/pages"
    payload["parent"]["database_id"] = databaseID

    payload_jsonstr = json.dumps(payload)
    res = requests.request("POST", readUrl, headers=headers, data=payload_jsonstr)
    data = res.json()
    # print(res.status_code)
    # pprint(res.text)
    print(data)
    return data
