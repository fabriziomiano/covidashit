release: python -m flask createdb
web: gunicorn wsgi:app
worker: celery -A celery_worker.celery worker --concurrency 4
beat: celery -A celery_worker.celery beat