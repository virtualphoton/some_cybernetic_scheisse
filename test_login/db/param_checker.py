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

def check_command(command: str, params: dict[str, tp.Any]):
    checker = PARAMETERS[command]
    if isinstance(checker, Params):
        check_params(checker, params)
    else:
        checker(params)

PARAMETERS = {
    "add_resource": check_add_resource_params,
    "list_resources": Params({"resource_type"}),
    "delete_resource": Params({"resource_type", "delete_id"}),
    "get_resources": Params({"resource_type", "res_ids"}),
    
    "add_command": Params({"machine", "name"}),
    "list_commands": simple_list_params,
    "delete_command": simple_delete_params,

    "delete_user_account": simple_delete_params,
    "delete_my_account": no_params,
    "get_my_username": no_params,
    "list_users": no_params,
    
    "list_groups": no_params,
    "get_group": Params({"group_id"}),
    "modify_group": Params({"group_id", "name", "description", "cameras", "machines", "users"}),
    "delete_group": simple_delete_params,
    "list_groups_i_am_in": no_params,
    "leave_group": Params({"group_id"}),
}
