import openai
from configuration_const import config_const as c
from rabbitmq import producer as p
from rabbitmq import worker as w
import pika
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
    
    response = openai.ChatCompletion.create( 
        model="gpt-3.5-turbo", 
        messages=chat_history 
    )
    response=response.choices[0].message.get("content")
    send_to_rabbit(response)
    return response

def send_to_rabbit(response):
    p.send_message_to_worker(response)
    Work = w.Worker()
    Work.start_consuming()
