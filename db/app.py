import enum
import typing as tp
from dataclasses import dataclass
from functools import wraps

from flask_sqlalchemy import SQLAlchemy
from flask import Flask

MAX_NAME_LENGTH = 40
USER_ID_MAX_LENGTH = 50
MAX_ARUCO_ID = 1000

app = Flask(__name__)
app.secret_key = b'sth'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_db.sqlite3'
app.config['SQLAPLCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
db.init_app(app)

class UserRole(enum.Enum):
    user = "user"
    admin = "admin"
    guest = "guest"
ROLES_PRIORITY = {'guest': 1, 'user': 2, 'admin': 3}


class CameraConnection(enum.Enum):
    usb = "usb"
    url = "url"

def ForeignKeyId(table: str):
    return db.Column(db.Integer, db.ForeignKey(f'{table}.id'))

def ManyToMany(table_first: str, table_second: str, backref: str):
    table = db.Table(f'{table_first}_{table_second}'.lower(),
        db.Column(f'{table_first}_id', db.Integer, db.ForeignKey(f'{table_first.lower()}.id')),
        db.Column(f'{table_second}_id', db.Integer, db.ForeignKey(f'{table_second.lower()}.id')),
    )
    return db.relationship(table_second, secondary=table, backref=backref)

class Machine(db.Model):
    __tablename__ = 'machine'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(MAX_NAME_LENGTH), nullable=False)
    
    url = db.Column(db.Text, nullable=False)
    js_path = db.Column(db.Text, nullable=False)
    aruco_id = db.Column(db.Integer,
                         db.CheckConstrain(f'aruco_id > 0 and aruco_id < {MAX_ARUCO_ID}'))
                         
    specs = db.relationship('MachineSpec', 'machine')
    commands = db.relationship('Command', 'machine')
    
class MachineSpec(db.Model):
    __tablename__ = 'machinespec'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(MAX_NAME_LENGTH), nullable=False)
    
    commands = ManyToMany('MachineSpec', 'Command', 'spec')

class Command(db.Model):
    __tablename__ = 'command'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(MAX_NAME_LENGTH), nullable=False)

class Camera(db.Model):
    __tablename__ = 'camera'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(MAX_NAME_LENGTH), nullable=False)
    
    connection = db.Column(db.Enum(CameraConnection), nullable=False)
    address = db.Column(db.Text, nullable=False)
    res_x = db.Column(db.Integer, db.CheckConstrain('res_x > 0'))
    res_y = db.Column(db.Integer, db.CheckConstrain('res_x > 0'))

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(USER_ID_MAX_LENGTH), primary_key=True)
    username = db.Column(db.String(MAX_NAME_LENGTH), nullable=False)
    
    role = db.Column(db.Enum(UserRole))
    
    cameras = db.relationship('Camera', 'holder')
    machines = db.relationship('Machine', 'holder')
    groups_created = db.relationship('Group', 'creator')

class Group(db.Model):
    __tablename__ = 'group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(MAX_NAME_LENGTH), nullable=False)
    
    cameras = ManyToMany('Group', 'Camera', 'groups')
    machine_specs = ManyToMany('Group', 'MachineSpec', 'groups')
    users = ManyToMany('Group', 'user', 'groups_member')

OWNER_PATH = {
    'machine': ['holder'],
    'camera': ['holder'],
    'machinespec': ['machine', 'holder'],
    'command': ['machine', 'holder'],
    'group': ['creator'],
}

def test_owner(target, owner_id: str | None = None):
    if owner_id is None or find_by_id(User, owner_id).role == UserRole.admin:
        return
    cur_value = target
    for step in OWNER_PATH[target.__tablename__]:
        cur_value = getattr(cur_value, step)
    if cur_value.id != owner_id:
        raise RuntimeError(f'Wrong owner of {target}, needed {owner_id}!')

def test_role(role: str, pass_id = False):
    def decorator(func):
        @wraps(func)
        def inner(*, user_id, **kwargs):
            user = find_by_id(User, user_id)
            if ROLES_PRIORITY[user.role] < ROLES_PRIORITY[role]:
                raise RuntimeError(
                    f'Permission denied: user role - {user.role}, needed role - {role}')
            return func(**kwargs) if not pass_id else func(user_id=user_id, **kwargs)
        return inner
    return decorator

def pass_resource(func):
    @wraps(func)
    def inner(*, resource_type, **kwargs):
        table = get_resource_table(resource_type)
        return func(**kwargs, table=table)
    return inner


def find_by_id(table, id):
    try:
        iter(id)
    except AttributeError:
        query = table.query.filter_by(id=id)
        if not query.count():
            raise RuntimeError(f'Couldn\'t find {id} in {table}')
        return query.first()
    else:
        return table.query.filter(table.id.in_(id))


def list_command_fabric(user_role, table, list_field: str | None = None, return_all=False):
    @test_role(user_role, pass_id=True)
    def inner(user_id, target_id = None):
        if not return_all:
            target = find_by_id(table, target_id)
            test_owner(target, user_id)
            return getattr(find_by_id(table, target_id), list_field)
        else:
            return table.all()
    
    return inner


