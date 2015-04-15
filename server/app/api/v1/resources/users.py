from flask.ext.restful import Resource

from flask import jsonify
from flask import request

from ....data.models import User

class Me(Resource):
    def get(self):
        user = request.oauth.user
        return jsonify(user.toDict())

class UserInfo(Resource):
    def get(self, username):
        user = User.query.filter_by(username=username).first_or_404()
        return jsonify(user.toCustomDict(only=['id', 'name', 'contry']))
