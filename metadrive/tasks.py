from celery import Celery

app = Celery('metadrive.tasks', broker='pyamqp://guest@localhost//')

@app.task
def add(x, y):
    return x + y
