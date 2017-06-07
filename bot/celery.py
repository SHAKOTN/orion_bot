import os

import celery

app = celery.Celery('slack_bot')

app.conf.update(BROKER_URL=os.environ['REDIS_URL'])

app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'bot.tasks.hello',
        'schedule': 30.0,
    },
}

