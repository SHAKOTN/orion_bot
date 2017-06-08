import os

import celery

if os.environ.get('CELERY_ENABLED') == '1':

    app = celery.Celery('celery')

    app.conf.update(broker_url=os.environ['CLOUDAMQP_URL'])

