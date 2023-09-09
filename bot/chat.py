import openai
from configuration_const import config_const as c
from rabbitmq import producer as p
from rabbitmq import worker as w
import pika
import time
import random
chat_history = []
def activate(chat_history):
    try:
        openai.api_key=c.API.strip()
    except:
        print("Error in the connection...")
        print("Check if the API key is correct")
        quit()
    return question(chat_history)
    

def question(chat_history):
    sleep_time=random.randint(2,4)
    time.sleep(sleep_time)
    response = openai.ChatCompletion.create( 
        model="gpt-3.5-turbo", 
        messages=chat_history 
    )
    response=response.choices[0].message.get("content")
    print("AI: "+response)
    return response

