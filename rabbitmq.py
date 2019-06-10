#!/usr/bin/env python
import pika, random, string

def send():
	rand_serv = "172.22.0."+str(random.randint(2, 4) )
	credentials = pika.PlainCredentials('admin', 'admin123')
	#credentials = pika.PlainCredentials('guest', 'guest')
	connection = pika.BlockingConnection(pika.ConnectionParameters("192.168.1.2",5672,'/', credentials))
	channel = connection.channel()

	digits = "".join( [random.choice(string.digits) for i in xrange(8)] )
	chars = "".join( [random.choice(string.letters) for i in xrange(15)] )
	messs = digits + chars

	channel.exchange_declare(exchange='yolo',
	                         type='fanout')

	#channel.queue_declare(queue='hello')
	for i in range(10):
		channel.basic_publish(exchange='yolo',
	                      routing_key='hello',
	                      body=str(i)+"-"+messs+rand_serv)
	print(" [x] Sent 'Hello '"+messs)
	connection.close()


def receive():
	credentials = pika.PlainCredentials('admin', 'admin123')
	connection = pika.BlockingConnection(pika.ConnectionParameters("192.168.1.2",5672,'/', credentials))
	channel = connection.channel()

	#channel.exchange_declare(exchange='yolo',type='fanout')

	LAST=0
	def callback(ch, method, properties, body):
	#       print (" [x] Received %r" % body)
	    # NOW=body[:body.index('-')]
	    # global LAST
	    # if (NOW!=str(LAST+1)) and (NOW!="0"):
	    #     print ("LOOOASSSTT!!!!!!! %s - %s" % (LAST, NOW))
	    #     return
	    # else:
	    print (" [x] Received %r" % body)    
	    # LAST = int(NOW)


	result = channel.queue_declare(exclusive=True)
	queue_name = result.method.queue

	channel.queue_bind(exchange='shop',
	                   queue=queue_name,routing_key='123')

	channel.basic_consume(callback,
	                      queue=queue_name,
	                      no_ack=True)


	print(' [*] Waiting for messages. To exit press CTRL+C')
	channel.start_consuming()
