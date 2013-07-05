from pika.adapters.blocking_connection import BlockingConnection
from pika.exceptions import ProbableAuthenticationError
from threading import Thread, Lock

class AMQPAgent(Thread):
    def __init__(self, channel):
        super(AMQPAgent, self).__init__()

        self._channel = channel
        self._queue   = None
        self._queue_options = {}
        self._kwargs  = {}
        self._lock    = Lock()

    def set_queue(self, queue):
        self._queue = queue

    def set_options(self, options):
        self._queue_options = options

class Publisher(AMQPAgent):
    def publish(self, **kwargs):
        if not self._queue:
            raise RuntimeError('Queue is not defined.')

        self._kwargs = kwargs
        self.start()

    def run(self):
        self._lock.acquire()

        if not self._channel.is_open:
            self._channel.open()

        self._channel.queue_declare(queue=self._queue, **self._queue_options)
        self._channel.basic_publish(**self._kwargs)
        self._channel.close()

        self._lock.release()

class Consumer(AMQPAgent):
    def consume(self, callback):
        if not self._queue:
            raise RuntimeError('Queue is not defined.')

        self._kwargs = {
            'queue':             queue,
            'consumer_callback': callback
        }
        self.start()

    def close(self):
        self._channel.stop_consuming()
        self._channel.close()

    def run(self):
        self._lock.acquire()

        if not self._channel.is_open:
            self._channel.open()

        def wrapper(channel, method, properties, body):
            pass

        self._channel.queue_declare(queue=self._queue, **self._queue_options)
        self._channel.basic_consume(**self._kwargs)
        self._channel.start_consuming()

        self._lock.release()

class AMQPManager(object):
    def __init__(self, parameters, connection_type=None, default_queue=None,
                 default_queue_options=None):
        self._parameters      = parameters
        self._connection_type = connection_type or BlockingConnection
        self._connections     = {}
        self._channels        = {}
        self._publishers      = {}
        self._consumers       = {}
        self._default_queue   = default_queue
        self._default_queue_options = default_queue_options

    def connection(self, id):
        if id not in self._connections:
            self._connections[id] = self._connection_type(self._parameters)

        if not self._connections[id].is_open:
            self._connections[id].connect()

        return self._connections[id]

    def channel(self, id):
        if id not in self._channels:
            self._channels[id] = self.connection(id).channel()

        if not self._channels[id].is_open:
            self.connection(id)
            self._channels[id].open()

        return self._channels[id]

    def agent(self, id, kind):
        agent = kind(self.channel(id))

        if self._default_queue:
            agent.set_queue(self._default_queue)

        if self._default_queue_options:
            agent.set_options(self._default_queue_options)

        return agent

    def publisher(self, id=None):
        if not id:
            return self.agent(id, Publisher)

        if id not in self._publishers:
            self._publishers[id] = self.agent(id, Publisher)

        return self._publishers[id]

    def consumer(self, id=None):
        if not id:
            return self.agent(id, Consumer)

        if id not in self._consumers:
            self._consumers[id] = self.agent(id, Consumer)

        return self._consumers[id]