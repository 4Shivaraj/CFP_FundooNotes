#!/usr/bin/env python
import pika
import json
import sys
import os
from email.message import EmailMessage
import smtplib
import os


class Consumer:
    """
     will receive messages from the queue and print them on the screen
    """

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='send_email')
        self.sender = os.environ.get('EMAIL_HOST_USER')
        self.sender_password = os.environ.get('EMAIL_HOST_PASSWORD')

    def callback(self, ch, method, properties, body):
        """
         Whenever we receive a message, this callback function is called by the Pika library. 
         In our case this function will print on the screen the contents of the message.
        """

        payload = json.loads(body)
        msg = EmailMessage()            # Python EmailMessage Function
        msg['From'] = self.sender
        msg['To'] = payload.get('recipent')
        msg['Subject'] = 'User Registration with rabbitmq'
        msg.set_content(payload.get('message'))
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(user=self.sender, password=self.sender_password)
            smtp.sendmail(self.sender, payload.get(
                'recipent'), msg.as_string())
            print("[*] Mail sent to ", payload.get('recipent'))
            smtp.quit()

    def receiver(self):
        """
        will receive messages from the queue and print them on the screen
        """
        self.channel.basic_consume(queue='send_email',
                                   auto_ack=True,
                                   on_message_callback=self.callback)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()


if __name__ == '__main__':

    try:
        consumer = Consumer()
        consumer.receiver()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
