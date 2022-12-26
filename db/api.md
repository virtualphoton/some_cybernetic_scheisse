Создание и выдача ресурсов:
- `add_resource(user_id: str, name: str, resource_type: str, params: object), POST, admin` - создать новый ресурс
- - `user_id` - `id` пользователя, отправившего запрос
- - `name` - название, длины не больше 40
- - `resource_type`. Тип ресурса, значения: `"camera", "machine"`
- - `params` - параметры объекта
- - - Для камеры, обязательные параметры - `connection, address`, необязательные - `res_x, res_y`
- - - `connection: str` - из `url`, `usb`
- - - `address: str`
- - - `res_x: int, res_y: int`
- - - Обязательные для машины:
- - - `url: str`
- - - `js_path: str`
- - - `aruco_id: int`, от 0 до 1000

- `list_resources(user_id: str, resource_type: str), GET, admin` - вывести все ресуры данного типа
- - `user_id` - `id` пользователя, отправившего запрос
- - `resource_type`. Тип ресурса, значения: `"camera", "machine"`

- `delete_resource(user_id: str, resource_type: str, delete_id: int), DELETE, admin` - удалить ресурс с данным `id`
- - `user_id` - `id` пользователя, отправившего запрос
- - `resource_type`. Тип ресурса, значения: `"camera", "machine"`
- - `delete_id` - id удаляемого ресурса

- `give_resource(user_id: str, target_user_id: str, resource_type: str, resource_id: int), POST, admin` - выдать полльзователю право пользоваться ресурсом
- - `user_id` - `id` пользователя, отправившего запрос
- - `resource_type`. Тип ресурса, значения: `"camera", "machine"`
- - `target_user_id`
- - `resource_id`

- `list_user_resources(user_id: str, resource_type: str: str, target_id: str), GET, admin` - вывести ресурсы пользователя
- - `user_id` - `id` пользователя, отправившего запрос
- - `resource_type`. Тип ресурса, значения: `"camera", "machine"`
- - `target_id` - id пользователя, чьи ресурсы интересуют

- `revoke_resource(user_id: str, resource_type: str: str, resource_id: int, target_user_id: str), DELETE, admin` - удалить ресурс пользователя
- - `user_id` - `id` пользователя, отправившего запрос
- - `resource_type`. Тип ресурса, значения: `"camera", "machine"`
- - `target_user_id` - id пользователя, чьи ресурсы интересуют
- - `resource_id`


Работа с доступными устройтсву командами:
- `add_command(user_id: str, machine_id: int, command_name: str), POST, admin` - создать команду для машины
- - `user_id` - `id` пользователя, отправившего запрос
- - `machine_id` - машина, к которой привязана команда
- - `command_name`

- `list_commands(user_id: str, target_id: int), GET, user` - найти команды для машины. Пользователь должен владеть запрашиваемой машиной
- - `user_id` - `id` пользователя, отправившего запрос
- - `target_id` - `id` машины

- `delete_command(user_id: str, delete_id: int), DELETE, admin` - удалить команду
- - `user_id` - `id` пользователя, отправившего запрос
- - `delete_id` - `id` удаляемой команды

Работа с аккаунтами и никами:
- `delete_user_account(user_id: str, delete_id: str), DELETE, admin` - удалить человека
- - `user_id` - `id` пользователя, отправившего запрос
- - `delete_id` - `id` удаляемого пользователя

- `list_usernames(user_id: str), GET, user` - вывести ники всех пользователей

- `user_id_from_username(user_id: str, username: str), GET, user` - `id` пользователя с соотв. ником
- - `user_id` - `id` пользователя, отправившего запрос

- `delete_my_account(user_id: str), DELETE, guest` - удалить свой аккаунт


- `get_my_username(user_id: str), GET, user` - получить свой ник


Работа со спецификациями:
- `add_spec(user_id: str, machine_id: int, commands: list[int]), POST, user` - создать спецификацию. Пользователь должен обладать машиной, все команды должны быть для посылаемой машины
- - `user_id` - `id` пользователя, отправившего запрос
- - `machine_id` - машина, к которой привязана спецификация
- - `commands` - список `id` команд для спецификации

