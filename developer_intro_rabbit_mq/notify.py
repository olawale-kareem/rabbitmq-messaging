import pika
import json
import uuid


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

queue = channel.queue_declare( 'order_notify')
queue_name = queue.method.queue

channel.queue_bind(
    exchange='order',
    queue=queue_name,
    routing_key='order.notify'   
)

def callback(ch, method, properties, body):
    payload = json.loads(body)
    print(' [x] Notifying {}'.format(payload['user_email']))
    print('[x] Done')
    ch.basic_ack(delivery_tag=method.delivery_tag)    

channel.basic_consume(on_message_callback=callback, queue='order_notify')
print(' [*] Waiting for notify messages. To exit  press CTRL')
channel.start_consuming()

