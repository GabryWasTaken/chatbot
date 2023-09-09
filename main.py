#import pymongo
#from pymongo import MongoClient
#-*- coding: utf-8 -*-
import time
from configuration_const import config_const as c
from bot import chat
from database import create_db as d
from users import user
from user import User as u
from users import superuser
from superuser import SuperUser as s
import os
import json
from dotenv import load_dotenv
import passwordcheck as p
import datetime
from tabulate import tabulate
import random
from database import store_data as dt
import hashlib
import producer as pd
import worker as wk
load_dotenv()


def loginpage():
    while True:
        print("###########################################################")
        print("###########################################################")
        print("0 - Exit Program")
        print("1 - Login")
        print("2 - Register")
        print("###########################################################")
        print("###########################################################")
        print("Waiting for input...")
        try:
            pick = int(input())
        except:
            pick=int(77) #random number to activate the default
        match pick:
            case 0:
                break
            case 1:
                login()
            case 2:
                register()
            case default:
                print("Invalid Input... Please Try Again Later")

def save_credentials(username, password,type):
    dt.store_user(username,password,type)

def verify_credentials(username,password):
    password= hashlib.md5(password.encode())
    password=password.hexdigest() 
    doc = dt.search_credentials(username,password)
    try:
        stored_password=doc["password"]
        stored_username=doc["user_name"]
    except:
        stored_password=""
        stored_username=""
    if stored_password == password and stored_username==username:
        return True


def register():
    while True:
        new_username = input("Create a username: ")
        username=dt.get_username(new_username)
        if new_username == username:
            print("Username alredy exists, retry...")
        else:
            break
    new_password = p.getpass_masked()
    while True:
        print("do you wanna register like user or superuser?")
        resp=input("0/1: ")
        if resp =="0":
            type="user"
            break
        elif resp =="1":
            type="superuser"
            break
        else:
            print("Wrong answer... Retry")
    save_credentials(new_username, new_password,type)
    print("Registration Completed. Now you can login with your credentials.")


def login():
    username = input("Insert the username: ")
    password = p.getpass_masked()
    
    if verify_credentials(username, password):
        type = dt.get_type(username)
        main(username,type)
    else:
        print("Incorrect credentials.")


def main(username,type):
    message_history=[]
    while True:
        if type =="user":
            usr = u(username)
        elif type =="superuser":
            usr = s(username)
        print("###########################################################")
        print("###########################################################")
        print("0 - Logout")
        print("1 - Send a message")
        print("2 - Start a chat")
        print("3 - View your last N interaction")
        print("###########################################################")
        print("###########################################################")        
        print("Waiting for input...")
        try:
            pick = int(input())
        except:
            pick=int(9)
        match pick:
            case 0:
                message_history=[]
                break
            case 1:
                    print("Make a question to the AI")
                    prompt=input(username+": ")
                    info = [username,message_history,prompt]
                    info=json.dumps(info)
                    sleep_time=random.randint(3,5)
                    time.sleep(sleep_time)
                    pd.send_message_to_worker(info)
                    w=wk.Worker()
                    data=w.start_consuming()
                    message_history=data[0]
                    response=data[1]
                    populate_db(username,prompt,response)             
            case 2:
                chat_history=[]
                print("Chat starts here... Write 'exit' if you wanna leave the chat")
                while True:
                    prompt=input(username+": ")
                    info = [username,chat_history,prompt]
                    info=json.dumps(info)
                    sleep_time=random.randint(3,5)
                    time.sleep(sleep_time)
                    pd.send_message_to_worker(info)
                    w=wk.Worker()
                    data=w.start_consuming()
                    chat_history = data[0]
                    response = data[1]
                    populate_db(username,prompt,response)
                    if prompt.lower() == "exit":
                        break

            case 3:
                n=int(0)
                try:
                    interaction=input("How many interaction do you wanna see? (A number for example 3): ")
                    interaction=int(interaction)
                except:
                    print("Number selected is wrong... Back in menu")
                    interaction=int(0)
                list=usr.get_N_message(c.client,c.db,c.collection)

                while True:
                    n=n+1
                    try:
                        if n<=interaction:
                            tab = dict()
                            tab=list.pop()
                            timestamp=tab['time_stamp']
                            date = datetime.datetime.fromtimestamp(timestamp)
                            date = date.strftime('%Y-%m-%d %H:%M:%S')            
                            print("###########################################################")
                            table = [
                                ["User name", tab['user_name']],
                                ["Message Sent", tab['message_sent']],
                                ["Message received", tab['message_received']],
                                ["Message time", str(date)]
                                    ]
                            print(tabulate(table,tablefmt="grid"))
                        else:
                            break
                    except IndexError:
                        print("Number of interaction greater than interaction of user/s...")
                        break


            case default:
                print("Incorrect number selected, Retry...")

def populate_db(username,prompt,response):
    timestamp = time.time()
    doc = {
    'user_name': username,
    'message_sent':prompt,
    'message_received':response,
    'time_stamp':timestamp
        }
    d.setup(c.client,c.db,c.collection,doc)


loginpage()

quit()

