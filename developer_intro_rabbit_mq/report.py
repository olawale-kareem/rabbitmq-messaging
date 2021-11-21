import pika
import json
import uuid


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

queue = channel.queue_declare( 'order_report')
queue_name = queue.method.queue

channel.queue_bind(
    exchange='order',
    queue=queue_name,
    routing_key='order.report'   
)

def callback(ch, method, properties, body):
    payload = json.loads(body)
    print(' [x] Generating report ')
    print(f'''
        ID: {payload.get('id')}
        USER_EMAIL: {payload.get('user_email')}
        PRODUCT: {payload.get('product')}
        QUANTITY: {payload.get('quantity')}
        ''')
    ch.basic_ack(delivery_tag=method.delivery_tag)    

channel.basic_consume(on_message_callback=callback, queue='order_report')
print(' [*] Waiting for notify messages. To exit  press CTRL')
channel.start_consuming()

