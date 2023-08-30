
import pymongo
from pymongo import MongoClient

def setup(client,db,collection,doc):
    collection.create_index([("user_name",pymongo.ASCENDING)])
    collection.insert_one(doc)


