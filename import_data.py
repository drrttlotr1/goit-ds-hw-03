import json
from pathlib import Path

from pymongo import MongoClient


MONGO_URI = "mongodb+srv://drrttlotr:QPJwbT8wa7KjMghtFjFJGN1S@cluster0.xpcecen.mongodb.net/?appName=Cluster0"
DB_NAME = "quotes_db"


def import_json_to_mongodb() -> None:
    base_path = Path(__file__).resolve().parent
    authors_path = base_path / "authors.json"
    quotes_path = base_path / "quotes.json"

    with authors_path.open("r", encoding="utf-8") as file:
        authors = json.load(file)

    with quotes_path.open("r", encoding="utf-8") as file:
        quotes = json.load(file)

    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    authors_collection = db["authors"]
    quotes_collection = db["quotes"]

    authors_collection.delete_many({})
    quotes_collection.delete_many({})

    if authors:
        authors_collection.insert_many(authors)
    if quotes:
        quotes_collection.insert_many(quotes)

    print(
        f"Imported {len(authors)} authors and {len(quotes)} quotes into '{DB_NAME}'."
    )


if __name__ == "__main__":
    import_json_to_mongodb()
