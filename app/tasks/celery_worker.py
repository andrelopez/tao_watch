from celery import Celery

from app.core.config import settings
from app.core.logging import configure_logging

# Configure logging
configure_logging()

# Create Celery instance
celery = Celery(
    "worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[],  # Add task modules here as they're created
)

# Set up Celery configuration
celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    worker_concurrency=2,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    task_track_started=True,
)


@celery.task(name="test_celery")
def test_celery() -> str:
    """Test Celery task to verify worker setup."""
    return "Celery is working!" 