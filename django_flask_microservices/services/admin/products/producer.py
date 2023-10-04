# amqps://axyvtxso:XY03zx-wAvJt4kCN_Ej_sdALAuJTd8sp@codfish.rmq.cloudamqp.com/axyvtxso
import pika, json

params = pika.URLParameters('amqps://axyvtxso:XY03zx-wAvJt4kCN_Ej_sdALAuJTd8sp@codfish.rmq.cloudamqp.com/axyvtxso')
connection = pika.BlockingConnection(params)
channel = connection.channel()

def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='main', body=json.dumps(body), properties=properties)
