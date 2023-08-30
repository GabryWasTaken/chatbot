import pika

class Worker:
    def __init__(self):
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue='input_queue')
        except:
            print("Error in the connection...")
            print("Check if you inserted the right parameters")
            quit()

    def produce_response(self, ch, method, properties, body):
        message = body.decode('utf-8')
        print(f"Assistant: {message}")
        self.connection.close()
        

    def start_consuming(self):
        self.channel.basic_consume(queue='input_queue', on_message_callback=self.produce_response, auto_ack=True)
        print("Worker is waiting for messages...")
        self.channel.start_consuming()

        







