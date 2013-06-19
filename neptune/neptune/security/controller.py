from tori.controller import Controller
from tori.decorator.controller import renderer
from neptune.security.model import Credential

@renderer('neptune.view')
class Authentication(Controller):
    def get(self):
        self.render('security/authentication.html')

    def post(self):
        login    = self.get_argument('u', None)
        password = self.get_argument('p', None)

        if not login and not password:
            return self.set_status(400)

        manager = self.component('db')
        session = manager.open_session()

        users    = session.collection(User)
        criteria = users.new_criteria()

        criteria.where('login', login)
        criteria.where('password', password)
        criteria.limit(1)

        user = users.find(criteria)

        if not user:
            return self.set_status(403)

        self.set_status(200)