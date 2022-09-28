# Описание
Ресурсы всего 2 типов - камеры и устройства:
- камеры транслируют видео
- устройства - то, чему пользователи могут посылать команды через консоль (например, роботы)

Пользователи могут владеть некоторыми из этих ресурсов, объединять их в группы (с различными ограничениями на разрешенные команды) и давать доступ к группам другим пользователям.
# Данные
Отношения: O-t-M - one-to-many, M-t-O, M-t-M.

Задаются в виде `O-t-M(table[, field])` - связь с таблицей `table`. Если связь двусторонняя, то в другой таблице связь через поле `field`.

Camera:
- `id: int, unique, not null`
- `name: str, not null`
- `holder: M-t-O(User), not null` - обладатель ресурсов
- `groups: M-t-M(Group)` - в каких группах присутствует
- `connection: not null`, категориальная из `{"url", "usb"}`
- `address: str, not null` - либо url, либо id (подключение через usb)
- `res_x, res_y: int` - разрешение (если нужно)

Machine:
- `id, name` - аналогично
- `url: str, not null` - url сервера, на который посылаются команды
- `holder: M-t-O(User), not null`
- `commands: O-t-M(Command)` - все доступные команды
- `specs: O-t-M(MachineSpec)` - созданные спецификации
- `js_path: str, not null` - путь к js-скрипту с командами
- `aruco_id: int, >= 0, < 1000` - номер на аруко-маркере (упрощенная версия QR-кода)

MachineSpec - ограничения на список команд для машины:
- `id, name` - ...
- `machine: M-t-O(Machine), not null` - от какой машины идет
- `commands: M-t-M(Command)` - разрешенные команды
- `groups: M-t-M(Group)` - в каких группах присутствует

Command:
- `id, name` - ...
- `machine: M-t-O(Machine), not null`
- `specs: M-t-M(MachineSpec)`

Group - группа из камер и устройств:
- `id, name` - ...
- `creator: M-t-O(User), not null` - создатель группы
- `users: M-t-M(User)` - люди, имеющие доступ к группе
- `cameras: M-t-M(Camera)`
- `machine_specs: M-t-M(MachineSpec)`

User:
- `id: str, unique, not null`
- `role: not null` - категориальная `{"user", "admin", "guest"}`
- `username: str, unique, not null`
- `cameras: O-t-M(Camera)` - обладание ресурсом
- `machines: O-t-M(Machine)` - обладание ресурсом
- `groups_created: O-t-M(Group)` - созданные группы
- `groups_member: M-t-M(Group)` - в какие группы входит

Общая целостность:

- в группе все ресурсы должны имеют одного обладателя - создателя
- в MachineSpec команды у спецификации от одной машины
# Пользовательские роли
Обычный пользователь:
- владеет ресурсами и может изменять их параметры
- может объединять свои ресурсы в группы
- может давать другим пользователям доступ к этим группам
- может получать доступ к группам (при этом он не становится владельцем ресурсов)

Администратор:
- те же права, что и у обычного пользователя
- может подтверждать, что другие пользователи владеют ресурсами
- всего 1 администратор

Гость:
- не может владеть ресурсами
- может получать доступ к ресурсам
- учетная запись удаляется, как только сессия заканчивается (log out или если какое-то время offline)

Суть роли гостя - возможность просто получить временный доступ к ресурсам (например при переходе по ссылке от пользователя).
# UI / API

Явного API не будет, т.к. команды будут обернуты в web-приложение. В API каждая команда имеет первым скрытым параметром куки/id посылающего, по которому сервер может его определить.

Для Админа:

- add_resource(resource_type, resource_id, **kwargs)
- - list_resources(resource_type)
- - delete_resource(resource_type, resource_id)
- - modify_resource(resource_type, resource_id, **kwargs)
- add_command(machine_id, comand_name)
- - list_commands(machine_id)
- - delete_command(machine_id, comand_id)
- give_resource(user_id, resource_type, resource_id)
- - list_user_resources(user_id, resource_type)
- - revoke_resource(user_id, resource_type, resource_id)

Для владельца ресурса:
- list_commands(machine_id)
- create_spec(machine_id, commands), commands - состоит в get_commands
- - specs_list(machine_id)
- - delete_spec(spec_id)
- add_command_to_spec(spec_id, command_id)
- - list_spec_commands(spec_id)
- - delete_command_from_spec(spec_id, command_id)
- create_group(cameras, machine_specs)
- - list_groups()
- - delete_group(group_id)
- add_resource_to_group(group_id, resource_type, resource_id)
- - list_group_resources(gorup_id)
- - delete_resource_from_group(group_id, resource_type, resource_id)
- add_to_group(group_id, user_id)
- - list_group_members(group_id)
- - remove_from_group(group_id, user_id)



# Технологии разработки
ЯП - Python

СУБД - SQLite3, работа с БД через модуль SQLalchemy
# Тестирование
