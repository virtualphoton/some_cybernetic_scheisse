from ..extensions import db
from .utils import find_by_id, test_role

def list_command_factory(user_role, table, list_field: str | None = None, return_all=False):
    @test_role(user_role, pass_id=False)
    def inner(target_id = None):
        if not return_all:
            return getattr(find_by_id(table, target_id), list_field)
        else:
            return table.query.all()
    
    return inner


def add_new_factory(user_role: str, table, from_ids = None):
    """
    ids_translate: list of tuples (field, table)
    """
    if from_ids is None:
        from_ids = {}
        
    @test_role(user_role, pass_id=False)
    def inner(**params):
        for name, from_table in from_ids.items():
            # print(name, from_table)
            objects = find_by_id(from_table, params[name])
            params[name] = objects
        obj = table(**params)
        db.session.add(obj)
        db.session.commit()
        return obj
        
    return inner


def delete_factory(user_role, table):
    @test_role(user_role, pass_id=False)
    def inner(delete_id):
        to_del = find_by_id(table, delete_id)
        db.session.delete(to_del)
        db.session.commit()
    return inner
