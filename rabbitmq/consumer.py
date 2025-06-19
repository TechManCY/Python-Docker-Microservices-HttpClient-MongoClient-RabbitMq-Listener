import pika
import time # Good practice to add a delay to ensure RabbitMQ is ready

# Connect to RabbitMQ (host = name of the RabbitMQ service in docker-compose)
# set the service name in docker-compose = the container name
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq_local')
)
channel = connection.channel()

# Ensure the queue exists and match its existing properties
# since the queue was created as durable=True, then declare it as such.
channel.queue_declare(queue='networkTrial.queue', durable=True)

def callback(ch, method, properties, body):
    print(" [x] Raw body:", body, flush=True)
    try:
        print(" [x] Decoded:", body.decode(), flush=True)
    except Exception as e:
        print(f" [!] Decode error: {e}", flush=True)
    time.sleep(2)
    print("Message processed and acknowledged after delay.", flush=True)
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(
    queue='networkTrial.queue',
    on_message_callback=callback,
    auto_ack=False #false: The message is only removed from the queue after your application confirms successful processing.
)

print(' [*] Waiting for messages. To exit press CTRL+C', flush=True)
channel.start_consuming()