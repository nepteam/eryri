from tori.db.entity import entity

@entity
class Credential(object):
    def __init__(self, login, password, salt, name):
        self.login = login
        self.password = password
        self.salt = salt
        self.name = name