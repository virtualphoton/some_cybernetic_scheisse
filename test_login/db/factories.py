from .models import db, UserRole
from .utils import find_by_id, pass_resource, test_owner, test_role

def list_command_factory(user_role, table, list_field: str | None = None, return_all=False):
    @test_role(user_role, pass_id=True)
    def inner(user_id, target_id = None):
        if not return_all:
            target = find_by_id(table, target_id)
            test_owner(target, user_id)
            return getattr(find_by_id(table, target_id), list_field)
        else:
            return table.query.all()
    
    return inner


def add_new_factory(user_role: str, table, from_ids = None):
    """
    ids_translate: list of tuples (field, table)
    """
    
    if from_ids is None:
        from_ids = []
    @test_role(user_role, pass_id=True)
    def inner(user_id, **params):
        for name, from_table in from_ids:
            # print(name, from_table)
            objects = find_by_id(from_table, params[name])
            if isinstance(params[name], list):
                for obj in objects:
                    test_owner(obj, user_id)
            else:
                test_owner(objects, user_id)
            params[name] = objects
        obj = table(**params)
        db.session.add(obj)
        db.session.commit()
        return obj
    return inner


def delete_factory(user_role, table):
    @test_role(user_role, pass_id=True)
    def inner(user_id, delete_id):
        to_del = find_by_id(table, delete_id)
        test_owner(to_del, user_id)
        db.session.delete(to_del)
        db.session.commit()
    return inner


def change_list_factory(user_role, table, item_table, id_name, item_id_name, list_field_name, action, test=None, to_test_owner=True):
    @test_role(user_role, pass_id=True)
    def inner(user_id, **kwargs):
        target = find_by_id(table, kwargs[id_name])
        if to_test_owner:
            test_owner(target, user_id)
        item = find_by_id(item_table, kwargs[item_id_name])
        if test is not None:
            if not test(target, item):
                raise RuntimeError(f"Integrity error: tried to add {item} to {target}")
        list_field = getattr(target, list_field_name)
        if action == "append":
            list_field.append(item)
        elif action == "remove":
            if item not in list_field:
                raise RuntimeError(f"Element {item} not present in list!")
            list_field.remove(item)
        db.session.commit()
    return inner


def add_revoke(*args, test=None, to_test_owner=True):
    return [change_list_factory(*args, action, test=test, to_test_owner=to_test_owner) for action in ("append", "remove")]


def add_revoke_resource_commands(target_table, field_names, target_id_name, test=None):
    def inner(action):
        @pass_resource
        def resource_action(table, **kwargs):
            find_by_id(target_table, kwargs[target_id_name])
            list_field_name = field_names[table.__tablename__]
            change_list_factory(
                UserRole.admin, target_table, table,
                target_id_name, "resource_id", list_field_name,
                action, test=test
            )(**kwargs)
        return resource_action
    return [inner("append"), inner("remove")]
