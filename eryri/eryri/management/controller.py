import json
import re
import time
from eryri.common import Controller
from eryri.security.model import Credential

class User(Controller):
    def get(self):
        session = self.component('db').open_session()
        query   = self.get_argument('query', None)

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

        self.render('management/user.html')