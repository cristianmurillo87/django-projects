from dcelery.celery_config import app


@app.task(queue="tasks")
def test_task():
    pass
