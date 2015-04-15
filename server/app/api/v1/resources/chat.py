from flask.ext.restful import Resource
from flask.ext.restful import reqparse
#from flask.ext.restful import fields, marshal

from flask.ext.restful import fields
from flask.ext.restful import marshal_with


from flask import jsonify
from flask import request
from flask import abort

from ....data.models import Chat as ChatModel, Messages as MessagesModel
from ....data import mydb as db

from sqlalchemy.sql import and_, or_
from sqlalchemy.orm import eagerload



parser_chat = reqparse.RequestParser()
parser_chat.add_argument('name', type=str, required=True,help="Name cannot be blank!")

parser_msg = reqparse.RequestParser()
parser_msg.add_argument('body', type=str, required=True,help="Body cannot be blank!")

parser_join_chat = reqparse.RequestParser()
parser_join_chat.add_argument('chat_id', type=int, required=True,help="Chat id is necesary!")

chat_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'uri': fields.Url('chat'),
}

msg_fields = {
    'id': fields.Integer,
    'chat_id': fields.Integer,
    'uri': fields.Url('msg'),
}

class ChatList(Resource):
    def get(self):
        chats = []
        q = ChatModel.query.all()
        for chat in q:
            chats.append(chat.toCustomDict(merge={'joined':chat.isUserJoined(request.oauth.user.id)}))
        return jsonify(result = chats)

    @marshal_with(chat_fields)
    def post(self):
        args = parser_chat.parse_args()
        chat = ChatModel(args['name'], request.oauth.user.id)
        db.session.add(chat)
        chat.users.append(request.oauth.user)
        db.session.commit()
        return chat.toDict(), 201

class Chat(Resource):
    def get(self, id):
        chat = ChatModel.query.filter(ChatModel.id == id).first_or_404()
        return jsonify(chat.toCustomDict(merge={'joined':chat.isUserJoined(request.oauth.user.id)}))

class JoinedChat(Resource):
    @marshal_with(chat_fields)
    def get(self, id):
        chat = ChatModel.query.filter(ChatModel.id == id).first_or_404()
        return chat.toDict()

class JoinedChatList(Resource):
    def get(self):
        chats = [];
        q = ChatModel.query.filter(ChatModel.users.any(id=request.oauth.user.id))
        for chat in q:
            chats.append(chat.toDict())
        return jsonify(chats = chats)

    @marshal_with(chat_fields)
    def post(self):
        args = parser_join_chat.parse_args()
        q = ChatModel.query.filter(and_(ChatModel.id == args['chat_id'],ChatModel.users.any(id=request.oauth.user.id))).count()
        if q:
            abort(400)
        chat = ChatModel.query.filter(ChatModel.id == args['chat_id']).first()
        if not chat:
            abort(400)
        chat.users.append(request.oauth.user)
        db.session.commit()
        return chat.toDict(), 201

class MessagesList(Resource):
    def get(self, chat_id):
        parser = reqparse.RequestParser()
        parser.add_argument('after_id', type=int, location='args')
        parser.add_argument('before_id', type=int, location='args')
        parser.add_argument('limit', type=int, location='args')
        args = parser.parse_args()
        messages = []
        chat = ChatModel.query.filter(ChatModel.id == chat_id).first_or_404()
        if not chat.isUserJoined(request.oauth.user.id):
            abort(401)
        q = MessagesModel.query
        q = q.filter(MessagesModel.chat_id == chat_id)

        if(args['after_id']):
            q = q.filter(MessagesModel.id > args['after_id'])
        if(args['before_id']):
            q = q.filter(MessagesModel.id < args['before_id'])
        if(args['limit']):
            if (args['after_id']):
                q = q.limit(args['limit'])
            else:
                q = q.order_by(MessagesModel.id.desc()).limit(args['limit']).from_self().options(eagerload(MessagesModel.user)).order_by(MessagesModel.id)
        for msg in q:
            messages.append(msg.toDict())
        return jsonify(messages = messages)

    @marshal_with(msg_fields)
    def post(self, chat_id):
        args = parser_msg.parse_args()
        chat = ChatModel.query.filter(ChatModel.id == chat_id).first_or_404()
        if not chat.isUserJoined(request.oauth.user.id):
            abort(401)
        msg = MessagesModel(chat_id, request.oauth.user.id, args['body'])
        db.session.add(msg)
        db.session.commit()
        return msg.toDict(), 201

class Message(Resource):
    def get(self, chat_id, id):
        msg = MessagesModel.query.filter(and_(MessagesModel.chat_id == chat_id, MessagesModel.id == id).first_or_404())
        return jsonify(message = msg)
