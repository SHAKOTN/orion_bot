import os

import celery
from celery.schedules import crontab

app = celery.Celery('celery')

app.conf.update(broker_url=os.environ['REDIS_URL'])
app.conf.update(redis_max_connections=3)


@app.on_after_configure.connect
def add_periodic(**kwargs):
    from bot.tasks import post_random_webm
    app.add_periodic_task(
        crontab(minute='*/15'),
        post_random_webm.s(),
        name='Post random WEBM'
    )
    app.add_periodic_task(
        crontab(hour=11, minute=0),
        post_random_webm.s(),
        name='Post random WEBM'
    )
    app.add_periodic_task(
        crontab(hour=13, minute=0),
        post_random_webm.s(),
        name='Post random WEBM'
    )
