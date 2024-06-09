import os

from celery import Celery
from celery.result import AsyncResult, allow_join_result
from kombu import Exchange, Queue

APP_NAME = "indexer"


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


def run_task(task_name: str, wait_result: bool = False, **kwargs) -> tuple[str, any]:
    queue = APP_NAME
    task = celery_app.send_task(task_name, kwargs=kwargs, queue=queue)
    if wait_result:
        with allow_join_result():
            return (task.id, task.get())
    else:
        return (task.id, None)


def get_status(task_id: str) -> dict:
    if task_id is None:
        return {"status": "Неизвестно"}
    res = AsyncResult(task_id, backend=celery_app.backend, app=celery_app)
    if res.state == "PROGRESS":
        return {"status": res.info.get("status", "Неизвестно")}
    elif res.state == "FAILURE":
        return {"status": "Ошибка"}
    elif res.state == "STARTED":
        return {"status": "В процессе"}
    else:
        return {"status": "Готово"}
