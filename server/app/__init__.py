# coding: utf-8
from flask import Flask

from flask import session, request, url_for
from flask import render_template, redirect, jsonify

from flask.ext.login import current_user
from flask import make_response

from flask.ext.socketio import SocketIO
socketio = SocketIO()

from settings import settings_start

import re

app = Flask(__name__, template_folder='templates')
app.config.from_object(config)
settings_start(app)

socketio.init_app(app)

@app.route('/')
def home():
    user = current_user
    return render_template('home.html', user=user)

@app.errorhandler(404)
def not_found(error):
    if re.match("/api/*", request.path):
	return make_response(jsonify({'error': 'Not found'}), 404)
    return make_response('Not found', 404)

@app.errorhandler(401)
def not_found(error):
    if re.match("/api/*", request.path):
	return make_response(jsonify({'error': 'Unauthorized'}), 401)
    return make_response('Unauthorized', 401)
