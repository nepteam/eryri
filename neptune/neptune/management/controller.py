from neptune.common import Controller

class Beacon(Controller):
    def get(self):
        self.render('management/beacon.html')

class BeaconAPI(Controller):
    def post(self):
        pass