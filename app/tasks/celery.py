from celery import Celery

from app.config import Setting

celery = Celery(
    "tasks",
    broker=f"redis://{Setting.REDIS_HOST}:{Setting.REDIS_PORT}",
    include=["app.tasks.tasks"],
    broker_connection_retry_on_startup=True,
)