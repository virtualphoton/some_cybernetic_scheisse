// not dry
let $terminal_attached = $('#terminal');

function print_msg_from_resp(terminal, response){
    response.json().then(function (resp){ terminal.echo(resp.msg) })
}

$(function(){
    console.log(1)
    let get_machines_url = window.location.href + 'get_machines'
    setInterval( function(){
        $.ajax(get_machines_url, {
            timeout: 500,
            success: function (data){
                console.log(data)
            }
        })
    }, 1000)
})

$terminal_attached.terminal({
    cat: function () {
        const img = $('<img src="https://placekitten.com/400/400">');
        img.on('load', this.resume);
        this.pause();
        this.echo(img);
    },
    move_to: function (x, y) {
        if (typeof (x) == 'number' && typeof (y) == 'number') {
            const requestOptions = {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({command: 'move_to', args: [x, y]})
            }
            let address = window.location.href + 'send_command';
            fetch(address, requestOptions).then(async response => {
                // check for error response
                if (!response.ok) {
                    // get error message from body or default to response status
                    const error = response.status;
                    return Promise.reject(error);
                }
                //this.echo(response.json().msg)
            }).catch(error => {
                this.echo(error);
            })
        } else
            this.echo('Params must be numbers!')
    },

    change_res: function (x, y) {
        if (x === '~')
            x = 960
        if (y === '~')
            y = 540
        let $stream = $("#stream");
        $stream.attr("width", `${x}`);
        $stream.attr("height", `${y}`);
    },

    general: function (command) {
        const requestOptions = {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                command: command, args:
                    Array.prototype.slice.call(arguments, 1)
            })
        }
        let address = window.location.href + 'send_command';
        fetch(address, requestOptions).then(async response => {
            // check for error response
            if (!response.ok) {
                // get error message from body or default to response status
                const error = response.status;
                return Promise.reject(error);
            }
            //this.echo(response.json().msg)
        }).catch(error => {
            this.echo(error);
        })
    },

    set_cam_height: function (h) {
        if (typeof (h) == 'number' && h > 3) {
            const requestOptions = {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({command: 'change_height', args: [h]})
            }
            let address = window.location.href + 'send_command';
            fetch(address, requestOptions).then(async response => {
                if (!response.ok) {
                    const error = response.status;
                    return Promise.reject(error);
                }
                print_msg_from_resp(this, response)

            }).catch(error => {
                this.echo(error);
            })
        } else
            this.echo('Height must be a number higher than 3!')
    },
    help: function () {
        this.echo('you can use Tab for autocomplete\n' + 'Ctrl+F5 for static files to reload\n\n' +
            'move_to <x> <y>\n' + 'set_cam_height <h>\n' + 'cat',
        );
    },
    hell: function () {
        console.log('Hello, world!')
    }
}, {
    greetings: '`help` is actually a valid command',
    completion: true
});
$terminal_attached.terminal.push({
    hello: function () {
        console.log('Hello, world!')
    },
    help: function () {
        this.echo('you can use Tab for autocomplete\n' + 'Ctrl+F5 for static files to reload\n\n' +
            'move_to <x> <y>\n' + 'set_cam_height <h>\n' + 'cat',
        );
    },
});