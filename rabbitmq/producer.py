import pika

def send_message_to_worker(message):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
    except:
        print("Error in the connection...")
        print("Check if you inserted the right parameters")
        quit()

    channel.queue_declare(queue='message_queue')

    channel.basic_publish(exchange='', routing_key='message_queue', body=message)
    #print(f"Sent message to worker: {message}")
    connection.close()


