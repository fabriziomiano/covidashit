"""
celery worker
"""
from app import create_app
from celery import Celery

app = create_app()
app.app_context().push()
celery = Celery(__name__)
celery.config_from_object(app.config)
celery.conf.update(
    broker_url=app.config['BROKER_URL'],
    result_backend=app.config['RESULT_BACKEND']
)
