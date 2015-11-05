from flaskext import couchdb


class Storage:

    def __init__(self, app):
        self.manager = couchdb.CouchDBManager()
        self.manager.setup(app)

    def store(self, token, value):
        couchdb.g.couch[token] = {'msg': value}

    def obtain(self, token, limit):
        return str(couchdb.g.couch.get(token))
