
# import blue prints

from .users_manager import controller as users_manager
from .users_manager.extensions import login_manager

# register blueprints you want
def register_blueprints(app):
	# users
	app.register_blueprint(users_manager)
	login_manager.init_app(app)

	#websocket chat
	from .chatio import chatio as chatio_blueprint
	app.register_blueprint(chatio_blueprint)
