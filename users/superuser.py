import user as u
import pymongo
from pymongo import MongoClient
class SuperUser(u.User):
    def __init__(self, username):
        super().__init__(username)

    def get_N_message(self,client,db,collection):
        list = []
        all_data = collection.find()
        for i in all_data:
            list.append(i)
        return list
