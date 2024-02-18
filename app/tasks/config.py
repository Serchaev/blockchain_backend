from celery import Celery

from app.core import settings

celery_app = Celery(
    "tasks",
    broker=settings.celery_broker(),
    backend="rpc://",
    include=["app.tasks.tasks"],
)
