import json
import bson
import pika
import pymongo
import time
from tori.db.common import Serializer
from neptune.common import Controller, WebSocket, RestController
from neptune.beacon.model import BeaconMessage
from neptune.security.decorator import access_control, restricted_to_xhr_only
from neptune.security.model import Credential, WebAccessMode

class Beacon(Controller):
    def get(self):
        self.render('beacon/beacon.html')

    def put(self):
        """ Form marking all messages as read.
        """
        entity_manager = self.component('db')
        session        = entity_manager.open_session()
        collection     = session.repository(BeaconMessage)
        criteria       = collection.new_criteria()

        criteria.where('owner', self.user.id)
        criteria.where('is_read', false)
        criteria.order('created', pymongo.DESCENDING)

        for message in collection.find(criteria):
            message.is_read = True

            session.persist(message)

        session.flush()

class BeaconSocket(WebSocket):
    consumer = None

    @property
    def queue_name(self):
        return '{}_{}'.format(self.component('amqp')._default_queue, str(self.user.id))

    def open(self):
        amqp = self.component('amqp')

        def handler(channel, method, properties, body):
            self.write_message(json.dumps({
                'current_time': time.time(),
                'message':      body
            }))
            channel.basic_ack(delivery_tag = method.delivery_tag)

        self.consumer = amqp.consumer('beacon')
        self.consumer.set_queue(self.queue_name)
        self.consumer.consume(handler)

    def close(self):
        self.consumer.abort()

class BeaconAPI(RestController):
    serializer = Serializer()

    @restricted_to_xhr_only
    @access_control(WebAccessMode.ANY_AUTHENTICATED_ACCESS, relay_point='/login')
    def list(self):
        accepted_at = time.time()
        limit = int(self.get_argument('limit', None) or 25)

        entity_manager = self.component('db')
        session        = entity_manager.open_session()
        collection     = session.repository(BeaconMessage)

        recent_criteria = self.__create_basic_criteria(collection, self.user)
        recent_criteria.limit(limit)
        
        total_count_criteria  = self.__create_basic_criteria(collection, self.user)
        unread_count_criteria = self.__create_basic_criteria(collection, self.user)
        unread_count_criteria.where('is_read', False)

        messages = []

        for message in collection.find(recent_criteria):
            serialized_data = {
                'id':   str(message.id),
                'type': message.kind,
                'body': message.body,
                'created': message.created,
                'is_read': message.is_read
            }

            messages.append(serialized_data)

        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps({
            'meta': {
                'total_count':   collection.count(total_count_criteria),
                'unread_count':  collection.count(unread_count_criteria),
                'produced_time': time.time(),
                'response_time': time.time() - accepted_at
            },
            'messages': messages
        }))

    def create(self):
        request = self.request
        email   = None
        token   = None

        try:
            email = request.headers['X-Agent-User']
            token = request.headers['X-Agent-Token']
        except KeyError as exception:
            return self.set_status(400)

        # Authenticate the token.
        entity_manager = self.component('db')
        session        = entity_manager.open_session()
        collection     = session.repository(Credential)
        criteria       = collection.new_criteria()

        criteria.where('login', email)
        criteria.limit(1)

        credential = collection.find(criteria)

        if not credential:
            return self.set_status(403)

        if credential.api_token() != token:
            return self.set_status(401)

        # Push the message to the queue.
        amqp       = self.component('amqp')
        publisher  = amqp.publisher('beacon')
        properties = pika.BasicProperties(
            app_id       = 'nep_beacon',
            content_type = 'application/json'
        )

        data = json.loads(self.request.body)

        data['type'] = data['type'] or 'notice'

        publisher.publish(
            json.dumps(data),
            '{}_{}'.format(amqp._default_queue, str(credential.id)),
            properties = properties
        )

        # Push the message to the database.
        data    = json.loads(self.request.body)
        message = BeaconMessage(
            owner  = credential,
            sender = None,
            body   = data['body'],
            kind   = data['type'] or 'notice'
        )

        session.persist(message)
        session.flush()

        self.set_status(200)

    def remove(self, id):
        oid = bson.ObjectId(id)

        entity_manager = self.component('db')
        session        = entity_manager.open_session()
        collection     = session.repository(BeaconMessage)
        message        = collection.get(oid)

        if not message:
            return self.set_status(404)

        session.delete(message)
        session.flush()

    def __create_basic_criteria(self, collection, user):
        criteria = collection.new_criteria()

        criteria.where('owner', user.id)
        criteria.order('created', pymongo.DESCENDING)

        return criteria