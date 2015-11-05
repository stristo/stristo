from flaskext import couchdb
import time


class MessageContainer(couchdb.Document):
    messages = couchdb.ListField(couchdb.TextField())


class Storage:

    def __init__(self, app):
        self.manager = couchdb.CouchDBManager()
        self.manager.add_document(MessageContainer)
        self.manager.setup(app)

    def store(self, token, value):

        if MessageContainer.load(token):
            message_container = MessageContainer.load(token)
        else:
            message_container = MessageContainer(id=token)

        message_container.messages = [value] + list(message_container.messages)
        message_container.store()

    def obtain(self, token, limit):

        if MessageContainer.load(token):
            messages = MessageContainer.load(token).messages[:int(limit)]
            return str([m.encode('utf-8') for m in messages])
        return "TOKEN %s is invalid!" % token
