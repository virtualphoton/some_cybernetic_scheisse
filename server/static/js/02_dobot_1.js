let commands_url = create_url('send_command')

$terminal_attached.terminal().push({
        move_xyz: function (x, y, z) {
            $.ajax(commands_url, {
                method: 'POST', contentType: 'application/json; charset=utf-8', dataType: 'json',
                data: JSON.stringify({
                    command: 'move_xyz',
                    args: [[x, y, z]],
                    id: 2
                })
            })
        },

        help: function () {
            this.echo(
                'move_xyz <x> <y> <z> - move robot to these coordinates relative to home position',
            );
        }
    },
    {
        name: '1',
        prompt: '1> ',
        greetings: 'type `help` to find out commands',
        completion: true,
        checkArity: false
    }
)