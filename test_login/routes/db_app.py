from flask import Blueprint, abort, current_app, request
from sqlalchemy.exc import IntegrityError

from .auth_utils import login_required
from ..db.commands import API_COMMANDS
from ..db.param_checker import check_command
from ..db.serialization import serialize
from ..extensions import db
from ..db.private_api import email_to_id

db_api = Blueprint('db_api', __name__)

@db_api.route('/db_api/<string:method>', methods=['POST']) 
@login_required
def call_api(method: str, decoded_jwt: dict[str, str]):
    try:
        if method not in API_COMMANDS:
            raise RuntimeError(f'No such method exists: {method}')
        
        params = request.get_json()
        params['user_id'] = email_to_id(decoded_jwt['email'])
        print(params)
        check_command(method, params)
        
        # in case any changes were made
        db.session.rollback()
        res = API_COMMANDS[method](**params)
        
    except (RuntimeError, IntegrityError) as e:
        print(e.args[0])
        return abort(400, e.args[0])
    serialized = serialize(res)
    print(f'{serialized=}')
    return serialized


@db_api.teardown_request
def teardown_request(exception):
    with current_app.app_context():
        if exception:
            db.session.rollback()
        db.session.remove()
