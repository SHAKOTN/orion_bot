import os

import celery
from celery.schedules import crontab

if os.environ.get('CELERY_ENABLED') == '1':

    app = celery.Celery('celery')

    app.conf.update(broker_url=os.environ['CLOUDAMQP_URL'])


    @app.on_after_configure.connect
    def add_periodic(**kwargs):
        from bot.tasks import post_random_webm
        app.add_periodic_task(
            crontab(hour='7,16', minute='*/30'),
            post_random_webm.s(),
            name='Post random WEBM'
        )
