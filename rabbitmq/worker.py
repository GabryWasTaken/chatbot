import pika
import user as usr
import json
import time
class Worker:
    def __init__(self):
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue='message_queue')
        except:
            print("Error in the connection...")
            print("Check if you inserted the right parameters")
            quit()

    def produce_response(self, ch, method, properties, body):
        test = body.decode('utf-8')
        info = json.loads(test)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        username=info[0]
        global data
        message_history=info[1]
        u = usr.User(username)
        prompt=info[2]
        data=u.send_message(message_history,prompt)  
        self.connection.close()
        
        

    def start_consuming(self):
        self.channel.basic_consume(queue='message_queue', on_message_callback=self.produce_response, auto_ack=False)
        print("Worker is waiting for messages...")
        self.channel.start_consuming()
        return data









