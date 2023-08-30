import main as m
from bot import chat
import pymongo
from pymongo import MongoClient
class User(object):
  def __init__(self, name):
    self.username = name
  def send_message(self,message_history,prompt):
    message_history.append({"role":"user","content": prompt}) 
    response=chat.activate(message_history)
    message_history.append({"role":"assistant","content": response})
    m.populate_db(self.username,prompt,response)
    return message_history

  def get_N_message(self,client,db,collection):
    list = []
    user_data = collection.find({"user_name":self.username})
    for i in user_data:
      list.append(i)
    return list