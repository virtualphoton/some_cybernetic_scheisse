from .oauth_tools import register_google
from flask import Blueprint, session, redirect
from authlib.integrations.flask_client import OAuth
from flask import url_for, current_app, render_template

authorization = Blueprint('authorization', __name__)

oauth = OAuth(current_app)
register_google(oauth)


@authorization.route('/login')
def login():
    return render_template('login.html')


@authorization.route('/login/google')
def login_google():
    google = oauth.create_client('google')
    redirect_uri = url_for('.authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@authorization.route('/login/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo', token=token)
    user_info = resp.json()
    print(user_info)
    user = oauth.google.userinfo()  # uses openid endpoint to fetch user info
    print(help(oauth.google.userinfo))
    print(user)
    session['profile'] = user_info
    session.permanent = True
    return redirect(url_for('.home'))


@authorization.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect(url_for('.home'))


@authorization.route('/home')
def home():
    return 'Well... hi!'
