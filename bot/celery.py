import os

import celery

if os.environ.get('CELERY_ENABLED') == '1':

    app = celery.Celery('celery')

    app.conf.update(broker_url=os.environ['CLOUDAMQP_URL'])
    app.conf.update(redis_max_connections=3)

