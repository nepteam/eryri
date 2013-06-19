import unittest as t
from neptune.security.service import PasswordService

class TestCase(t.TestCase):
    def setUp(self):
        self.service = PasswordService()

    def test_generate_salt(self):
        self.assertEqual(32, len(self.service.generate_salt()))

    def test_generate_hash(self):
        plain_password = 'panda'
        password_salt  = 'qwerty'
        password_hash  = self.service.generate_hash(plain_password, password_salt)

        self.assertEqual('9bda272dbc2b040a6fb231d5b1ba128c6df33620', password_hash)