def get_resource_table(resource_type: str, machinespec_used=True):
    resource_type = resource_type.lower()
    if resource_type == 'machinespec' and not machinespec_used or resource_type not in ('camera', 'machine', 'machinespec'):
        raise RuntimeError(f'Wrong resource type: {resource_type}')
    resource_table = {
        'camera': Camera,
        'machine': Machine,
        'machinespec': MachineSpec
    }[resource_type]
    
    return resource_table

@pass_resource
def list_resources(user_id, table):
    return list_command_fabric(UserRole.admin, table, return_all=True)(user_id)

def list_user_resources(user_id, resource_type, target_id):
    get_resource_table(resource_type)
    list_field_name = 'cameras' if resource_type == 'camera' else 'machines'
    return list_command_fabric(UserRole.admin, User, list_field_name)(user_id, target_id)

def list_usernames(user_id):
    return [user.username for user in list_command_fabric(UserRole.user, User, return_all=True)(user_id)]

def list_groups(user_id):
    return list_command_fabric(UserRole.user, User, 'groups_created')(user_id, user_id)

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
        raise RuntimeError(f'Couldn\'t find {username} in users')
    return query.first()

@dataclass
class Params:
    needed: set[str] = set()
    optional: set[str] = set()

simple_list_params = Params({'target_id'})
resource_list_params = Params({'resource_type', 'target_id'})
no_params = Params()

get_commands = {
    'list_resources': list_resources,
    'list_user_resources': list_user_resources,
    'list_usernames': list_usernames,
    'list_commands': list_command_fabric(UserRole.user, Machine, 'machine_id'),
    'list_specs': list_command_fabric(UserRole.user, MachineSpec, 'machine_id'),
    'list_spec_commands': list_command_fabric(UserRole.user, Command, 'spec_id'),
    'list_groups': list_groups,
    'list_group_resources': list_group_resources,
    'list_group_members': list_group_members,
    'list_groups_i_am_in': list_groups_i_am_in,
    'user_id_from_username': user_id_from_username,
    'get_my_username': lambda user_id: user_id_from_username(user_id, user_id),
}

def add_new_fabric(user_role: str, table, from_ids):
    """
    ids_translate: list of tuples (field, table)
    """
    
    @test_role(user_role, pass_id=True)
    def inner(user_id, **params):
        for name, from_table in from_ids:
            objects = find_by_id(from_table, params[name])
            if isinstance(params[name], list):
                for obj in objects:
                    test_owner(obj, user_id)
            else:
                test_owner(objects, user_id)
        obj = table(**params)
        db.session.add(obj)
        db.session.commit()
        return obj
    return inner

@pass_resource
def add_resource(table, **params):
    obj = table(**params)
    db.session.add(obj)
    db.session.commit()

def change_list_factory(user_role, table, item_table, id_name, item_id_name, list_field_name, action, test=None):
    @test_role(user_role, pass_id=True)
    def inner(user_id, **kwargs):
        target = find_by_id(table, kwargs[id_name])
        test_owner(target, user_id)
        item = find_by_id(item_table, kwargs[item_id_name])
        if test is not None:
            if not test(target, item):
                raise RuntimeError(f'Integrity error: tried to add {item} to {target}')
        list_field = getattr(target, list_field_name)
        if action == 'append':
            list_field.append(item)
        elif action == 'remove':
            list_field.remove(item)
        db.session.commit()
    return inner

def add_revoke(args, test=None):
    return [change_list_factory(*args, action, test=test) for action in ('append', 'remove')]

def add_revoke_resource_commands(target_table, field_names, target_id_name, test=None):
    def inner(action):
        @pass_resource
        def resource_action(table, **kwargs):
            find_by_id(Group, kwargs[target_id_name])
            list_field_name = field_names[table.__tablename__]
            change_list_factory(
                UserRole.admin, target_table, table,
                target_id_name, 'resource_id', list_field_name,
                action, test=test
            )(**kwargs)
        return resource_action
    return [inner('append'), inner('remove')]

def machine_spec_in_group_test(group: Group, resource: MachineSpec | Camera):
    if resource.__tablename__ == 'machinespec':
        for machinespec in group.machine_specs:
            if machinespec.machine.id == resource.machine.id:
                break
        else:
            return
        group.machine_specs.remove(machinespec)
    return True

give_resource, revoke_resource = add_revoke_resource_commands(
    User, {
        'machine': 'machines',
        'camera': 'cameras'
    },
    'target_user_id'
)
add_resource_to_group, delete_resource_from_group = add_revoke_resource_commands(
    Group, {
        'machinespec': 'specs',
        'camera': 'cameras'
    },
    'group_id', test=machine_spec_in_group_test
)

add_command_to_spec, delete_command_from_spec = add_revoke(UserRole.user, MachineSpec, Command,
                                                           'spec_id', 'command_id', 'commands',
                                                           test=lambda spec, command: spec.machine.id == command.machine.id)
add_to_group, delete_from_group = add_revoke(UserRole.user, Group, User,
                                             'group_id', 'target_user_id', 'members')

