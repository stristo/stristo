#!/usr/bin/env python2

from flask import Flask
import storage
import uuid

app = Flask(__name__)
app.config.update(
    COUCHDB_SERVER="http://localhost:5984",
    COUCHDB_DATABASE="stristo"
)
s = storage.Storage(app)


def write(message, token=None):
    if not token:
        token = uuid.uuid4().hex
    s.store(token, message)
    return token


def read(token, num=1, full=False):
    return s.obtain(token, num, full)


@app.route('/write/<message>')
def write_to_new_token(message):
    return write(message)


@app.route('/write/<token>/<message>')
def write_to_existing_token(message, token):
    return write(message, token)


@app.route('/read/<token>')
def read_newest_message(token):
    return read(token)


@app.route('/read/<token>/<amount>')
def read_messages(token, amount):
    return read(token, amount)


@app.route('/readfull/<token>/<amount>')
def read_full_messages(token, amount):
    return read(token, amount, full=True)


if __name__ == '__main__':
    # Only executed if directly run (not via wsgi)
    app.run(debug=True)
