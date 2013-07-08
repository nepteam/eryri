from neptune.common             import Controller
from neptune.security.model     import Credential, WebAccessMode, User
from neptune.security.decorator import access_control

class Deauthentication(Controller):
    @access_control(WebAccessMode.ANY_AUTHENTICATED_ACCESS, relay_point='/login')
    def get(self):
        self.session.delete('user')

        if self.is_xhr:
            return self.set_status(200)

        self.redirect('/')

class Authentication(Controller):
    @access_control(WebAccessMode.ONLY_ANONYMOUS_ACCESS, relay_point='/dashboard')
    def get(self):
        self.render('security/authentication.html')

    @access_control(WebAccessMode.ONLY_ANONYMOUS_ACCESS)
    def post(self):
        login    = self.get_argument('u', None)
        password = self.get_argument('p', None)

        if not login and not password:
            return self.set_status(400)

        pass_srv = self.component('service.password')
        manager  = self.component('db')
        session  = manager.open_session()

        credentials = session.collection(Credential)
        criteria    = credentials.new_criteria()

        criteria.where('login', login)
        criteria.limit(1)

        credential = credentials.find(criteria)

        if not credential:
            return self.set_status(403)

        password = pass_srv.generate_hash(password, credential.salt)

        if credential.password != password:
            self.set_status(403)

        user = User(
            id    = credential.id,
            alias = credential.alias,
            email = credential.login,
            name  = credential.name,
            roles = credential.roles,
            api_token = credential.api_token()
        )

        self.session.set('user', user)

        self.set_status(200)
        self.set_header('Content-Type', 'application/json')
        self.render('security/authentication.ok.json', user=user)