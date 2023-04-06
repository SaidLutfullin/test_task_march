import pymongo
import bson

client = pymongo.MongoClient('localhost', 27017)
db = client['test_database']
collection = db["sample_collection"]

with open('sample_collection.bson', 'rb') as f:
    data = bson.decode_all(f.read())
    collection.insert_many(data)