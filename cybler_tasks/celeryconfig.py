## Broker settings.
from cybler_tasks import setup_app
setup_app("development.ini")
BROKER_URL = "mongodb://localhost:27017/cybler"
# List of modules to import when celery starts.
CELERY_IMPORTS = ("celery_tasks.tasks.scraped_ingestion", "celery_tasks.data.feed_scraper")
