from flask.ext.restful import Api
#from . import v1
#from .oauth import oauth

#api = Api(None, decorators=[oauth.require_oauth()])
#api = Api()

#def register_restful(app):
#	v1.register(app)

class APIVersion:
	def __init__(self,version, url_prefix, decorators=None):
		self.api = Api(None, decorators=decorators)
		self.version = version
		self.url_prefix = url_prefix

	def add_resource(self,resource, url, endpoint=None):
		if endpoint:
			self.api.add_resource(resource, self.url_prefix + url, endpoint=endpoint)
		else:
			self.api.add_resource(resource, self.url_prefix + url)

	def register(self, app):
		self.api.init_app(app)
