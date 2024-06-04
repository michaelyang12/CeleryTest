from celery import Celery
import time
import logging

# Configure Celery
redis_password = 'mypassword'
CELERY_BROKER_URL = f'redis://:{redis_password}@localhost:6379/0'
CELERY_RESULT_BACKEND = f'redis://:{redis_password}@localhost:6379/0'

celery = Celery(__name__, broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

# Configure logging
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

@celery.task(bind=True)
def long_running_task(self):
    i = 0
    while True:
        if self.request.called_directly:
            break
        logger.info(f"Task running... {i+1} seconds elapsed")
        i += 1
        time.sleep(1)  # Simulate a long-running task
    logger.info("Task completed")
    return 'Task completed'
