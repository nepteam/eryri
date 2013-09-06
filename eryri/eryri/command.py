class Database(object):
    """ Command to manage the database
    """
    def __init__(self, db):
        self._db = db
    
    def init(self):
        self._session = self._db.open_session()

    def clean_up(self):
        del self._session
    
    def define_arguments(self, argument_parser):
        argument_parser.add_argument('-d', '--delete', action='store_true')

    def execute(self, args):
        if args.delete:
            self._db.db.connection.drop_database(self._db._name)
            print('The database "{}" has been deleted.'.format(self._db._name))