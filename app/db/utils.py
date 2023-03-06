from functools import wraps

from .models import Camera, Machine, User, UserRole

ROLES_PRIORITY = {UserRole.user: 1, UserRole.admin: 2}

def test_role(role: str | None, pass_id = False):
    def decorator(func):
        @wraps(func)
        def inner(*, user_id, **kwargs):
            if role is not None:
                user = find_by_id(User, user_id)
                if ROLES_PRIORITY[user.role] < ROLES_PRIORITY[role]:
                    raise RuntimeError(
                        f"Permission denied: user role - {user.role}, needed role - {role}")
            return func(**kwargs) if not pass_id else func(user_id=user_id, **kwargs)
        return inner
    return decorator


def get_resource_table(resource_type: str):
    resource_type = resource_type.lower()
    if resource_type not in ("camera", "machine"):
        raise RuntimeError(f"Wrong resource type: {resource_type}")
    resource_table = {
        "camera": Camera,
        "machine": Machine,
    }[resource_type]
    
    return resource_table


def pass_resource(func):
    @wraps(func)
    def inner(*, resource_type, **kwargs):
        table = get_resource_table(resource_type)
        return func(**kwargs, table=table)
    return inner


def find_by_id(table, id):
    if isinstance(id, list):
        return table.query.filter(table.id.in_(id)).all()
    query = table.query.get(id)
    if not query:
        raise RuntimeError(f"Couldn\'t find {id} in table `{table.__tablename__}`")
    return query
