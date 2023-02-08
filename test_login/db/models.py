import enum

from .constants import MAX_NAME_LENGTH, MAX_ARUCO_ID
from ..extensions import db

class UserRole(enum.Enum):
    user = "user"
    admin = "admin"

class CameraConnection(enum.Enum):
    usb = "usb"
    url = "url"

def ManyToMany(table_first: str, table_second: str, backref: str):
    table = db.Table(f"{table_first}_{table_second}".lower(),
        db.Column(f"{table_first}_id", db.Integer, db.ForeignKey(f"{table_first.lower()}.id")),
        db.Column(f"{table_second}_id", db.Integer, db.ForeignKey(f"{table_second.lower()}.id")),
    )
    return db.relationship(table_second, secondary=table, backref=backref)

class Machine(db.Model):
    __tablename__ = "machine"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(MAX_NAME_LENGTH), nullable=False)
    
    url = db.Column(db.Text, nullable=False)
    js_path = db.Column(db.Text, nullable=False)
    aruco_id = db.Column(db.Integer,
                         db.CheckConstraint(f"aruco_id > 0 and aruco_id < {MAX_ARUCO_ID}"),
                         nullable=False, unique=True)
        
    commands = db.relationship("Command", backref="machine", cascade="all, delete-orphan")

class Command(db.Model):
    __tablename__ = "command"
    id = db.Column(db.Integer, primary_key=True)
    machine_id = db.Column(db.Integer, db.ForeignKey("machine.id"))
    name = db.Column(db.String(MAX_NAME_LENGTH), nullable=False)

class Camera(db.Model):
    __tablename__ = "camera"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(MAX_NAME_LENGTH), nullable=False)
    
    connection = db.Column(db.Enum(CameraConnection), nullable=False)
    address = db.Column(db.Text, nullable=False)
    res_x = db.Column(db.Integer, db.CheckConstraint("res_x > 0"))
    res_y = db.Column(db.Integer, db.CheckConstraint("res_x > 0"))

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    
    username = db.Column(db.String(MAX_NAME_LENGTH), nullable=False, unique=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    role = db.Column(db.Enum(UserRole), nullable=False)

class Group(db.Model):
    __tablename__ = "group"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(MAX_NAME_LENGTH), nullable=False)
    description = db.Column(db.Text)
    
    cameras = ManyToMany("Group", "Camera", "groups")
    machines = ManyToMany("Group", "Machine", "groups")
    users = ManyToMany("Group", "User", "groups_member")
