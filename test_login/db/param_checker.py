import typing as tp
from dataclasses import dataclass, field

__all__ = ["check_command"]

@dataclass
class Params:
    needed: set[str] = field(default_factory=set)
    optional: set[str] = field(default_factory=set)

simple_list_params = Params({"target_id"})
resource_list_params = Params({"resource_type", "target_id"})
no_params = Params()
simple_delete_params = Params({"delete_id"})


def check_params(needed_params: Params, params: dict[str, tp.Any], add_user_id=True):
    params_given = set(params)
    needed = needed_params.needed | ({"user_id"} if add_user_id else set())
    possible_params = needed | needed_params.optional
    if not params_given.issubset(possible_params):
        raise RuntimeError(f"Excessive: {params_given - possible_params}")
    if not params_given.issuperset(needed):
        raise RuntimeError(f"Lacking: {needed - params_given}")


def check_add_resource_params(params: dict[str, tp.Any]):
    params_given = set(params)
    needed_params = {"user_id", "name", "resource_type"}
    if not needed_params.issubset(params_given):
        raise RuntimeError(f"Need to provide this params: {needed_params - params_given}")
    if params["resource_type"] == "camera":
        needed_params |= {"connection", "address"}
        optional_params = {"res_x", "res_y"}
    elif params["resource_type"] == "machine":
        needed_params |= {"url", "js_path", "aruco_id"}
        optional_params = set()
    check_params(Params(needed_params, optional_params), params)


def check_add_user_params(params):
    check_params(Params({"secret_key", "role", "username"}), params, False)


PARAMETERS = {
    "add_resource": check_add_resource_params,
    "list_resources": Params({"resource_type"}),
    "delete_resource": Params({"resource_type", "delete_id"}),
    "give_resource": Params({"target_user_id", "resource_type", "resource_id"}),
    "list_user_resources": resource_list_params,
    "revoke_resource": Params({"target_user_id", "resource_type", "resource_id"}),
    
    "add_command": Params({"machine", "name"}),
    "list_commands": simple_list_params,
    "delete_command": simple_delete_params,
    
    "add_user": check_add_user_params,
    "delete_user_account": simple_delete_params,
    "delete_my_account": no_params,
    "list_usernames": no_params,
    "user_id_from_username": Params({"username"}),
    "get_my_username": no_params,
    "list_users": no_params,
    
    "add_spec": Params({"name", "machine", "commands"}),
    "list_specs": simple_list_params,
    "delete_spec": simple_delete_params,
    "add_command_to_spec": Params({"spec_id", "command_id"}),
    "list_spec_commands": simple_list_params,
    "delete_command_from_spec": Params({"spec_id", "command_id"}),
    
    "create_group": Params({"name", "cameras", "machine_specs"}),
    "list_groups": no_params,
    "delete_group": simple_delete_params,
    "add_resource_to_group": Params({"group_id", "resource_type", "resource_id"}),
    "list_group_resources": Params({"group_id", "resource_type"}),
    "delete_resource_from_group": Params({"group_id", "resource_type", "resource_id"}),
    "add_to_group": Params({"group_id", "target_user_id"}),
    "list_group_members": simple_list_params,
    "delete_from_group": Params({"group_id", "target_user_id"}),
    "list_groups_i_am_in": no_params,
    "leave_group": Params({"group_id"}),
    "get_group": Params({"group_id"}),
}

def check_command(command: str, params: dict[str, tp.Any]):
    checker = PARAMETERS[command]
    if isinstance(checker, Params):
        check_params(checker, params)
    else:
        checker(params)
