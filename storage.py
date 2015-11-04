from flaskext import couchdb


class Storage:

    def __init__(self, app):
        self.manager = couchdb.CouchDBManager()
        self.manager.setup(app)

    def store(token, value):
        #couchdb.g.couch[token] = {'msg': value}
        print("sd")

    def obtain(token, limit):
        message = str(couchdb.g.couch.get(token))
