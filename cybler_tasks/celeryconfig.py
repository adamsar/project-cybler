## Broker settings.
from cybler_tasks import setup_app
from datetime import timedelta
setup_app("development.ini")

BROKER_URL = "mongodb://localhost:27017/cybler"
# List of modules to import when celery starts.
CELERY_IMPORTS = ("cybler_tasks.tasks.scraped_ingestion", "cybler_tasks.data.feed_scraper")

CELERYBEAT_SCHEDULE = {
    "ingest-backpage": {
        "task": "celery_tasks.tasks.scraped_ingestion.ingest_backpage",
        "schedule": timedelta(seconds=60*30), #Every 30 minutes
        },
    "ingest-adultsearch": {
        "task": "celery_tasks.tasks.scraped_ingestion.ingest_adultsearch",
        "schedule": timedelta(seconds=60*30), #Every 30 minutes
        },
    "ingest-naughtyreviews": {
        "task": "celery_tasks.tasks.scraped_ingestion.ingest_naughtyreviews",
        "schedule": timedelta(seconds=60*30), #Every 30 minutes
        }        
    }

