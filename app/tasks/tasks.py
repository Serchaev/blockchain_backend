from app.tasks.config import celery_app


@celery_app.task
async def calculate_hash(id: int):
    ...
