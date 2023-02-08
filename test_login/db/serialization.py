from dataclasses import dataclass, field

from flask import jsonify

@dataclass
class Serializer:
    simple_columns: list[str] = field(default_factory=list)
    many_columns: list[str] = field(default_factory=list)
    enum_columns: list[str] = field(default_factory=list)

SERIALIZATION_FIELDS = {
    "machine": Serializer(["id", "name", "url", "js_path", "aruco_id"], ["commands"]),
    "command": Serializer(["id", "name", "machine_id"]),
    "camera": Serializer(["id", "name", "address", "res_x", "res_y"], ["groups"], ["connection"]),
    "user": Serializer(["id", "username", "email"], ["cameras", "machines", "groups_member"], ["role"]),
    "group": Serializer(["id", "name"], ["cameras", "machines", "users"]),
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
