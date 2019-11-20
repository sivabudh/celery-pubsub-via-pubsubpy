# celery-pubsub-via-pubsubpy
Simplest example to demonstrate how to do publish/subscribe with Celery

To run this application, first do the usual:

```
pip install -r requirements.txt
````

For this program to work correctly, you need to have a RabbitMQ running. For my case, I ran RabbitMQ with Docker. So
you could, for instance, run RabbitMQ in the background like this:

```
docker run -d -p 15672:15672 -p 5672:5672 -p 5671:5671 --hostname my-rabbitmq --name my-rabbitmq-container rabbitmq:3-management
```

Then, open 3 terminals.

In the first terminal, run the scheduler:

```
# This runs Celery beat which triggers our desired function every 3 seconds.
celery -A main beat --loglevel=warning
```

In the second terminal, run the subscriber:

```
# This runs Celery worker which actually calls our desired function
celery -A main worker --loglevel=warning
```

In the third terminal, run the publisher:

```
# Go into Python console, and do the following:
>>> from pubsub import PubSub
>>> pubsub_app = PubSub('amqp://guest@localhost', 'sample.topic')
>>> pubsub_app.publish_model_event('booking', 'saved', {"document_register_number": 12345})
```

Finally, you should see the subscriber printing out data received from the publisher!
