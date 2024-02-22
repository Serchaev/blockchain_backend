from celery import Celery

from app.core import settings

celery_app = Celery(
    "tasks",
    broker=settings.BROKER_URL,
    backend="rpc://",
    include=["app.tasks.tasks"],
)

celery_app.conf.beat_schedule = {
    f"run-every-{settings.CELERY_CH_TIME_DELTA}-seconds": {
        "task": "app.tasks.tasks.calculate_hash",
        "schedule": settings.CELERY_CH_TIME_DELTA,
    }
}
