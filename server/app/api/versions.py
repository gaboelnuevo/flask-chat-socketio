#import versions

from .v1 import v1

def register_versions(app):
	v1.register(app)
