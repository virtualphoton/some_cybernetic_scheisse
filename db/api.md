Все запросы посылаются на адрес `/api/<method>` POST-запросом.

Если команда возвращает объект из предметной области, то в json-объекте поля, задающие множественное отношение, возвращаются как список `id` тех объектов, на которые они указвают; чтобы описать одиночное отношение, возвращается поле с внешним ключом остальные поля возвращаются как есть.

`user_id` выдается использующему api при авторизации.

Создание и выдача ресурсов:
- `add_resource(user_id: int, name: str, resource_type: str, params...), admin` - создать новый ресурс
- - `user_id` - `id` пользователя, отправившего запрос
- - `name` - название, длины не больше 40
- - `resource_type`. Тип ресурса, значения: `"camera", "machine"`
- - `params` - параметры объекта (передаются вместе с остальными аргументами):
- - - Для камеры, обязательные параметры - `connection, address`, необязательные - `res_x, res_y`
- - - `connection: str` - из `url`, `usb`
- - - `address: str`
- - - `res_x: int, res_y: int`
- - - Обязательные для машины:
- - - `url: str`
- - - `js_path: str`
- - - `aruco_id: int`, от 0 до 1000

- `list_resources(user_id: int, resource_type: str), admin` - вывести все ресуры данного типа
- - `user_id` - `id` пользователя, отправившего запрос
- - `resource_type`. Тип ресурса, значения: `"camera", "machine"`

- `delete_resource(user_id: int, resource_type: str, delete_id: int), admin` - удалить ресурс с данным `id`
- - `user_id` - `id` пользователя, отправившего запрос
- - `resource_type`. Тип ресурса, значения: `"camera", "machine"`
- - `delete_id` - id удаляемого ресурса

- `give_resource(user_id: int, target_user_id: int, resource_type: str, resource_id: int), admin` - выдать полльзователю право пользоваться ресурсом
- - `user_id` - `id` пользователя, отправившего запрос
- - `resource_type`. Тип ресурса, значения: `"camera", "machine"`
- - `target_user_id`
- - `resource_id`

- `list_user_resources(user_id: int, resource_type: str: str, target_id: str), admin` - вывести ресурсы пользователя
- - `user_id` - `id` пользователя, отправившего запрос
- - `resource_type`. Тип ресурса, значения: `"camera", "machine"`
- - `target_id` - id пользователя, чьи ресурсы интересуют

- `revoke_resource(user_id: int, resource_type: str: str, resource_id: int, target_user_id: int), admin` - удалить ресурс пользователя
- - `user_id` - `id` пользователя, отправившего запрос
- - `resource_type`. Тип ресурса, значения: `"camera", "machine"`
- - `target_user_id` - id пользователя, чьи ресурсы интересуют
- - `resource_id`


Работа с доступными устройтсву командами:
- `add_command(user_id: int, machine: int, name: str), admin` - создать команду для машины
- - `user_id` - `id` пользователя, отправившего запрос
- - `machine` - `id` машины, к которой привязана команда
- - `name` - имя команды

- `list_commands(user_id: int, target_id: int), user` - найти команды для машины. Пользователь должен владеть запрашиваемой машиной
- - `user_id` - `id` пользователя, отправившего запрос
- - `target_id` - `id` машины

- `delete_command(user_id: int, delete_id: int), admin` - удалить команду
- - `user_id` - `id` пользователя, отправившего запрос
- - `delete_id` - `id` удаляемой команды

Работа с аккаунтами и никами:
- `add_user(secret_key: str, username: str, role: str)` - регистрация новго пользователя
- - `secret_key` - специальный ключ для регистрации (т. к. за регистрацию отвечает сервис, а не на админ)
- - `username`
- - `role` - из `"admin", "user", "guest"`
- `delete_user_account(user_id: int, delete_id: str), admin` - удалить человека
- - `user_id` - `id` пользователя, отправившего запрос
- - `delete_id` - `id` удаляемого пользователя

- `list_usernames(user_id: int), user` - вывести ники всех пользователей

- `user_id_from_username(user_id: int, username: str), user` - `id` пользователя с соотв. ником
- - `user_id` - `id` пользователя, отправившего запрос

- `delete_my_account(user_id: int), guest` - удалить свой аккаунт


- `get_my_username(user_id: int), user` - получить свой ник


