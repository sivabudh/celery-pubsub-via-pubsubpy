from celery import Celery
from pubsub import PubSub

app = Celery()
pubsub_app = PubSub('amqp://guest@localhost', 'sample.topic')


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(3.0, pubsub_listen, name='Consume messages')


@pubsub_app.subscribe('booking.*')
def process_booking_event(body, _):
    print(body['object'])


@app.task
def pubsub_listen():
    pubsub_app.drain()
    return "Done!"
