import os

import celery

app = celery.Celery('celery')

app.conf.update(BROKER_URL=os.environ['REDIS_URL'])


@app.on_after_configure.connect
def add_periodic(**kwargs):
    from bot.tasks import hello
    app.add_periodic_task(10.0, hello(), name='add every 10')
