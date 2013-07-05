from neptune.common import Controller

class Beacon(Controller):
    def get(self):
        self.render('management/beacon.html')

class BeaconAPI(Controller):
    def get(self):
        manager   = self.component('amqp')
        publisher = manager.publisher('beacon')
        publisher.publish(
            exchange='',
            routing_key=manager._default_queue,
            body='ping'
        )
        self.set_status(201)

    def post(self):
        self.set_status(201)