import os

import celery
from celery.schedules import crontab

if os.environ.get('CELERY_ENABLED') == '1':

    app = celery.Celery('celery')

    app.conf.update(broker_url=os.environ['CLOUDAMQP_URL'])


    @app.on_after_configure.connect
    def add_periodic(**kwargs):
        from bot.tasks import (
            post_random_webm,
            post_morning_weather
        )
        app.add_periodic_task(
            crontab(minute=0,
                    hour='7,8,9,10,11,12,13,14,15,16,17,18'),
            post_random_webm.s(),
            name='Post random WEBM'
        )

        app.add_periodic_task(
            crontab(hour=6, minute=0),
            post_morning_weather.s(),
            name='Post morning weather'
        )
