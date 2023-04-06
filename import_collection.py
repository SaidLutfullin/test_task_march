from config import HOST, POST, DB_NAME, COL_NAME
import pymongo
import bson

client = pymongo.MongoClient(HOST, POST)
db = client[DB_NAME]
collection = db[COL_NAME]

with open('sample_collection.bson', 'rb') as f:
    data = bson.decode_all(f.read())
    collection.insert_many(data)