from functools import wraps

from .models import Camera, Machine, MachineSpec, User, UserRole

OWNER_PATH = {
    "machine": ["holder"],
    "camera": ["holder"],
    "machinespec": ["machine", "holder"],
    "command": ["machine", "holder"],
    "group": ["creator"],
    "user": []
}

ROLES_PRIORITY = {UserRole.guest: 1, UserRole.user: 2, UserRole.admin: 3}


def test_owner(target, owner_id: str | None = None):
    if owner_id is None or find_by_id(User, owner_id).role == UserRole.admin:
        return
    cur_value = target
    for step in OWNER_PATH[target.__tablename__]:
        cur_value = getattr(cur_value, step)
    if cur_value is None:
        raise RuntimeError("Object doesn\'t belong to anyone!")
    if cur_value.id != owner_id:
        raise RuntimeError(f"Wrong owner of {target}!")


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


def get_resource_table(resource_type: str, machinespec_used=True):
    resource_type = resource_type.lower()
    if resource_type == "machinespec" and not machinespec_used or resource_type not in ("camera", "machine", "machinespec"):
        raise RuntimeError(f"Wrong resource type: {resource_type}")
    resource_table = {
        "camera": Camera,
        "machine": Machine,
        "machinespec": MachineSpec
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
