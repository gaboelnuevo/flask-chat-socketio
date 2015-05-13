from setuptools import setup

setup(name='airchatServer',
      version='1.0',
      description='A basic Flask app server',
      author='Gabriel O. Sabillon',
      author_email='gabrielsabillon@googlemail.com',
      url='http://www.python.org/sigs/distutils-sig/',
      install_requires=[
         'Flask>=0.10.1',
         'werkzeug==0.9.4',
         'Flask-OAuthlib>=0.5.0',
         'Flask-WTF==0.9.3',
         'Flask-Login==0.2.7',
         'Flask-Script==2.0.5',
         'Flask-Migrate==1.3.0',
         'Flask-Cors==1.10.2',
         'Flask-DebugToolbar==0.9.2',
         'Flask-RESTful==0.3.1',
         'mysql-python',
         'alembic==0.7.2',
         'Flask-SocketIO==0.6.0',
         'gevent==1.0.1',
         'gevent-socketio==0.3.6',
         'gevent-websocket==0.9.3']
     )
