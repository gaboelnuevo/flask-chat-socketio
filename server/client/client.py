from flask import Flask, url_for, session, request, jsonify, redirect
from flask import render_template
from flask_oauthlib.client import OAuth
#from flask_debugtoolbar import DebugToolbarExtension

CLIENT_ID = 'YcrXQPOHi4UBnKwYbJllqySVAPtsPS79irMWbCpX'
CLIENT_SECRET = 'c4wO1D90yCxULIgKP04TH0uvMbCkjJpbeGIpN9bBcwxI2pXwBB'


app = Flask(__name__, template_folder='templates')
app.debug = True
app.secret_key = 'secret'
oauth = OAuth(app)

#Debug toolbar
#toolbar = DebugToolbarExtension(app)

remote = oauth.remote_app(
    'remote',
    consumer_key=CLIENT_ID,
    consumer_secret=CLIENT_SECRET,
    request_token_params={'scope': 'email'},
    base_url='http://127.0.0.1:5000/api/v1/',
    request_token_url=None,
    access_token_url='http://127.0.0.1:5000/oauth/token',
    authorize_url='http://127.0.0.1:5000/oauth/authorize'
)


@app.route('/')
def index():
    if 'remote_oauth' in session:
        resp = remote.get('me')
        print resp.data
        return jsonify(resp.data)
    next_url = request.args.get('next') or request.referrer or None
    return remote.authorize(
        callback=url_for('authorized', next=next_url, _external=True)
    )

@app.route('/api_console')
def console():
    if 'remote_oauth' in session:
        return render_template('api_console.html')
    else:
        return redirect('/')

@app.route('/service_console', methods=['POST'])
def service_console():
    uri=request.form['uri']
    query_method=request.form['query_method']
    query_body=request.form['query_body']
    if query_method == 'GET':
        resp = remote.get(uri)
    elif query_method == 'POST':
        resp = remote.post(uri, format='json', data=query_body)
    elif query_method == 'PUT':
        resp = remote.put(uri, format='json', data=query_body)
    elif query_method == 'DELETE':
        resp = remote.delete(uri)
    return jsonify(resp.data)

@app.route('/authorized')
def authorized():
    if 'remote_oauth' in session:
        return redirect('/')
    resp = remote.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    try:
        session['remote_oauth'] = (resp['access_token'], '')
    except:
        return jsonify(resp)
    return "authorized"


@remote.tokengetter
def get_oauth_token():
    return session.get('remote_oauth')

if __name__ == '__main__':
    import os
    os.environ['DEBUG'] = 'true'
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'
    app.run(host='localhost', port=8008)
