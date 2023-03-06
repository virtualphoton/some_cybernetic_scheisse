from flask import Blueprint, request, abort
from .auth_utils import login_required
from ..db.private_api import email_to_id
from ..db.commands import get_group
from ..db.serialization import serialize

machines = Blueprint("machines", __name__)

class MachineBase:
    def run(self, command, args):
        raise NotImplemented

def get_machine(machine_id):
    return dummy_machines[machine_id - 1]

@machines.route("/machine_commands", methods=["POST"])
@login_required
def machine_commands(decoded_jwt: dict[str, str]):
    data = request.json
    user_id = email_to_id(decoded_jwt["email"])
    group_ser = serialize(get_group(user_id=user_id, group_id=data["group_id"]))
    if data["machine_id"] not in group_ser["machines"] or user_id not in group_ser["users"]:
        return abort(403, "You can't access that machine!")
    result = get_machine(data["machine_id"]).run(data["command"], data["args"])
    print(result)
    return result



class DummyMachine(MachineBase):
    def __init__(self):
        self.counter = 0
    
    def run(self, command, args):
        if command == "help":
            msg = "ping\nhelp\ninc"
        elif command == "ping":
            msg = "pong"
        elif command == "inc":
            self.counter += int(args[0])
            msg = list(range(self.counter))
        else:
            msg = "Unknown command, type `help` to get list of commands"
        return {"msg": msg}

dummy_machines = [DummyMachine() for _  in range(10)]
