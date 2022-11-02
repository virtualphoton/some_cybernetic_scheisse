# Описание
Есть ресурсы 2 типов - камеры и устройства:
- камеры транслируют видео
- устройства (Machine) - то, чему пользователи могут посылать команды через консоль (например, робот)

Пользователи могут обладать некоторыми из этих ресурсов (т.е. иметь право с ними взаимодействовать). Чтобы с ресурсами было удобнее работать, пользователи могут объединять их в группы (например, камера и несколько устройств), а также давать доступ к группам другим пользователям (т.е. другие пользователи получают права взаимодействия с ресурсами).

Но пользователь может захотеть сделать так, чтобы в разных группах было одно и тоже устройство, но списки разрешенных команд отличалист. Для этого в группы вместо самого устройства кладется спецификация - сущность, содержащая список разрешенных команд. Спецификации создаются пользователем, обладающим устройством. 
# Данные
Отношения: O-t-M - one-to-many, M-t-O, M-t-M.

Camera:
- `id: int, unique, not null`
- `name: str, not null`
- `holder: M-t-O(User), not null` - обладатель ресурсов
- `groups: M-t-M(Group)` - в каких группах присутствует
- `connection: not null`, категориальная из `{"url", "usb"}`
- `address: str, not null` - либо url, либо id (подключение через usb)
- `res_x, res_y: int` - разрешение (если нужно)

Machine - устройства:
- `id, name` - аналогично
- `url: str, not null` - url сервера, на который посылаются команды
- `holder: M-t-O(User), not null`
- `commands: O-t-M(Command)` - все доступные команды
- `specs: O-t-M(MachineSpec)` - созданные спецификации
- `js_path: str, not null` - путь к js-скрипту с командами
- `aruco_id: int, >= 0, < 1000` - номер на аруко-маркере (упрощенная версия QR-кода)

MachineSpec - спецификации - ограничения на список команд для машины:
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

- в группе все ресурсы должны иметь одного holder-а - создателя группы
- MachineSpec не должна содержать команд для другого устройства
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

В API каждая команда имеет первым скрытым параметром куки/id посылающего, по которому сервер может его определить.

Т. к. команды идут либо тройкой `add`, `list`, `delete` (м.б. еще с `modify`), параметры повторяются, а потому приводятся только для `add`. Команда типа `list` возвращает все столбцы сущностей.

Для Админа:

- работа с ресурсами, `resource_type` из `{Camera, Machine}`:
- - `add_resource(resource_type, resource_id, params...)`
- - `list_resources(resource_type)`
- - `delete_resource(resource_type, resource_id)`
- - `modify_resource(resource_type, resource_id, params..)`
- работа с доступными командами устройтсву:
- - `add_command(machine_id, comand_name)`
- - `list_commands(...)`
- - `delete_command(...)`
- подтверджение права на ресурс
- - `give_resource(user_id, resource_type, resource_id)`
- - `list_user_resources(...)`
- - `revoke_resource(...)`
- другое:
- - `delete_user_account(user_id)`

Для юзера - поиск людей:

- `list_usernames()`
- `user_id_from_username(user_id)`
- `get_my_username()`

Для юзера - менеджмент ресурсов и групп:

- создание спецификаций:
- - `list_commands(machine_id)`
- - `add_spec(machine_id, commands)` (`commands` - подмножество `get_commands(...)`)
- - `list_specs(...)`
- - `delete_spec(...)`
- модификация списка команд в спецификации
- - `add_command_to_spec(spec_id, command_id)`
- - `list_spec_commands(...)`
- - `delete_command_from_spec(spec_id, command_id)`
- работа с группами
- - `create_group(cameras, machine_specs)`
- - `list_groups()`
- - `delete_group(...)`
- модификация ресурсов в группе
- - `add_resource_to_group(group_id, resource_type, resource_id)`
- - `list_group_resources(...)`
- - `delete_resource_from_group(...)`
- добавление людей к группе:
- - `add_to_group(group_id, user_id)`
- - `list_group_members(...)`
- - `delete_from_group(...)`

Для юзеров и гостей:

- `leave_group(group_id)`
- `delete_my_account()`


# Технологии разработки
ЯП - Python

СУБД - SQLite3, работа с БД через модуль SQLalchemy
# Тестирование
