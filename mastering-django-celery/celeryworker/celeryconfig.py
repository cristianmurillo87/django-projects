import os

"""
These variables could also be declared as:
broker_url and result_backend

In this case, the config_from_object function should be called without the "namespace" argument
"""
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_BACKEND", "redis://redis:6379/0")
