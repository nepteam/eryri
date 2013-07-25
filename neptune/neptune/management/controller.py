from neptune.common import Controller
from neptune.security.model import Credential

class User(Controller):
    def get(self):
        session = self.component('db').open_session()
        repository = session.collection(Credential)

        self.render('management/user.html', users = repository.find(repository.new_criteria()))