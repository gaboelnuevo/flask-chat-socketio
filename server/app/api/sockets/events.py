from flask import session, request
from flask.ext.socketio import emit, join_room, leave_room
from ... import socketio
from ...data.models import Token, Messages as MessagesModel, Chat as ChatModel
from ...data import mydb as db

from functools import wraps

from flask import jsonify

def load_token(access_token):
        return Token.query.filter_by(access_token=access_token).first()

def get_user():
    return session.get('chat_user', None)

#### @authenticated_only decorator
def authenticated_only(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
            if session.get('chat_user', None):
                #try:
                return f(*args, **kwargs)
                #except Exception:
                #    raise Exception
            request.namespace.disconnect()
    return wrapped

@socketio.on('connect', namespace='/chat')
def handle_connect():
    emit('event connected', {'msg': 'connection open!'})

@socketio.on('disconnect', namespace='/chat')
def handle_disconnect():
    print "user disconeccted.."

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
    chat = ChatModel.query.filter(ChatModel.id == room).first_or_404()
    if chat.isUserJoined(user.id):
        Msg = MessagesModel(chat.id, user.id, msg)
        db.session.add(Msg)
        db.session.commit()
        emit('message', {'msg': Msg.toDict()}, room = room)

@socketio.on('left', namespace='/chat')
@authenticated_only
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    leave_room(message['room'])
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)



@socketio.on_error('/chat')
def error_handler_namespace(value):
    print "prueba"
    raise value


@socketio.on("error testing", namespace='/chat')
def raise_error_namespace(data):
    raise AssertionError()
