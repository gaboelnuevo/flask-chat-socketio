from flask import request

from flask import Blueprint, jsonify

from .oauth import oauth, oauth_blue

from .versions import register_versions

from . import versions

from sockets import events

api_blue = Blueprint( 'api', __name__,template_folder='../templates')

def register_apis(app):
    oauth.init_app(app)
    app.register_blueprint(oauth_blue, url_prefix='/oauth')
    app.register_blueprint(api_blue, url_prefix='/api')
    register_versions(app)

@api_blue.route('/me')
@oauth.require_oauth()
def me():
    user = request.oauth.user
    return jsonify(username=user.username)
