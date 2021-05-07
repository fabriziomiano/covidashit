"""
celery worker
"""
import datetime as dt

from celery import Celery

from app import create_app

app = create_app()
app.app_context().push()
celery = Celery(__name__)
celery.config_from_object(app.config)
celery.conf.update(app.config.get("CELERY_CONFIG", {}))
celery.conf.beat_schedule = {
    'run-me-every-ten-seconds': {
        'task': 'app.db_utils.tasks.update_istat_it_population_collection',
        'schedule': dt.timedelta(days=1)
    }
}
