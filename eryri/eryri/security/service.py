import random as r
import time as t
import hashlib as h

class PasswordService(object):
    FIRST_USABLE_ASCII_CODE = 33
    USABLE_CHARACTER_COUNT  = 127 - FIRST_USABLE_ASCII_CODE

    def random_int(self):
        return int(r.randint(0, 123456) * t.time())

    def generate_salt(self):
        salt = []

        for i in range(32):
            ascii_code = PasswordService.FIRST_USABLE_ASCII_CODE \
                + (self.random_int() % PasswordService.USABLE_CHARACTER_COUNT)

            salt.append(chr(ascii_code))

        return ''.join(salt)

    def generate_hash(self, password, salt):
        return h.sha1('%s%s'.format(password, salt)).hexdigest()