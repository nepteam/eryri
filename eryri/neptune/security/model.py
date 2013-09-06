from hashlib import sha1, md5
from tori.db.entity import entity

class WebAccessMode(object):
    RESTRICTED_ACCESS        = 1
    ONLY_ANONYMOUS_ACCESS    = 2
    ANY_AUTHENTICATED_ACCESS = 3

class User(object):
    """ User data
    """
    def __init__(self, id, alias, email, name, roles=[], api_token=None):
        self.id = id
        self.alias = alias
        self.email = email
        self.name  = name
        self.roles = roles
        self.api_token = api_token

    def gravatar(self):
        return 'http://www.gravatar.com/avatar/{}'.format(md5(self.email).hexdigest())

@entity
class Credential(object):
    def __init__(self, alias, login, password, salt, name, roles=[]):
        self.alias = alias
        self.login = login
        self.password = password
        self.salt = salt
        self.name = name
        self.roles = roles

    def api_token(self):
        return sha1('{}{}'.format(self.salt, self.alias)).hexdigest()