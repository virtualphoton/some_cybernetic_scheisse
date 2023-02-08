from .models import db, UserRole, Group, Camera, User, Command, Machine, MachineSpec
from .factories import (
    list_command_factory,
    add_new_factory,
    delete_factory,
    add_revoke,
    add_revoke_resource_commands
)
from .utils import find_by_id, get_resource_table, pass_resource, test_role

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
