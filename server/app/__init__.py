# coding: utf-8
from flask import Flask
from flask import session, request, url_for
from flask import render_template, redirect, jsonify
from flask.ext.login import current_user
from flask import make_response
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.cors import CORS
from .blueprints import register_blueprints
import re

from data import mydb as db
from api.api import register_apis
import config
from data.models import *
import logging

app = Flask(__name__, template_folder='templates')
app.config.from_object(config)

#app.config['SQLALCHEMY_ECHO'] = True

# add the flask log handlers to sqlalchemy
loggers = [logging.getLogger('sqlalchemy.engine'),
logging.getLogger('flask_oauthlib')]
for logger in loggers:
    for handler in app.logger.handlers:
        logger.addHandler(handler)

#Debug toolbar
#toolbar = DebugToolbarExtension(app)

#enable CORS for /api/* or use @cross_origin() decorator
cors = CORS(app, resources={r"/api/*": {"origins": "*"}}, allow_headers=['Authorization','Content-Type'])

#register extensions
db.init_app(app)

#register apis
register_apis(app)

#register blueprints
register_blueprints(app)

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
