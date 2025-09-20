import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'security_system.settings')

app = Celery('security_system')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Celery Beat Schedule for periodic tasks
app.conf.beat_schedule = {
    'send-joke-emails-daily': {
        'task': 'automation.tasks.send_joke_emails',
        'schedule': crontab(hour=9, minute=0),  # Daily at 9:00 AM
    },
    'cleanup-sessions-weekly': {
        'task': 'automation.tasks.cleanup_old_sessions',
        'schedule': crontab(hour=2, minute=0, day_of_week=1),  # Weekly on Monday at 2:00 AM
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