Работа со спецификациями:
- `add_spec(user_id: int, machine_id: int, commands: list[int]), user` - создать спецификацию. Пользователь должен обладать машиной, все команды должны быть для посылаемой машины
- - `user_id` - `id` пользователя, отправившего запрос
- - `machine_id` - машина, к которой привязана спецификация
- - `commands` - список `id` команд для спецификации

- `list_specs(user_id: int, target_id: int), user` - найти спецификации для машины, пользователь должен владеть машиной
- - `user_id` - `id` пользователя, отправившего запрос
- - `target_id` - `id` машины

- `delete_spec(user_id: int, delete_id: int), user` - удалить спецификации, пользователь должен владеть машиной
- - `user_id` - `id` пользователя, отправившего запрос
- - `delete_id` - `id` удаляемой спецификации


- `add_command_to_spec(user_id: int, spec_id: int, command_id: int), user` - добавить команду к спецификации, пользователь должен обладать машиной, команды и спецификация должны быть для одной машины
- - `user_id` - `id` пользователя, отправившего запрос
- - `spec_id`
- - `command_id`

- `list_spec_commands(user_id: int, target_id: int), user` - вывести команды спецификации, пользователь должен обладать машиной
- - `user_id` - `id` пользователя, отправившего запрос
- - `target_id`

- `delete_command_from_spec(user_id: int, spec_id: int, command_id: int), user` - удалить команду из спецификации, пользователь должен обладать машиной
- - `user_id` - `id` пользователя, отправившего запрос
- - `spec_id`
- - `command_id`


Работа с группами, их ресурсами и входящими людьми:

- `create_group(user_id: int, cameras: list[int], machine_specs: list[int]), user` - создать группу. Пользователь должен обладать соотв. камерами и машинами, все спецификации должны быть для разных машин
- - `user_id` - `id` пользователя, отправившего запрос
- - `cameras` - список `id` камер
- - `machine_specs` - список `id` различающихся машин 

- `list_groups(user_id: int), user` - найти группы, созданные пользователем
- - `user_id` - `id` пользователя, отправившего запрос

- `delete_group(user_id: int, delete_id: int), user` - удалить группу. Пользователь должен быть создателем группы
- - `user_id` - `id` пользователя, отправившего запрос
- - `delete_id` - `id` удаляемой группы

- `add_resource_to_group(user_id: int, group_id: int, resource_type: str, resource_id: int), user` - добавить ресурс в группу, пользователь должен быть создателем группы и обладателем ресурса
- - `user_id` - `id` пользователя, отправившего запрос
- - `group_id`
- - `resource_type`. Тип ресурса, значения: `"camera", "machine_spec"`
- - `resource_id`

- `list_group_resources(user_id: int, group_id: int, resource_type: str), user` - вывести ресурсы группы, пользователь должен быть создателем группы
- - `user_id` - `id` пользователя, отправившего запрос
- - `group_id`
- - `resource_type`. Тип ресурса, значения: `"camera", "machine_spec"`

- `delete_resource_from_group(user_id: int, group_id: int, resource_type: str, resource_id: int), user` - удалить ресурс из группу, пользователь должен быть создателем группы
- - `user_id` - `id` пользователя, отправившего запрос
- - `group_id`
- - `resource_type`. Тип ресурса, значения: `"camera", "machine_spec"`
- - `resource_id`


- `add_to_group(user_id: int, group_id: int, target_user_id: int), user` - добавить человека в группу, пользователь должен быть создателем группы
- - `user_id` - `id` пользователя, отправившего запрос
- - `group_id`
- - `target_user_id`

- `list_group_members(user_id: int, target_id: int), user` - вывести членов группы, пользователь должен быть создателем группы
- - `user_id` - `id` пользователя, отправившего запрос
- - `target_id`

- `delete_from_group(user_id: int, group_id: int, target_user_id: int), user` - удалить человека из группы, пользователь должен быть создателем группы
- - `user_id` - `id` пользователя, отправившего запрос
- - `group_id`
- - `target_user_id`

- `list_groups_i_am_in(user_id: int), guest` - найти группы, в которые пользователь входит
- - `user_id` - `id` пользователя, отправившего запрос

- `leave_group(user_id: int, group_id: int), guest` - покинуть группу
- - `user_id` - `id` пользователя, отправившего запрос
- - `group_id`
