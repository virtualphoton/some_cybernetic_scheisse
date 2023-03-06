from ..extensions import db
from .factories import add_new_factory
from .models import User

def add_user(role: str, username: str, email: str):
    if role == "admin" and User.query.filter_by(role="admin").count():
        raise RuntimeError("More than 1 admins")
    add_new_factory(None, User)(user_id=None, role=role, username=username, email=email)

def email_to_id(email: str) -> int | None:
    query = User.query.filter_by(email=email)
    if not query.count():
        return None
    return query.first().id

def set_role(email: str, new_role: str):
    User.query.filter_by(email=email).first().role = new_role
    db.session.commit()

def get_role(email: str):
    return User.query.filter_by(email=email).first().role.value