def create_group(user_id, **params):
    holder = find_by_id(User, user_id)
    add_new_fabric(UserRole.user, MachineSpec, [('machine_specs', MachineSpec), ('cameras', Camera)])\
        (user_id=user_id, holder=holder, **params)

simple_delete_params = Params({'delete_id'})

def check_params(needed_params: Params, params: dict[str, tp.Any]):
    params_given = set(params)
    needed = needed_params.needed | {'user_id'}
    possible_params = needed + needed_params.optional
    if not params_given.issubset(possible_params):
        raise RuntimeError(f'Excessive: {params_given - possible_params}')
    if not params_given.issuperset(needed):
        raise RuntimeError(f'Lacking: {needed - params_given}')

def check_add_resource_params(params: dict[str, tp.Any]):
    params_given = set(params)
    needed_params = {'user_id', 'name', 'resource_type'}
    if not needed_params.issubset(params_given):
        raise RuntimeError(f'Need to provide this params: {needed_params - params_given}')
    if params['resource_type'] == 'camera':
        needed_params |= {'connection', 'address'}
        optional_params = {'res_x', 'res_y'}
    elif params['resource_type'] == 'machine':
        needed_params |= {'url', 'js_path', 'aruco_id'}
        optional_params = {}
    check_params(Params(needed_params, optional_params), params)

def check_command(command: str, checker: Params | tp.Callable[[dict[str, tp.Any]], None]):
    needed_params = parameters[command]
    if isinstance(needed_params, Params):
        check_params(needed_params, checker)
    else:
        checker(command)

parameters = {
    'add_resource': check_add_resource_params,
    'list_resources': Params({'resource_type'}),
    'delete_resource': Params({'resource_type', 'delete_id'}),
    'give_resource': Params({'target_user_id', 'resource_type', 'resource_id'}),
    'list_user_resources': resource_list_params,
    'revoke_resource': Params({'target_user_id', 'resource_type', 'resource_id'}),
    
    'add_command': Params({'machine_id', 'command_name'}),
    'list_commands': simple_list_params,
    'delete_command': simple_delete_params,
    
    'delete_user_account': simple_delete_params,
    'delete_my_account': no_params,
    'list_usernames': no_params,
    'user_id_from_username': Params(names={'username'}),
    'get_my_username': no_params,
    
    'add_spec': Params({'machine_id', 'commands'}),
    'list_specs': simple_list_params,
    'delete_spec': simple_delete_params,
    'add_command_to_spec': Params({'spec_id', 'command_id'}),
    'list_spec_commands': simple_list_params,
    'delete_command_from_spec': Params({'spec_id', 'command_id'}),
    
    'create_group': Params({'cameras', 'machine_specs'}),
    'list_groups': no_params,
    'delete_group': simple_delete_params,
    'add_resource_to_group': Params({'group_id', 'resource_type', 'resource_id'}),
    'list_group_resources': Params({'group_id', 'resource_type'}),
    'delete_resource_from_group': Params({'group_id', 'resource_type', 'resource_id'}),
    'add_to_group': Params({'group_id', 'target_user_id'}),
    'list_group_members': simple_list_params,
    'delete_from_group': Params({'group_id', 'target_user_id'}),
    'list_groups_i_am_in': no_params,
    'leave_group': Params({'group_id'}),
}

post_commands = {
    'add_resource': add_resource,
    'add_command': add_new_fabric(UserRole.admin, Command, [('machine_id', Machine)]),
    'give_resource': give_resource,
    
    'add_spec': add_new_fabric(UserRole.user, MachineSpec,[('machine_id', Machine), ('commands', Command)]),
    'add_command_to_spec': add_command_to_spec,
    'add_resource_to_group': add_resource_to_group,
    'create_group': create_group,
    'add_to_group': add_to_group,
}

def delete_fabric(user_role, table):
    @test_role(user_role, pass_id=True)
    def inner(user_id, delete_id):
        to_del = find_by_id(table, delete_id)
        test_owner(to_del, user_id)
        db.session.delete(to_del)
        db.session.commit()
    return inner

@pass_resource
def delete_resource(table, delete_id):
    return delete_fabric(UserRole.admin, table)(delete_id)

delete_commands = {
    'delete_resource': delete_resource,
    'delete_command': delete_fabric(UserRole.admin, Command),
    'delete_user_account': delete_fabric(UserRole.admin, User),
    'revoke_resource': revoke_resource,
    'delete_spec': delete_fabric(UserRole.user, MachineSpec),
    'delete_command_from_spec': delete_command_from_spec,
    'delete_resource_from_group': delete_resource_from_group,
    'delete_from_group': delete_from_group,
    'delete_group': delete_fabric(UserRole.user, Group),
    'leave_group': (lambda user_id, group_id: delete_from_group(user_id=user_id, group_id=group_id, target_user_id=user_id)),
    'delete_my_account': lambda user_id: delete_fabric(UserRole.guest, User)(user_id=user_id, delete_id=user_id)
}


with app.app_context(): ...

