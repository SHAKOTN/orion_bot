import celery
import os

app = celery.Celery('slack_bot')

app.conf.update(BROKER_URL=os.environ['REDIS_URL'])