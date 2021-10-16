let commands_url = create_url('send_command')

$terminal_attached.terminal().push({
        move_to: function (...args) {
            let xyz = args.slice(0, 3)
            let rpy = args.slice(3)
            $.ajax(commands_url, {
                method: 'POST', contentType: 'application/json; charset=utf-8', dataType: 'json',
                data: JSON.stringify({
                    command: 'move_to',
                    args: rpy.length ? [xyz, rpy] : [xyz],
                    id: 1
                })
            })
        },

        help: function () {
            this.echo(
                'move_to <x> <y> <z> [<r> <p> <y>] - move robot to these coordinates',
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