import json
from pathlib import Path
from functools import wraps

import jwt
from dotenv import dotenv_values
from flask import current_app
from flask.globals import request
from flask.wrappers import Response
from werkzeug.exceptions import abort

env_vars = dotenv_values(Path(__file__).parent.parent / ".env" )
ALGORITHM = env_vars["ALGORITHM"]

def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        encoded_jwt = request.headers.get("Authorization").split("Bearer ")[1]
        if encoded_jwt is None:
            return abort(401)
        
        try:
            decoded_jwt = jwt.decode(encoded_jwt, current_app.secret_key, algorithms=[ALGORITHM])
        except Exception as e: 
            return Response(
                response=json.dumps({"message":"Decoding JWT Failed", "exception": e.args}),
                status=401,
                mimetype="application/json"
            )
        
        return func(*args, **kwargs, decoded_jwt=decoded_jwt)
    return inner


def generate_JWT(payload):
    encoded_jwt = jwt.encode(payload, current_app.secret_key, algorithm=ALGORITHM)
    return encoded_jwt
