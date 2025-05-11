from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CallAgent.settings')

app = Celery('CallAgent')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'mark-unresolved-task': {
        'task': 'src.tasks.mark_unresolved_if_expired',  
        'schedule': 60.0,  
    },
}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
