from eryri.security.model import Credential

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