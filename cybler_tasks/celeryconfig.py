## Broker settings.
from cybler_tasks import setup_app
from celery.schedules import crontab
setup_app("development.ini")

BROKER_URL = "mongodb://localhost:27017/cybler"
# List of modules to import when celery starts.
CELERY_IMPORTS = ("cybler_tasks.tasks.scraped_ingestion", "cybler_tasks.data.feed_scraper")

CELERYBEAT_SCHEDULE = {
    "ingest-backpage": {
        "task": "celery_tasks.tasks.scraped_ingestion.ingest_backpage",
        "schedule": crontab(minute="0,15,30,45"),
        "args": ()
        },
    "ingest-adultsearch": {
        "task": "celery_tasks.tasks.scraped_ingestion.ingest_adultsearch",
        "schedule": crontab(minute="0,15,30,45"),
        "args": ()
        }
    }

