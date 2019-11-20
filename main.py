from celery import Celery
from pubsub import PubSub

app = Celery('periodic')
pubsub_app = PubSub('amqp://guest@localhost', 'sample.topic')


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(3.0, pubsub_listen, name='Consume messages')


@pubsub_app.subscribe('booking.*')
def process_booking_event(_, message):
    print("Subscriber!")
    print(message)


@app.task
def pubsub_listen():
    print("Go go")
    pubsub_app.drain()
    print("Drained")
    return "Done!"
