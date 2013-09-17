import json
import re
import time
from bson.objectid import ObjectId
from eryri.common import Controller
from eryri.security.model import Credential, WebAccessMode
from eryri.security.decorator import access_control

class User(Controller):
    @access_control(WebAccessMode.RESTRICTED_ACCESS, roles=['master', 'admin'], relay_point='/login')
    def get(self):
        session = self.component('db').open_session()
        query   = self.get_argument('query', None)
        uid     = self.get_argument('uid', None)

        if query:
            repository = session.collection(Credential)
            criteria   = repository.new_criteria()
            re_query  = re.compile(query, re.IGNORECASE)

            criteria.where('name', re_query)

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

            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps({
                'updated': time.time(),
                'count':   len(simplified_users),
                'users':   simplified_users
            }))

            return

        if uid:
            repository = session.collection(Credential)

            id   = ObjectId(uid)
            user = repository.get(id)

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

            return

        self.render('management/user.html')