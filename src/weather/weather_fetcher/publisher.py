import json

from datetime import datetime
from typing import Any

from aio_pika import DeliveryMode, Message

from src.config import settings
from src.weather.utils.rabbitmq import get_rabbitmq_connection


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


async def publish_weather_message(message: dict[str, Any]) -> None:
    connection = await get_rabbitmq_connection()
    async with connection:
        # Creating channel
        channel = await connection.channel()

        # Declaring queue
        queue = await channel.declare_queue(settings.RABBITMQ_QUEUE, durable=True)
        print(f" [x] Publishing message to queue {message}")

        # Sending the message
        await channel.default_exchange.publish(
            Message(
                body=json.dumps(message, cls=DateTimeEncoder).encode("utf-8"),
                content_type="application/json",
                delivery_mode=DeliveryMode.PERSISTENT,
            ),
            routing_key=queue.name,
        )
