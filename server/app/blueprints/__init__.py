
# imports blue prints

from .users  import controller as users
from .users.extensions import login_manager 

# register blueprints you want
def register_blueprints(app):
	# users
	app.register_blueprint(users)
	login_manager.init_app(app)
	
