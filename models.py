from pymongo import MongoClient
import json

# Ustawienia MongoDB
MONGO_URI = "mongodb://localhost:27017"
DATABASE_NAME = "quotes_database"

def upload_to_mongodb():
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    
    with open("quotes.json", "r", encoding="utf-8") as f:
        quotes_data = json.load(f)
        db.quotes.insert_many(quotes_data)

    with open("authors.json", "r", encoding="utf-8") as f:
        authors_data = json.load(f)
        db.authors.insert_many(authors_data)

upload_to_mongodb()
