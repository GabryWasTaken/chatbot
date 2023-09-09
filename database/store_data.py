import pymongo
from pymongo import MongoClient
from configuration_const import config_const
import hashlib
from configuration_const import config_const as c

def store_user(username,password,type):
    db=c.db
    collection=db.user
    collection.create_index([("user_name",pymongo.ASCENDING)])
    collection.create_index([("password",pymongo.ASCENDING)])
    password= hashlib.sha256(password.encode())
    password=password.hexdigest()
    doc = {
    'user_name': username,
    'password':password,
    'type':type,
        }
    collection.insert_one(doc)

def search_credentials(username,s_password):
    doc = dict()
    db=c.db
    collection=db.user
    password = collection.find({"password":s_password,"user_name":username})
    try:
        doc=password[0]
        return doc
    except:
        return None
    
def get_type(username):
    doc = dict()
    db=c.db
    collection=db.user
    try:
        doc = collection.find({"user_name":username})
        type=doc[0]
        return type["type"]
    except:
        print("Error... Retry later")
        return None
    
def get_username(username):
    doc = dict()
    db=c.db
    collection=db.user
    try:
        doc = collection.find({"user_name":username})
        usr=doc[0]
        return usr["user_name"]
    except:
        return None      

