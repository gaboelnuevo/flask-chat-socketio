from flask import session, request
from flask.ext.socketio import emit, join_room, leave_room
from ... import socketio
from ...data.models import Token

from functools import wraps

def load_token(access_token):
        return Token.query.filter_by(access_token=access_token).first()

def get_user():
    return session.get('chat_user', None)

#### @authenticated_only decorator
def authenticated_only(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        try:
            user = session.get('chat_user')
            return f(*args, **kwargs)
        except:
            request.namespace.disconnect()
    return wrapped

@socketio.on('connect', namespace='/chat')
def handle_connect():
    emit('event connected', {'msg': 'connection open!'})

@socketio.on('disconnect', namespace='/chat')
def handle_disconnect():
    pass
    #session.clear()

@socketio.on('authenticate', namespace='/chat')
def authenticate(message):
    token = load_token(message['token'])
    if token:
        session['chat_user'] = token.user
        emit('authenticated', {'msg': 'Authenticated successfully! Welcome ' + token.user.name })
    else:
        emit('authentication failed', {'msg': 'authentication failed. Invalid token!'})

@socketio.on('joined', namespace='/chat')
@authenticated_only
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = message['room']
    join_room(message['room'])
    user = get_user()
    emit('status', {'msg': user.name + ' has entered the room: '+ room}, room=room)

@socketio.on('text', namespace='/chat')
@authenticated_only
def msg(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    msg = message['msg']
    room = message['room']
    user = get_user()
    emit('message', {'msg': user.name  +':'+ msg}, room = room)

@socketio.on('left', namespace='/chat')
@authenticated_only
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    leave_room(message['room'])
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)
