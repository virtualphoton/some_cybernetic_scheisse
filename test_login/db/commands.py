from .models import db, UserRole, Group, Camera, User, Command, Machine, MachineSpec
from .factories import (
    list_command_factory,
    add_new_factory,
    delete_factory,
    add_revoke,
    add_revoke_resource_commands
)
from .utils import find_by_id, get_resource_table, pass_resource, test_role


@pass_resource
def list_resources(user_id, table):
    # print(table)
    return list_command_factory(UserRole.admin, table, return_all=True)(user_id=user_id)

def list_user_resources(user_id, resource_type, target_id):
    get_resource_table(resource_type)
    list_field_name = "cameras" if resource_type == "camera" else "machines"
    return list_command_factory(UserRole.admin, User, list_field_name)(user_id=user_id, target_id=target_id)

def list_usernames(user_id):
    return [user.username for user in list_command_factory(UserRole.user, User, return_all=True)(user_id=user_id)]

def list_groups(user_id):
    return list_command_factory(UserRole.user, User, "groups_created")(user_id=user_id, target_id=user_id)

@test_role(UserRole.user)
@pass_resource
def list_group_resources(table, group_id: int):
    group = find_by_id(Group, group_id)
    if table is Camera:
        return group.cameras
    return group.machines

@test_role(UserRole.user)
def list_group_members(target_id):
    return find_by_id(Group, target_id).users

def list_groups_i_am_in(user_id):
    return find_by_id(User, user_id).groups_member

@test_role(UserRole.admin)
def user_id_from_username(username):
    query = User.query.filter_by(username=username)
    if not query.count():
        raise RuntimeError(f"Couldn\'t find {username} in users")
    return query.first().id


@test_role(UserRole.admin)
@pass_resource
def add_resource(table, **params):
    obj = table(**params)
    db.session.add(obj)
    db.session.commit()

def machine_spec_in_group_test(group: Group, resource: MachineSpec | Camera):
    if resource.__tablename__ == "machinespec":
        for machinespec in group.machine_specs:
            if machinespec.machine.id == resource.machine.id:
                break
        else:
            return
        group.machine_specs.remove(machinespec)
    return True

give_resource, revoke_resource = add_revoke_resource_commands(
    User, {
        "machine": "machines",
        "camera": "cameras"
    },
    "target_user_id"
)
add_resource_to_group, delete_resource_from_group = add_revoke_resource_commands(
    Group, {
        "machinespec": "specs",
        "camera": "cameras"
    },
    "group_id", test=machine_spec_in_group_test
)

add_command_to_spec, delete_command_from_spec = add_revoke(UserRole.user, MachineSpec, Command,
                                                           "spec_id", "command_id", "commands",
                                                           test=(lambda spec, command: spec.machine.id == command.machine.id))
add_to_group, delete_from_group = add_revoke(UserRole.user, Group, User,
                                             "group_id", "target_user_id", "users")
_, delete_self_from_group = add_revoke(UserRole.user, Group, User,
                                             "group_id", "target_user_id", "users", to_test_owner=False)

def create_group(user_id, **params):
    creator = find_by_id(User, user_id)
    add_new_factory(UserRole.user, Group, [("machine_specs", MachineSpec), ("cameras", Camera)])\
        (user_id=user_id, creator=creator, **params)

@pass_resource
def delete_resource(user_id, table, delete_id):
    return delete_factory(UserRole.admin, table)(user_id=user_id, delete_id=delete_id)

@test_role(UserRole.admin, pass_id=False)
def get_group(group_id):
    return find_by_id(Group, group_id)

API_COMMANDS = {
    "list_resources": list_resources,
    "list_user_resources": list_user_resources,
    "list_usernames": list_usernames,
    "list_users": list_command_factory(UserRole.admin, User, return_all=True),
    "list_commands": list_command_factory(UserRole.user, Machine, "commands"),
    "list_specs": list_command_factory(UserRole.user, Machine, "specs"),
    "list_spec_commands": list_command_factory(UserRole.user, MachineSpec, "commands"),
    "list_groups": list_groups,
    "list_group_resources": list_group_resources,
    "list_group_members": list_group_members,
    "list_groups_i_am_in": list_groups_i_am_in,
    "user_id_from_username": user_id_from_username,
    "get_my_username": lambda user_id: find_by_id(User, user_id).username,
    
    "add_resource": add_resource,
    "add_command": add_new_factory(UserRole.admin, Command, [("machine", Machine)]),
    "give_resource": give_resource,
    "add_spec": add_new_factory(UserRole.user, MachineSpec, [("machine", Machine), ("commands", Command)]),
    "add_command_to_spec": add_command_to_spec,
    "add_resource_to_group": add_resource_to_group,
    "create_group": create_group,
    "add_to_group": add_to_group,
    "get_group": get_group,
    
    "delete_resource": delete_resource,
    "delete_command": delete_factory(UserRole.admin, Command),
    "delete_user_account": delete_factory(UserRole.admin, User),
    "revoke_resource": revoke_resource,
    "delete_spec": delete_factory(UserRole.user, MachineSpec),
    "delete_command_from_spec": delete_command_from_spec,
    "delete_resource_from_group": delete_resource_from_group,
    "delete_from_group": delete_from_group,
    "delete_group": delete_factory(UserRole.user, Group),
    "leave_group": (lambda user_id, group_id: delete_self_from_group(user_id=user_id, group_id=group_id, target_user_id=user_id)),
    "delete_my_account": lambda user_id: delete_factory(UserRole.guest, User)(user_id=user_id, delete_id=user_id)
}
