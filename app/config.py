import os

from app.cache.base import QuizCache
from app.cache.redis import QuizCacheRedis
from app.logger import Logger
from app.message_queue.base import MessageQueue
from app.message_queue.rabbitmq import RabbitMQ
from app.monitor.base import Monitor
from app.monitor.prometheus import Prometheus


class AppConfigs:
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "logs.json")

    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DECODE_RESPONSE = bool(os.getenv("REDIS_DECODE_RESPONSE", True))

    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", 3306))
    DB_NAME = os.getenv("DB_NAME", "quiz")

    RMQ_HOST = os.getenv("RMQ_HOST", "localhost")
    RMQ_PORT = os.getenv("RMQ_PORT", 5672)
    RMQ_USERNAME = os.getenv("RMQ_USERNAME")
    RMQ_PASSWORD = os.getenv("RMQ_PASSWORD")
    RMQ_VHOST = os.getenv("RMQ_VHOST")

    PROMETHEUS_PORT = int(os.getenv("PROMETHEUS_PORT", 8001))


class AppClients:
    def __init__(self, config: AppConfigs):
        self.logger: Logger = Logger(log_file=config.LOG_FILE, log_level=config.LOG_LEVEL)
        self.monitor: Monitor = Prometheus(
            gauge_name="websocket_connections",
            gauge_documentation="Current WebSocket connections",
            histogram_name="websocket_request_latency",
            histogram_documentation="Request latency"
        )

        self.cache: QuizCache = QuizCacheRedis(
            host=config.REDIS_HOST,
            port=config.REDIS_PORT,
            decode_responses=config.REDIS_DECODE_RESPONSE
        )

        self.message_queue: MessageQueue = RabbitMQ(
            host=config.RMQ_HOST,
            port=config.RMQ_PORT,
            vhost=config.RMQ_VHOST,
            username=config.RMQ_USERNAME,
            password=config.RMQ_PASSWORD,
        )
