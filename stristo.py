#!/usr/bin/env python2

from flask import Flask
from flask.ext.cors import CORS
from flask import jsonify
import storage
import exception

app = Flask(__name__)
app.config.update(
    COUCHDB_SERVER="http://localhost:5984",
    COUCHDB_DATABASE="stristo"
)
s = storage.Storage(app)

# Allow Cross Origin Resource Sharing on ALL ROUTES
cors = CORS(app)


def write(message, token=None):
    if not token:
        token = s.new_token()
    s.store(token, message)
    return token


def read(token, num=1, full=False):
    try:
        return s.obtain(token, num, full)
    except AttributeError:
        raise exception.InvalidUsage('Invalid Token')


@app.errorhandler(exception.InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/write/<message>')
def write_to_new_token(message):
    return write(message)


@app.route('/write/<token>/<message>')
def write_to_existing_token(message, token):
    if token and not s.token_exists(token):
        raise exception.InvalidUsage('Invalid Token')
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
    app.run(host='0.0.0.0', debug=True, port=5050)
