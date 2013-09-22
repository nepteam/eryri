import json
import re
import time
from bson.objectid import ObjectId
from eryri.common import Controller
from eryri.security.model import Credential, WebAccessMode
from eryri.security.decorator import access_control

class User(Controller):
    @access_control(WebAccessMode.RESTRICTED_ACCESS, roles=['master', 'admin'], relay_point='/login')
    def get(self, id=None):
        session = self.component('db').open_session()
        query = self.get_argument('query', None)
        uid   = self.get_argument('uid', id)

        if query:
            repository = session.collection(Credential)
            criteria   = repository.new_criteria()
            re_query   = re.compile(query, re.IGNORECASE)

            criteria.where('name', re_query)
            criteria.order('id')

            users = repository.find(criteria)
            simplified_users = [
                {
                    'id':       str(user.id),
                    'alias':    user.alias,
                    'name':     user.name,
                    'gravatar': user.gravatar(),
                    'roles':    user.roles
                }

                for user in users
            ]

            response = {
                'query':   query,
                'updated': time.time(),
                'count':   len(simplified_users),
                'users':   simplified_users
            }

            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(response))

            return

        if uid:
            repository = session.collection(Credential)

            id   = ObjectId(uid)
            user = repository.get(id)

            self._send_ok(user)

            return

        self.render('management/user.html')

    @access_control(WebAccessMode.RESTRICTED_ACCESS, roles=['master', 'admin'], relay_point='/login')
    def put(self, id):
        session    = self.component('db').open_session()
        repository = session.collection(Credential)

        id   = ObjectId(id)
        user = repository.get(id)

        if not user:
            return self.set_status(404)

        name     = self.get_argument('name', None)
        password = self.get_argument('password', None)

        if name:
            user.name = name

            repository.put(user)

            self._send_ok(user)

            return

        raise self.set_status(403)

    def _send_ok(self, user):
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps({
            'updated': time.time(),
            'user':    {
                'id':       str(user.id),
                'email':    user.login,
                'alias':    user.alias,
                'name':     user.name,
                'gravatar': user.gravatar(),
                'roles':    user.roles
            }
        }))