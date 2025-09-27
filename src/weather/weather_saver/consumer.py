import asyncio
import json

from datetime import datetime
from typing import Any

from aio_pika.abc import AbstractIncomingMessage

from src.config import settings
from src.weather.crud import CurrentWeatherDAO
from src.weather.utils.rabbitmq import get_rabbitmq_connection


def parse_datetime(obj: Any) -> Any:
    """Convert string time fields to ``datetime`` objects."""

    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, str) and key == "time":
                try:
                    obj[key] = datetime.fromisoformat(value)
                except ValueError:
                    pass  # Keep as string if parsing fails
    return obj


async def handle_message(message: AbstractIncomingMessage) -> None:
    """Process and save received weather message."""

    async with message.process():
        try:
            payload: dict[str, Any] = json.loads(message.body.decode(), object_hook=parse_datetime)
            # Expecting payload to match CurrentWeatherHistory fields
            await CurrentWeatherDAO.create(**payload)
            print(f" [x] Saved weather data for provider: {payload.get('provider', 'unknown')}")
        except Exception as e:
            print(f" [x] Error processing message: {e}")
            # Reject the message so it goes back to the queue
            await message.reject(requeue=False)


async def start_consumer() -> None:
    """Start a RabbitMQ queue consumer."""

    connection = await get_rabbitmq_connection()
    async with connection:
        # Creating channel
        channel = await connection.channel()

        # Declaring queue
        queue = await channel.declare_queue(settings.RABBITMQ_QUEUE, durable=True)

        # Start consuming messages
        await queue.consume(handle_message, no_ack=True)

        print(" [*] Waiting for messages. To exit press CTRL+C")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(start_consumer())
