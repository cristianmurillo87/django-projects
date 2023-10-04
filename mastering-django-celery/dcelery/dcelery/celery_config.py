from __future__ import absolute_import, unicode_literals

import os
import time

from celery import Celery
from kombu import Exchange, Queue

# ensure settings defined in settings.py are initialized
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dcelery.settings")

app = Celery("dcelery")
# search in the settings file for all variables whose name starts with CELERY
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.tasks_queues = [
    Queue(
        "tasks",
        Exchange("tasks"),
        routing_key="tasks",
        queue_arguments={"x-max-priority": 10},
    )
]

app.conf.tasks_acks_late = True
app.conf.task_default_priority = 5
app.conf.worker_prefetch_multiplier = 1
app.conf.worker_concurrency = 1

base_dir = os.getcwd()
tasks_folder = os.path.join(base_dir, "dcelery", "celery_tasks")

task_modules = []
if os.path.exists(tasks_folder) and os.path.isdir(tasks_folder):
    for filename in os.listdir(tasks_folder):
        if not (filename.startswith("ex") and filename.endswith(".py")):
            continue
        module_name = f"dcelery.celery_tasks.{filename[:-3]}"
        module = __import__(module_name, fromlist=["*"])

        for name in dir(module):
            obj = getattr(module, name)
            if callable(obj) and name.startswith("test_task"):
                task_modules.append(f"{module_name}.{name}")

# register tasks by looking for files named tasks.py where the tasks are defined
app.autodiscover_tasks(task_modules)
