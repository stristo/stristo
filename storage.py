import couchdb

class Storage:

    def __init__(self):
        self.manager = couchdb.CouchDBManager()
