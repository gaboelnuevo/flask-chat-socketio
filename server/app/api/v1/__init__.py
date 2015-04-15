from ..restful import APIVersion
from resources.users import Me, UserInfo
from resources.chat import Message, Chat, ChatList, JoinedChatList,  JoinedChat, MessagesList
from ..oauth import oauth

#declare api
v1 = APIVersion(1, '/api/v1', [oauth.require_oauth()])

#add resources
v1.add_resource(Me, '/me')
v1.add_resource(JoinedChatList, '/joined/chats')
v1.add_resource(JoinedChat, '/joined/chats/<int:id>')
v1.add_resource(UserInfo, '/user/<username>')
v1.add_resource(Chat, '/chats/<int:id>', endpoint='chat')
v1.add_resource(MessagesList, '/chats/<int:chat_id>/messages')
v1.add_resource(Message, '/chats/<int:chat_id>/messages/<int:id>', endpoint='msg')
v1.add_resource(ChatList, '/chats')
