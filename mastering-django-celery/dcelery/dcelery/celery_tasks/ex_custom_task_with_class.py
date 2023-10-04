from celery import Task


class CustomTask(Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        if isinstance(exc, ConnectionError):
            print("Connection error ocurred...")
        else:
            print("{0!r} failed {1!r}".format(task_id, exc))
