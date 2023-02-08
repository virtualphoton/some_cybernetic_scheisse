from dataclasses import dataclass, field
from enum import Enum

from flask import jsonify

@dataclass
class Serializer:
    simple_columns: list[str] = field(default_factory=list)
    many_columns: list[str] = field(default_factory=list)
    enum_columns: list[str] = field(default_factory=list)

SERIALIZATION_FIELDS = {
    "machine": Serializer(["id", "name", "url", "js_path", "aruco_id", "holder_id"], ["specs", "commands"]),
    "machinespec": Serializer(["id", "name", "machine_id"], ["commands", "groups"]),
    "command": Serializer(["id", "name", "machine_id"], ["specs"]),
    "camera": Serializer(["id", "name", "address", "res_x", "res_y", "holder_id"], ["groups"], ["connection"]),
    "user": Serializer(["id", "username", "email"], ["cameras", "machines", "groups_created", "groups_member"], ["role"]),
    "group": Serializer(["id", "name", "creator_id"], ["cameras", "machine_specs", "users"]),
}

def serialize_table(obj):
    serializer = SERIALIZATION_FIELDS[obj.__tablename__]
    return dict((col, getattr(obj, col)) for col in serializer.simple_columns) | \
            dict((col, [relation.id for relation in getattr(obj, col)]) for col in serializer.many_columns) | \
            dict((col, getattr(obj, col).value) for col in serializer.enum_columns)

def serialize(obj):
    if obj is None:
        return {}
    try:
        jsonify(obj)
        return obj
    except TypeError:
        try:
            iter(obj)
        except TypeError:
            return serialize_table(obj)
        else:
            return list(map(serialize_table, obj))
