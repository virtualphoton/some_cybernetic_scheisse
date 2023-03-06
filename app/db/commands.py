from ..extensions import db
from .models import UserRole, Group, Camera, User, Command, Machine
from .factories import (
    list_command_factory,
    add_new_factory,
    delete_factory,
)
from .utils import find_by_id, get_resource_table, pass_resource, test_role


@pass_resource
def list_resources(user_id, table):
    # print(table)
    return list_command_factory(UserRole.user, table, return_all=True)(user_id=user_id)

def list_user_resources(user_id, resource_type, target_id):
    get_resource_table(resource_type)
    list_field_name = "cameras" if resource_type == "camera" else "machines"
    return list_command_factory(UserRole.admin, User, list_field_name)(user_id=user_id, target_id=target_id)

def list_groups_i_am_in(user_id):
    return find_by_id(User, user_id).groups_member

@test_role(UserRole.admin)
@pass_resource
def add_resource(table, **params):
    obj = table(**params)
    db.session.add(obj)
    db.session.commit()

@test_role(UserRole.user)
def delete_self_from_group(user_id, group_id):
    group = find_by_id(Group, group_id)
    user = find_by_id(User, user_id)
    if user not in group.users:
        raise RuntimeError(f"Element {user} not present in list!")
    group.users.remove(user)
    db.session.commit()

@pass_resource
def delete_resource(user_id, table, delete_id):
    return delete_factory(UserRole.admin, table)(user_id=user_id, delete_id=delete_id)

@test_role(UserRole.user)
def get_group(group_id):
    return find_by_id(Group, group_id)

@test_role(UserRole.user)
@pass_resource
def get_resources(table, res_ids):
    return find_by_id(table, res_ids)
    

@test_role(UserRole.admin, pass_id=True)
def modify_group(user_id, group_id, **params):
    from_ids = {"machines": Machine, "cameras": Camera, "users": User}
    if group_id is None:
        group = add_new_factory(UserRole.admin, Group, from_ids)\
                    (user_id=user_id, **params)
        
    else:
        group = find_by_id(Group, group_id)
        for field, new_val in params.items():
            if field in from_ids:
                new_val = find_by_id(from_ids[field], new_val)
            setattr(group, field, new_val)
    db.session.commit()
    return group

def list_groups(user_id, **kwargs):
    if (find_by_id(User, user_id).role is UserRole.admin):
        return list_command_factory(UserRole.admin, Group, return_all=True)(user_id=user_id, **kwargs)
    else:
        return list_groups_i_am_in(user_id=user_id, **kwargs)

API_COMMANDS = {
    "add_command": add_new_factory(UserRole.admin, Command, {"machine": Machine}),
    "list_commands": list_command_factory(UserRole.user, Machine, "commands"),
    "delete_command": delete_factory(UserRole.admin, Command),
    
    "add_resource": add_resource,
    "list_resources": list_resources,
    "get_resources": get_resources,
    "delete_resource": delete_resource,
    
    "list_users": list_command_factory(UserRole.admin, User, return_all=True),
    "get_my_user": lambda user_id: find_by_id(User, user_id),
    "delete_user_account": delete_factory(UserRole.admin, User),
    
    "list_groups": list_groups,
    "get_group": get_group,
    "modify_group": modify_group,
    "delete_group": delete_factory(UserRole.admin, Group),
    "leave_group": (lambda user_id, group_id: delete_self_from_group(user_id=user_id, group_id=group_id, target_user_id=user_id)),
    
}
