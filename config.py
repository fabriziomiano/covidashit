"""
Configuration
"""
import os

from dotenv import load_dotenv

load_dotenv()


class BaseConfig(object):
    """Base config class."""
    API_KEY = os.environ.get('API_KEY')
    REDIS_URL = os.environ.get('REDIS_URL')
    MONGO_URI = os.environ.get('MONGO_URI')
    SITEMAP_INCLUDE_RULES_WITHOUT_PARAMS = True
    CELERY_CONFIG = {
        'broker_url': REDIS_URL,
        'result_backend': REDIS_URL
    }


class Development(BaseConfig):
    """Development config."""
    DEBUG = True
    ENV = 'dev'


class Staging(BaseConfig):
    """Staging config."""
    DEBUG = True
    ENV = 'staging'


class Production(BaseConfig):
    """Production config"""
    DEBUG = False
    ENV = 'production'


config = {
    'development': Development,
    'staging': Staging,
    'production': Production,
}
