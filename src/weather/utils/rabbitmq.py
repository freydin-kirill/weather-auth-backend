from aio_pika import RobustConnection, connect_robust

from src.config import settings


# noinspection PyTypeChecker
async def get_rabbitmq_connection() -> RobustConnection:
    """Create a connection to RabbitMQ."""

    connection: RobustConnection = await connect_robust(
        host=settings.RABBITMQ_HOST,
        port=settings.RABBITMQ_PORT,
        login=settings.RABBITMQ_USER,
        password=settings.RABBITMQ_PASS,
        virtualhost=settings.RABBITMQ_VHOST,
    )
    return connection
