import time
from datetime import datetime
from flaskext.couchdb import (Document, CouchDBManager, TextField,
                              ListField, DictField, DateTimeField, Mapping)


class MessageContainer(Document):
    messages = ListField(DictField())


class Storage:

    def __init__(self, app):
        self.manager = CouchDBManager()
        self.manager.add_document(MessageContainer)
        self.manager.setup(app)

    def store(self, token, value):

        if MessageContainer.load(token):
            message_container = MessageContainer.load(token)
        else:
            message_container = MessageContainer(id=token)

        msg = {'value': value, 'created': str(datetime.now())}
        message_container.messages = [msg] + list(message_container.messages)
        message_container.store()

    def obtain(self, token, limit, full):

        if not MessageContainer.load(token):
            return "TOKEN %s is invalid!" % token

        messages_unicode = MessageContainer.load(token).messages[:int(limit)]
        messages = []
        for message in messages_unicode:
            messages.append(
                {str(k): str(v) for (k, v) in message.items()}
            )

        if full:
            return str(messages)

        return str([m['value'] for m in messages])
