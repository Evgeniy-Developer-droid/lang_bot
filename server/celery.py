

import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

app = Celery('server')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'challenge': {
        'task': 'bot.tasks.challenge_task',
        'schedule': crontab(hour='9-21', minute="*/1")
    },
    'morning_word_list': {
        'task': 'bot.tasks.morning_word_list_task',
        'schedule': crontab(minute=0, hour=9)
    },
}


app.autodiscover_tasks()