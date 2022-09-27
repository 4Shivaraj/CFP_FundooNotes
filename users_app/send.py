#!/usr/bin/env python
import pika
import json


class Producer:
    """
    A program that sends messages is a producer
    """

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='send_email')

    def publish(self, method, payload):
        """
        a message can never be sent directly to the queue, it always needs to go through an exchange.
        This exchange is special ‒ it allows us to specify exactly to which queue the message should go. 
        """
        send_data = json.dumps(payload)
        self.channel.basic_publish(exchange='',
                                   routing_key='send_email',
                                   body=send_data,
                                   properties=pika.BasicProperties(method))
        print(" [x] 'Token' Sent Successfully")
        self.connection.close()
