from . import mydb as db
from . import DictMapper, mapper, mapperConfig
from datetime import datetime as date_time


from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.ext.associationproxy import association_proxy
from hashlib import sha512
#from backports.pbkdf2 import pbkdf2_hmac, compare_digest

from sqlalchemy import func

from random import SystemRandom
from flask.ext.login import UserMixin

import math

def haversine(lat1, lon1, lat2, lon2):
    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
    * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return c

class User(UserMixin, db.Model, DictMapper):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True)
    contry_id = db.Column(db.ForeignKey('contry.id'))
    contry = db.relationship('Contry')
    _password = db.Column(db.String(128))
    _salt = db.Column(db.String(128))

    @hybrid_property
    def password(self):
        return self._password

    # In order to ensure that passwords are always stored
    # hashed and salted in our database we use a descriptor
    # here which will automatically hash our password
    # when we provide it (i. e. user.password = "12345")
    @password.setter
    def password(self, value):
        # When a user is first created, give them a salt
        if self._salt is None:
            self._salt = bytes(SystemRandom().getrandbits(128))
        self._password = self._hash_password(value)

    def is_valid_password(self, password):
        """Ensure that the provided password is valid.

        We are using this instead of a ``sqlalchemy.types.TypeDecorator``
        (which would let us write ``User.password == password`` and have the incoming
        ``password`` be automatically hashed in a SQLAlchemy query)
        because ``compare_digest`` properly compares **all***
        the characters of the hash even when they do not match in order to
        avoid timing oracle side-channel attacks."""
        new_hash = self._hash_password(password)
        #return compare_digest(new_hash, self._password)
        return new_hash == self._password

    def _hash_password(self, password):
        #pwd = password.encode("utf-8")
        #salt = bytes(self._salt)
        #rounds = 100000
        #buff = pbkdf2_hmac("sha512", pwd, salt, iterations=rounds)
        #return bytes(buff)
        pwhash = sha512(password + self._salt)
        return pwhash.hexdigest()

    def __repr__(self):
        return "<User #{:d}>".format(self.id)

    @mapperConfig(only=['id', 'name', 'username'], exclude=['password','contry_id'])
    def defineMapper(self):
        pass

class Client(db.Model):
    client_id = db.Column(db.String(40), primary_key=True)
    #client_name = db.Column(db.String(40))
    client_secret = db.Column(db.String(55), nullable=False)

    user_id = db.Column(db.ForeignKey('user.id'))
    user = db.relationship('User')

    _redirect_uris = db.Column(db.Text)
    _default_scopes = db.Column(db.Text)

    @property
    def client_type(self):
        return 'public'

    @property
    def redirect_uris(self):
        if self._redirect_uris:
            return self._redirect_uris.split()
        return []

    @property
    def default_redirect_uri(self):
        return self.redirect_uris[0]

    @property
    def default_scopes(self):
        if self._default_scopes:
            return self._default_scopes.split()
        return []

class Grant(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id', ondelete='CASCADE')
    )
    user = db.relationship('User')

    client_id = db.Column(
        db.String(40), db.ForeignKey('client.client_id'),
        nullable=False,
    )
    client = db.relationship('Client')

    code = db.Column(db.String(255), index=True, nullable=False)

    redirect_uri = db.Column(db.String(255))
    expires = db.Column(db.DateTime)

    _scopes = db.Column(db.Text)

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []


class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(
        db.String(40), db.ForeignKey('client.client_id'),
        nullable=False,
    )
    client = db.relationship('Client')

    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id')
    )
    user = db.relationship('User')

    # currently only bearer is supported
    token_type = db.Column(db.String(40))

    access_token = db.Column(db.String(255), unique=True)
    refresh_token = db.Column(db.String(255), unique=True)
    expires = db.Column(db.DateTime)
    _scopes = db.Column(db.Text)

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []

#class Article(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    name = db.Column(db.String(55), nullable=False)
#    description = db.Column(db.String(140), nullable=False)
#    long_description = db.Column(db.Text, nullable=False)
#    price = db.Column(db.Float, nullable=False)
#    location = db.Column(db.String(40))
#    create_date = db.Column(db.DateTime, default=date_time.utcnow)
#    update_date = db.Column(db.DateTime, onupdate=date_time.utcnow)
#    user_id = db.Column(db.ForeignKey('user.id'))
#    user = db.relationship('User')

class Contry(db.Model, DictMapper):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(55), nullable=False)
    #default_currency_id = db.Column(db.ForeignKey('currency.id'))
    #default_currency = db.relationship('Currency')

    @mapperConfig()
    def defineMapper(self):
        pass

class ChatUsersDetail(db.Model, DictMapper):
    __tablename__ = 'chatusersdetail'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'),primary_key=True)
    special_key = db.Column(db.String(50))
    chat = db.relationship('Chat',backref="ChatUsersDetail")
    user = db.relationship("User")

    def __init__(self,user):
        self.user = user

    @mapperConfig(only=['user_id','chat_id'] ,exclude=['user'])
    def defineMapper(self):
        pass

class Chat(db.Model, DictMapper):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(55), nullable=False)
    user_id = db.Column(db.ForeignKey('user.id'))
    user = db.relationship('User')
    create_date = db.Column(db.DateTime, default=date_time.utcnow)
    users = association_proxy('ChatUsersDetail', 'user')
    is_private = db.Column(db.Boolean, unique=False, default=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    def __init__(self, name, user_id, latitude, longitude):
        self.name = name
        self.user_id = user_id
        self.latitude = latitude
        self.longitude = longitude

    @hybrid_property
    def peopleactive(self):
        return len(self.users)

    @hybrid_property
    def messages_count(self):
        return Messages.query.filter(Messages.chat_id == self.id).count()

    @hybrid_method
    def get_messages(self):
        return Messages.query.filter(Messages.chat_id == self.id).all()

    @hybrid_method
    def haversine(self,lon, lat):
         return haversine(self.lon,self.lat, lon, lat)

    @haversine.expression
    def haversine(cls, lat, lon):
        return func.haversine(cls.latitude, cls.longitude, lat, lon)

    @hybrid_method
    def isUserJoined(self, user_id):
        for u in self.users:
            if u.id == user_id:
                return True
        return False

    @mapperConfig(only=['id', 'name','peopleactive', 'is_private', 'messages_count', 'longitude', 'latitude'])
    def defineMapper(self):
        pass

class Messages(db.Model, DictMapper):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.ForeignKey('chat.id'))
    chat = db.relationship('Chat')
    body = db.Column(db.String(160), nullable=False)
    user_id = db.Column(db.ForeignKey('user.id'))
    user = db.relationship('User')
    create_date = db.Column(db.DateTime, default=date_time.utcnow)
    def __init__(self, chat_id, user_id, body):
        self.chat_id = chat_id
        self.body = body
        self.user_id = user_id

    @mapperConfig(exclude=['chat'])
    def defineMapper(self):
        pass
