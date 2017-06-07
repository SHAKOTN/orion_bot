import os

import celery
from celery.schedules import crontab

app = celery.Celery('celery')

app.conf.update(broker_url=os.environ['REDIS_URL'])


@app.on_after_configure.connect
def add_periodic(**kwargs):
    from bot.tasks import post_random_webm
    app.add_periodic_task(
        crontab(minute=0, hour=7),
        post_random_webm.s(),
        name='Post random WEBM'
    )
