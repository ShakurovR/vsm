import os

from celery import Celery
from kombu import Exchange, Queue

APP_NAME = "pipeline"


celery_app = Celery(
    f"worker_{APP_NAME}",
    broker_url=os.getenv("CELERY_BROKER_URL"),
    result_backend=os.getenv("CELERY_RESULT_BACKEND"),
)
celery_app.conf.update(task_track_started=True, broker_connection_retry_on_startup=True)

celery_app.conf.task_queues = [
    Queue(APP_NAME, exchange=Exchange(APP_NAME, type="direct"), routing_key=APP_NAME),
]
celery_app.conf.task_default_queue = APP_NAME
celery_app.conf.task_default_exchange = APP_NAME
celery_app.conf.task_default_routing_key = APP_NAME
