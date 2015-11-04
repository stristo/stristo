#!/usr/bin/env python3

from flask import Flask
import storage

app = Flask(__name__)


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


def write(message, token=None):
    if token:
        return 'You added message {msg} to token {tok}'.format(msg=message, tok=token)
    return 'Your token is NEW_TOKEN'


def read(token, num=1):
    return str(['sdad', 'asdasd', 'dsf'][:int(num)])


if __name__ == '__main__':
    app.run()
