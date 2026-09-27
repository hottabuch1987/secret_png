# config/celery.py
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# для докер исправить на settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Принудительно установить брокер
app.conf.broker_url = settings.REDIS_URL
app.conf.result_backend = settings.REDIS_URL


# Настройки для Celery Beat
app.conf.timezone = 'Europe/Moscow'
app.conf.enable_utc = False


app.conf.beat_schedule = {
    'clean_expired_codes_every_minute': {
        'task': 'users.tasks.clean_expired_codes',
        'schedule': crontab(minute='*/1'),  # каждую минуту
        'options': {
            'expires': 60,  # задача живет 60 секунд
        }
    },
}