release: python -m flask create-collections
web: gunicorn wsgi:app
worker: celery -A celery_worker.celery worker --concurrency 4
beat: celery -A celery_worker.celery beat