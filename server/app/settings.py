#from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.cors import CORS
from .blueprints import register_blueprints
import re

from data import mydb as db
from api.api import register_apis
import logging

#CustomJSONEncoder imports
from flask.json import JSONEncoder
from datetime import datetime
import calendar

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        print type(obj)
        try:
            #Custom Dateformat
            if isinstance(obj, datetime):
                # if obj.utcoffset() is not None:
                #     obj = obj - obj.utcoffset()
                # millis = int(
                #     calendar.timegm(obj.timetuple()) * 1000 +
                #     obj.microsecond / 1000
                # )
                return obj.strftime('%Y-%m-%dT%H:%M:%S') #millis or obj.strftime('%Y-%m-%dT%H:%M:%S')
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)

def settings_start(app):
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

  #CustomJSONEncoder
  app.json_encoder = CustomJSONEncoder