- `list_specs(user_id: str, target_id: int), GET, user` - найти спецификации для машины, пользователь должен владеть машиной
- - `user_id` - `id` пользователя, отправившего запрос
- - `target_id` - `id` машины

- `delete_spec(user_id: str, delete_id: int), DELETE, user` - удалить спецификации, пользователь должен владеть машиной
- - `user_id` - `id` пользователя, отправившего запрос
- - `delete_id` - `id` удаляемой спецификации


- `add_command_to_spec(user_id: str, spec_id: int, command_id: int), POST, user` - добавить команду к спецификации, пользователь должен обладать машиной, команды и спецификация должны быть для одной машины
- - `user_id` - `id` пользователя, отправившего запрос
- - `spec_id`
- - `command_id`

- `list_spec_commands(user_id: str, target_id: int), GET, user` - вывести команды спецификации, пользователь должен обладать машиной
- - `user_id` - `id` пользователя, отправившего запрос
- - `target_id`

- `delete_command_from_spec(user_id: str, spec_id: int, command_id: int), DELETE, user` - удалить команду из спецификации, пользователь должен обладать машиной
- - `user_id` - `id` пользователя, отправившего запрос
- - `spec_id`
- - `command_id`


Работа с группами, их ресурсами и входящими людьми:

- `create_group(user_id: str, cameras: list[int], machine_specs: list[int]), POST, user` - создать группу. Пользователь должен обладать соотв. камерами и машинами, все спецификации должны быть для разных машин
- - `user_id` - `id` пользователя, отправившего запрос
- - `cameras` - список `id` камер
- - `machine_specs` - список `id` различающихся машин 

- `list_groups(user_id: str), GET, user` - найти группы, созданные пользователем
- - `user_id` - `id` пользователя, отправившего запрос

- `delete_group(user_id: str, delete_id: int), DELETE, user` - удалить группу. Пользователь должен быть создателем группы
- - `user_id` - `id` пользователя, отправившего запрос
- - `delete_id` - `id` удаляемой группы

- `add_resource_to_group(user_id: str, group_id: int, resource_type: str, resource_id: int), POST, user` - добавить ресурс в группу, пользователь должен быть создателем группы и обладателем ресурса
- - `user_id` - `id` пользователя, отправившего запрос
- - `group_id`
- - `resource_type`. Тип ресурса, значения: `"camera", "machine_spec"`
- - `resource_id`

- `list_group_resources(user_id: str, group_id: int, resource_type: str), GET, user` - вывести ресурсы группы, пользователь должен быть создателем группы
- - `user_id` - `id` пользователя, отправившего запрос
- - `group_id`
- - `resource_type`. Тип ресурса, значения: `"camera", "machine_spec"`

- `delete_resource_from_group(user_id: str, group_id: int, resource_type: str, resource_id: int), DELETE, user` - удалить ресурс из группу, пользователь должен быть создателем группы
- - `user_id` - `id` пользователя, отправившего запрос
- - `group_id`
- - `resource_type`. Тип ресурса, значения: `"camera", "machine_spec"`
- - `resource_id`


- `add_to_group(user_id: str, group_id: int, target_user_id: str), POST, user` - добавить человека в группу, пользователь должен быть создателем группы
- - `user_id` - `id` пользователя, отправившего запрос
- - `group_id`
- - `target_user_id`

- `list_group_members(user_id: str, target_id: int), GET, user` - вывести членов группы, пользователь должен быть создателем группы
- - `user_id` - `id` пользователя, отправившего запрос
- - `target_id`

- `delete_from_group(user_id: str, group_id: int, target_user_id: str), DELETE, user` - удалить человека из группы, пользователь должен быть создателем группы
- - `user_id` - `id` пользователя, отправившего запрос
- - `group_id`
- - `target_user_id`

- `list_groups_i_am_in(user_id: str), GET, guest` - найти группы, в которые пользователь входит
- - `user_id` - `id` пользователя, отправившего запрос

- `leave_group(user_id: str, group_id: int), DELETE, guest` - покинуть группу
- - `user_id` - `id` пользователя, отправившего запрос
- - `group_id`
