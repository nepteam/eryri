from tori.db.entity import entity

@entity
class Credential(object):
    def __init__(self, login, password, salt, name, roles=[]):
        self.login = login
        self.password = password
        self.salt = salt
        self.name = name
        self.roles = roles