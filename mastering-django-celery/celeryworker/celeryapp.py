from celery import Celery

app = Celery("dcelery_st")
# reading from celeryconfig.py
app.config_from_object("celeryconfig", namespace="CELERY")
