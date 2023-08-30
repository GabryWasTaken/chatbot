import openai, pika, pymongo
from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_KEY")

"""

MONGODB DATA

"""

client= MongoClient('localhost',27017) #Connection to my DB noSQL
db = client.prj_db
collection = db.chat

"""

RABBITMQ DATA

"""

params = pika.ConnectionParameters(host="localhost")
connection = pika.BlockingConnection(params)

"""

OPENAI DATA

"""

API=openai.api_key=OPENAI_KEY
