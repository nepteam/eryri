import random
import sys
import time
from eryri.security.model import Credential

class RandomUserCreator(object):
    """ Command to randomly create a new user
    """
    _last_names = [
        'Satou',
        'Suzuki',
        'Takahashi',
        'Tanaka',
        'Watanabe',
        'Itou',
        'Nakamura',
        'Kobayashi',
        'Yamamoto',
        'Katou',
        'Yoshida',
        'Yamada',
        'Sasaki',
        'Yamaguchi',
        'Matsumoto',
        'Inoue',
        'Kimura',
        'Shimizu',
        'Hayashi',
        'Saitou'
    ]
    _first_names = [
        'Hiroto',
        'Ren',
        'Yuto',
        'Shota',
        'Yamato',
        'Sota',
        'Yuma',
        'Sora',
        'Haruto',
        'Sho',
        'Yui',
        'Aoi',
        'Hina',
        'Rin',
        'Ria',
        'Yuina',
        'Miu',
        'Sakura',
        'Miyu',
        'Nanami'
    ]

    def __init__(self, db, password_service):
        self._db      = db
        self._session = None
        self._ps      = password_service

    def init(self):
        self._session = self._db.open_session()

    def clean_up(self):
        del self._session

    def define_arguments(self, argument_parser):
        argument_parser.add_argument('-l', '--limit', type=int)

    def execute(self, args):
        if not self._session:
            raise IOError('The database session is not defined.')

        first_name_count = len(self._first_names)
        last_name_count  = len(self._last_names)

        password_salt = self._ps.generate_salt()
        credentials   = self._session.collection(Credential)

        criteria = credentials.new_criteria()

        for iteration in range(args.limit):
            findex = random.randint(0, 10000) % first_name_count
            lindex = random.randint(0, 10000) % last_name_count
            alias  = 'u{}.{}'.format(time.time(), iteration)
            fname  = self._first_names[findex]
            lname  = self._last_names[lindex]

            credential    = credentials.new(
                alias    = alias,
                login    = '{}@eryri.local'.format(alias),
                password = self._ps.generate_hash(alias, password_salt),
                salt     = password_salt,
                name     = '{} {}'.format(fname, lname),
                roles    = ['user']
            )

            credentials.persist(credential)

            sys.stdout.write('.')

        print('')

        credentials.commit()

        print('Done')

class UserCreator(object):
    """ Command to create a new user
    """
    def __init__(self, db, password_service):
        self._db      = db
        self._session = None
        self._ps      = password_service

    def init(self):
        self._session = self._db.open_session()

    def clean_up(self):
        del self._session

    def define_arguments(self, argument_parser):
        argument_parser.add_argument('-u', '--username', required=True)
        argument_parser.add_argument('-l', '--login', required=True)
        argument_parser.add_argument('-p', '--password', required=True)
        argument_parser.add_argument('-n', '--name', required=True)
        argument_parser.add_argument('-r', '--roles', nargs='+', required=True)

    def execute(self, args):
        if not self._session:
            raise IOError('The database session is not defined.')

        credentials = self._session.collection(Credential)
        criteria    = credentials.new_criteria()

        criteria.where('login', args.login)
        criteria.limit(1)

        if credentials.find(criteria):
            raise RuntimeError('This user already exists.')

        password_salt = self._ps.generate_salt()
        credential    = credentials.new(
            alias    = args.username,
            login    = args.login,
            password = self._ps.generate_hash(args.password, password_salt),
            salt     = password_salt,
            name     = args.name,
            roles    = args.roles
        )

        credentials.persist(credential)
        credentials.commit()

        print('Done')