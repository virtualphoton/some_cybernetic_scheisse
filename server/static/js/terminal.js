// not dry

$('body').terminal({
    cat: function() {
        const img = $('<img src="https://placekitten.com/400/400">');
        img.on('load', this.resume);
        this.pause();
        this.echo(img);
    },
    move_to: function(x, y) {
        if (typeof(x) == 'number' && typeof(y) == 'number') {
            const requestOptions = {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ command:'move_to', args:[x, y]})
            }
            let address = window.location.href + 'send_command';
            fetch(address, requestOptions).then( async response => {
                // check for error response
                if (!response.ok) {
                    // get error message from body or default to response status
                    const error = response.status;
                    return Promise.reject(error);
                }
                //this.echo(response.json().msg)
            }).catch(error => { this.echo(error); })
        } else
            this.echo('Params must be numbers!')
    },

    change_res: function(x, y) {
        if (typeof(x) == 'number' && x > 0 && typeof(y) == 'number' && y > 0) {
            const requestOptions = {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ command:'change_res', args:[[x, y]]})
            }
            let address = window.location.href + 'send_command';
            fetch(address, requestOptions).then( async response => {
                // check for error response
                if (!response.ok) {
                    // get error message from body or default to response status
                    const error = response.status;
                    return Promise.reject(error);
                }
                //this.echo(response.json().msg)
            }).catch(error => { this.echo(error); })
        } else
            this.echo('Params must be numbers!')
    },

    set_cam_height: function(h) {
        if (typeof(h) == 'number' && h > 3) {
            const requestOptions = {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ command:'change_height', args:h})
            }
            let address = window.location.href + 'send_command';
            fetch(address, requestOptions).then( async response => {
                // check for error response
                if (!response.ok) {
                    // get error message from body or default to response status
                    const error = response.status;
                    return Promise.reject(error);
                }
                // why the fuck it prints {"msg": "Success!"}
                // but when i print json().msg it prints undefined?
                //this.echo(response.json())
            }).catch(error => { this.echo(error); })
        } else
            this.echo('Height must be a number higher than 3!')
    },
    help: function() {
        this.echo('you can use Tab for autocomplete\n' + 'Ctrl+F5 for static files to reload\n\n' +
                'move_to <x> <y>\n' + 'set_cam_height <h>\n' + 'cat',
                );
    },
}, {
    greetings: '`help` is actually a valid command',
    completion: true
});