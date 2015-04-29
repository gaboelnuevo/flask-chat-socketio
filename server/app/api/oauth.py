import json
from datetime import datetime, timedelta
from flask import Blueprint
from flask import session, request, url_for, make_response
from flask import render_template, redirect, jsonify
from flask_oauthlib.provider import OAuth2Provider, OAuth2RequestValidator
from flask.ext.login import current_user, login_user, logout_user
from werkzeug.security import gen_salt
from .. import config

from flask.ext.cors import cross_origin

from ..data.models import Client, Grant, Token, User
from ..data import mydb as db

oauth_blue = Blueprint( 'oauth_blue', __name__,template_folder='../templates')
oauth = OAuth2Provider()


@oauth.clientgetter
def load_client(client_id):
    return Client.query.filter_by(client_id=client_id).first()

@oauth.grantgetter
def load_grant(client_id, code):
    return Grant.query.filter_by(client_id=client_id, code=code).first()


@oauth.grantsetter
def save_grant(client_id, code, request, *args, **kwargs):
    # decide the expires time yourself
    expires = datetime.utcnow() + timedelta(seconds=100)
    grant = Grant(
        client_id=client_id,
        code=code['code'],
        redirect_uri=request.redirect_uri,
        _scopes=' '.join(request.scopes),
        user=current_user,
        expires=expires
    )
    grants = Grant.query.filter_by(
        client_id=request.client.client_id,
        user_id=current_user.id
    )
    for g in grants:
        db.session.delete(g)
    db.session.add(grant)
    db.session.commit()
    return grant


@oauth.tokengetter
def load_token(access_token=None, refresh_token=None):
    if access_token:
        return Token.query.filter_by(access_token=access_token).first()
    elif refresh_token:
        return Token.query.filter_by(refresh_token=refresh_token).first()


@oauth.tokensetter
def save_token(token, request, *args, **kwargs):
    toks = Token.query.filter_by(
        client_id=request.client.client_id,
        user_id=request.user.id
    )
    # make sure that every client has only one token connected to a user
    for t in toks:
        db.session.delete(t)

    expires_in = token.pop('expires_in')
    expires = datetime.utcnow() + timedelta(seconds=expires_in)

    tok = Token(
        access_token=token['access_token'],
        refresh_token=token['refresh_token'],
        token_type=token['token_type'],
        _scopes=token['scope'],
        expires=expires,
        client_id=request.client.client_id,
        user_id=request.user.id,
    )
    db.session.add(tok)
    db.session.commit()
    return tok


@oauth_blue.route('/revoke', methods=['POST'])
@oauth.revoke_handler
def revoke_token():
    pass

@oauth.invalid_response
def invalid_require_oauth(req):
    return jsonify({'error': "invalid_token", 'message':req.error_message}), 401

@oauth_blue.route('/token')
@cross_origin()
@oauth.token_handler
def access_token():
    if hasattr(config, 'OAUTH2_PROVIDER_TOKEN_EXPIRES_IN'):
        expire_time = config.OAUTH2_PROVIDER_TOKEN_EXPIRES_IN
    else:
        expire_time = 3600
    return {'oauth_expires_in': expire_time}


def isOficialClient(client_id):
    if client_id in config.OFICIAL_CLIENTS_KEYS:
        return True
    return False

@oauth_blue.route('/authorize', methods=['GET', 'POST'])
@cross_origin()
@oauth.authorize_handler
def authorize(*args, **kwargs):
    user = current_user
    client_id = kwargs.get('client_id')
    response_type = kwargs.get('response_type')
    redirect_uri = kwargs.get('redirect_uri')
    data = {"response_type": response_type, "client_id": client_id, "redirect_uri": redirect_uri}
    if request.method == 'GET':
        if not user.is_authenticated():
            session['auth_args'] = json.dumps(data)
            return redirect(url_for('users.login'))
        oficial_client = isOficialClient(client_id)
        client = Client.query.filter_by(client_id=client_id).first()
        kwargs['client'] = client
        kwargs['user'] = user
        kwargs['oficial_client'] = oficial_client
        return render_template('authorize.html', **kwargs)
    username = request.form.get('username', None)
    password = request.form.get('password', None)
    if username and password:
        #if user.is_authenticated():
        #    return redirect(url_for('.error', error='user_have_been_logged'))
        user = User.query.filter_by(username = username).first()
        if not user or not user.is_valid_password(password):
            return redirect(url_for('.error', error='incorrect_user_or_password'))
        login_user(user)
        return True
    confirm = request.form.get('confirm', 'no')
    redirect_uri = request.form.get('redirect_uri', None)
    if not user.is_authenticated():
        return redirect(url_for('users.login'))
    if redirect_uri:
        return confirm == 'yes' or redirect(redirect_uri + '?error=user_denied&error_reason=user denied&error_description=User cancel the authentication')
    return confirm == 'yes' or redirect(url_for('.error', error='user_denied'))

@oauth_blue.route('/errors')
@cross_origin()
def error(*args, **kwargs):
    error = request.args.get('error')
    return make_response(jsonify({'error': error}), 401)

#fake callback
@oauth_blue.route('/fakecallback')
@cross_origin()
def show_request_token():
    return jsonify({'code':
        request.args.get("code")
    })

# @oauth_blue.route('/clientgenerator')
# def client():
#     user = current_user
#     if not user.is_authenticated():
#         return redirect(url_for('users.login'))
#     item = Client(
#         client_id=gen_salt(40),
#         client_secret=gen_salt(50),
#         _redirect_uris=' '.join([
#             'http://localhost:8000/authorized',
#             'http://127.0.0.1:8000/authorized',
#             'http://127.0.1:8000/authorized',
#             'http://127.1:8000/authorized',
#             ]),
#         _default_scopes='email',
#         user_id=user.id,
#     )
#     db.session.add(item)
#     db.session.commit()
#     return jsonify(
#         client_id=item.client_id,
#         client_secret=item.client_secret,
#     )
