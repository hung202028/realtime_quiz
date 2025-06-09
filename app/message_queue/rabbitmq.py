import json

import pika
from pydantic import BaseModel

from app.message_queue.base import MessageQueue


class RabbitMQ(MessageQueue):
    def __init__(self, *args, **kwargs):
        self.host = kwargs.get("host")
        self.port = kwargs.get("port", 5672)
        self.vhost = kwargs.get("vhost")
        self.credentials = pika.PlainCredentials(
            username=kwargs.get("username"),
            password=kwargs.get("password")
        )

    def _connect(self) -> pika.BlockingConnection:
        return pika.BlockingConnection(pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            credentials=self.credentials,
            virtual_host=self.vhost,
        ))

    def publish(self, data: BaseModel, **kwargs):
        connection = None
        try:
            connection = self._connect()
            channel = connection.channel()

            exchange_params = kwargs.get("exchange_params", {})

            channel.exchange_declare(**exchange_params)
            channel.basic_publish(
                exchange=exchange_params.get("exchange"),
                routing_key=kwargs.get("routing_key"),
                body=json.dumps(data.model_dump()),
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                ),
                mandatory=False,
            )
        finally:
            if connection and connection.is_open:
                connection.close()
