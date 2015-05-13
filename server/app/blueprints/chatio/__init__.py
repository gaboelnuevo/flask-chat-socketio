from flask import Blueprint

chatio = Blueprint('chatio', __name__)

import routes, events
