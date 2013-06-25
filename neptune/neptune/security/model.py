from tori.db.entity import entity

class WebAccessMode(object):
    RESTRICTED_ACCESS        = 1
    ONLY_ANONYMOUS_ACCESS    = 2
    ANY_AUTHENTICATED_ACCESS = 3

class User(object):
    """ User data
    """
    def __init__(self, email, name, roles=[]):
        self.email = email
        self.name  = name
        self.roles = roles

@entity
class Credential(object):
    def __init__(self, login, password, salt, name, roles=[]):
        self.login = login
        self.password = password
        self.salt = salt
        self.name = name
        self.roles = roles