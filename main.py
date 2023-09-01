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
from dotenv import load_dotenv
import passwordcheck as p
import datetime
from tabulate import tabulate
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

def save_credentials(username, password):
    with open(".env", "a") as env_file:
        env_file.write(f"\n{username}={password}")

def verify_credentials(username, password):
    stored_password = os.getenv(username)
    if stored_password == password:
        return True


def register():
    new_username = input("Create a username: ")
    new_password = p.getpass_masked()

    save_credentials(new_username, new_password)
    print("Registration Completed. Now you can login with your credentials.")
    load_dotenv()


def login():
    username = input("Insert the username: ")
    password = p.getpass_masked()
    
    if verify_credentials(username, password):
        while True:
            print("do you wanna log like user or superuser?")
            resp=input("0/1: ")
            if resp =="0":
                type="user"
                break
            elif resp =="1":
                type="superuser"
                break
            else:
                print("Wrong answer... Retry")
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
                    message_history=usr.send_message(message_history,prompt)

            case 2:
                chat_history=[]
                print("Chat starts here... Write 'exit' if you wanna leave the chat")
                while True:
                    prompt=input(username+": ")  
                    chat_history=usr.send_message(chat_history,prompt)
                    if prompt =="exit":
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

