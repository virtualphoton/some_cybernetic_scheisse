// not dry
$terminal_attached = $('#terminal');

function create_url(end) {
    return window.location.href + end
}


$(function () {
    let get_machines_url = create_url('get_machines')
    setInterval(function () {
        $.ajax(get_machines_url, {
            timeout: 500,
            success: function (data) {
                data.sort((fst, snd) => (snd.connected - fst.connected || snd.aruco_id - fst.aruco_id))
                $('#list li').remove()
                data.forEach(function (row) {
                    let inner_html = `<p>${row.aruco_id}: ${row.name}</p>`
                    if (row.connected)
                        inner_html += `<button id="b_off_${row.aruco_id}" class="button disconnect">Disonnect</button>`
                    else
                        inner_html += `<button id="b_on_${row.aruco_id}" class="button connect">Connect</button>`
                    $('#list').append(`<li id="m_${row.aruco_id}">${inner_html}</li>`)
                })
            }
        })
    }, 2000)

    let toggle_state_url = create_url('toggle_state')
    $('#list').on('click', function (event) {
        let id = event.target.id
        if (id.startsWith('b_'))
            $.ajax(toggle_state_url, {
                data: JSON.stringify({button_id: id}),
                method: 'POST',
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                success: data => {
                    if (data.type === 'has_connected') {
                        $.getScript(create_url(data.commands_url))
                    } else if (data.type === 'has_disconnected') {
                        console.log(123)
                        $terminal_attached.terminal().pop()
                    }
                }
            })
    })
})


$terminal_attached.terminal({
    add: function (...args) {
        this.echo(args.reduce((a, b) => a + b));
    },
    cat: function () {
        const img = $('<img src="https://placekitten.com/400/400">');
        img.on('load', this.resume);
        this.pause();
        this.echo(img);
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
    }
}, {
    checkArity: false,
    greetings: '`help` is actually a valid command',
    completion: true
});