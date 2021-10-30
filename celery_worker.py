"""
celery worker
"""
from celery import Celery

from app import create_app

app = create_app()
app.app_context().push()
celery = Celery(__name__)
celery.config_from_object(app.config)
celery.conf.update(app.config.get("CELERY_CONFIG", {}))
