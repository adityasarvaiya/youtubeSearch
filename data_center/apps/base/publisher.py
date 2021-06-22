import logging

from kombu.exceptions import KombuError

# Import celery app object of other micro-services into which you want to publish tasks here.

logger = logging.getLogger(__name__)

# Add the micro-service's name as key and imported celery app object as value in the below dictionary.
APP_NAMESPACE = {}


def publish(exchanges, task, *args, **kwargs):
    """
    This is a temporary method which can push the tasks into other exchanges
    Ideally, this should be handled via proper pub-sub infrastructure.
    """

    if not isinstance(exchanges, list):
        exchanges = [exchanges]

    for exchange in exchanges:
        exchange_app = APP_NAMESPACE.get(exchange)

        if not exchange_app:
            logger.warning(f"{exchange} is not a valid Exchange. Skipping this task")
            continue

        try:
            exchange_app.send_task(task, args=args, kwargs=kwargs)
        except KombuError:
            logger.exception(f"Connection Error for {exchange} for Task: {task}")
        else:
            logger.debug(f"Pushed task {task} with Args: {args} and Kwargs {kwargs} in {exchange}")