# celery.py

import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stroemer_test_farid.settings')

app = Celery('stroemer_test_farid')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.update(
    broker_url=os.environ.get('CELERY_BROKER_URL', 'pyamqp://guest:guest@rabbitmq:5672//'),
    result_backend=os.environ.get('CELERY_RESULT_BACKEND', 'rpc://'),
)
# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
