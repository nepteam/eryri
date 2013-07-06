import pika
from neptune.common import Controller
from neptune.security.model import Credential

class Beacon(Controller):
    def get(self):
        self.render('management/beacon.html')

class BeaconAPI(Controller):
    def post(self):
        request = self.request
        email   = None
        token   = None

        try:
            email = request.headers['X-Agent-User']
            token = request.headers['X-Agent-Token']
        except KeyError as exception:
            return self.set_status(400)

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

        amqp       = self.component('amqp')
        publisher  = amqp.publisher('beacon')
        properties = pika.BasicProperties(
            app_id       = 'nep_beacon',
            content_type = 'application/json'
        )

        publisher.publish(
            amqp._default_queue,
            self.request.body,
            properties = properties
        )

        self.set_status(200)