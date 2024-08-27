# from __future__ import absolute_import, unicode_literals
# import os
# from celery import Celery
#
# # Вказуємо Django settings як конфігурацію для Celery
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ParkEasy.settings')
#
# app = Celery('ParkEasy')
#
# # Автоматично знаходить таски у додатках Django
# app.config_from_object('django.conf:settings', namespace='CELERY')
#
# # Автоматичне знаходження завдань у додатках
# app.autodiscover_tasks()


import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ParkEasy.settings')

app = Celery('ParkEasy')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')