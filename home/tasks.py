from celery import shared_task
from . import client


@shared_task
def mark_as_read(no_of_unreads, entity):
    messages = client.loop.run_until_complete(
        client.get_messages(limit=no_of_unreads, entity=entity))
    for m in messages:
        try:
            client.loop.run_until_complete(client.send_read_acknowledge(m))
        except:
            pass
