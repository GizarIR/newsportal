# Как запускать celery задачи
#  Также необходимо установить Celery, Redis и запустить 4 терминала
# 1 - общий для запуска сервера Redis
# 2 - терминал окружения проекта: python3 manage.py runserver
# 3 - терминал окружения проекта для запуска задач без расписания: celery -A NewsPortal worker -l INFO --concurrency=10
#  где --concurrency - количество процессов, которые могут на нём запускаться
# 4 - (опционально) терминал окружения проекта для запуска задач с расписанием: celery -A NewsPortal beat -l INFO
# где beat м.б. заменен на флаг -B после INFO
# кроме того произведена установка в окружение и настройка в settings.py

import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPortal.settings')

app = Celery('news')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'news_week_every_monday_8am': {
        'task': 'news.tasks.news_week',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        # 'schedule': crontab(), #для отладки
        # 'args': (agrs),
    },
}

