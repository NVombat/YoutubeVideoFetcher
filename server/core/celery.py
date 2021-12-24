from celery import Celery
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

application = Celery("core")
application.config_from_object("django.conf:settings", namespace="CELERY")
application.autodiscover_tasks()

@application.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')