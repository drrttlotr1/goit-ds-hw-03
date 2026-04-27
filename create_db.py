from pymongo import MongoClient


client = MongoClient(
    "mongodb+srv://drrttlotr:QPJwbT8wa7KjMghtFjFJGN1S@cluster0.xpcecen.mongodb.net/?appName=Cluster0"
)

def create_db():
    db_name = "book"
    collection_name = "cats"

    db = client[db_name]
    collection = db[collection_name]
    collection.insert_one(
        {
            "name": "Ліліт",
            "age": 14,
            "features": ["нервова", "примхлива", "любить своїх людей"],
        }
    )
    print("Database created successfully")

if __name__ == "__main__":
    create_db()