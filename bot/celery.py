import os

import celery

app = celery.Celery('slack_bot')

app.conf.update(BROKER_URL=os.environ['REDIS_URL'])


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    from bot.tasks import hello
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(30.0, hello(), name='add every 10')
