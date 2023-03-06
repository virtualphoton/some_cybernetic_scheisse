import json
from pathlib import Path
import requests

import google
from dotenv import dotenv_values
from flask import Blueprint, Response
from flask.globals import request, session
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from werkzeug.utils import redirect

from .auth_utils import generate_JWT, login_required
from ..db.private_api import add_user, email_to_id, set_role, get_role


auth = Blueprint('auth', __name__)

env_vars = dotenv_values(Path(__file__).parent.parent / ".env" )
BACKEND_URL = env_vars["BACKEND_URL"]
GOOGLE_CLIENT_ID = env_vars["GOOGLE_CLIENT_ID"]
FRONTEND_URL = env_vars["FRONTEND_URL"]
CLIENT_SECRETS_FILE = Path(__file__).parent.parent / "client-secret.json"

flow = Flow.from_client_secrets_file(
    client_secrets_file=CLIENT_SECRETS_FILE,
    scopes=[
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
        "openid",
    ],
    redirect_uri=f"{BACKEND_URL}/auth/callback",
)

@auth.route("/auth/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials
    request_session = requests.session()
    token_request = google.auth.transport.requests.Request(session=request_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token, request=token_request,
        audience=GOOGLE_CLIENT_ID
    )
    session["google_id"] = id_info.get("sub")
    
    # removing the specific audience, as it is throwing error
    del id_info["aud"]
    
    print(*[f'{var} - {id_info.get(var)},' for var in ["name", "email", "picture"]])
    email = id_info["email"]
    if email_to_id(email) is None:
        add_user(role="user", username=id_info["name"], email=email)
    
    role = get_role(email)
    jwt_to_send = generate_JWT(id_info | {"role" : role})
    return redirect(f"{FRONTEND_URL}?jwt={jwt_to_send}&role={role}")


@auth.route("/auth/google")
def login():
    authorization_url, _ = flow.authorization_url()
    return Response(
        response=json.dumps({"auth_url" : authorization_url}),
        status=200,
        mimetype="application/json"
    )


@auth.route("/auth/logout")
def logout():
    # clear the local storage from frontend
    session.clear()
    return Response(
        response=json.dumps({"message" : "Logged out"}),
        status=202,
        mimetype="application/json"
    )


@auth.route("/home")
@login_required
def home_page_user(decoded_jwt):
    print(decoded_jwt)
    return Response(
        response=json.dumps(decoded_jwt),
        status=200,
        mimetype="application/json"
    )
