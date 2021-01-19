$( document ).ready(function() {
        
    var socket = io.connect();

    var username = "{{ current_user.name }}";
    var room_id = "{{ current_user.room_id }}";
    var rating = "{{ current_user.rating }}";

    socket.on('connect', data => {
        socket.emit('join', {'username': username, 'room': room_id});
    });

    socket.on('question_match', data => {
        var answer = window.confirm(data.question + "\nWould you like to answer that?");
        if (answer) {
            console.log(`You decided to answer this. ${data.room_id}`);
            socket.emit('redirect_asker', data);
            window.location.replace("http://127.0.0.1:5000/chat");
        } else {
            console.log('You dont want to.');
        }
    });

    socket.on('redirect', data => {
        window.location.replace("http://127.0.0.1:5000/chat");
    });


    document.querySelector('#acting').onclick = () => {
        if (document.querySelector('#question').value == "") {
            console.log("You must input question!");
        } else {
            socket.emit('match', {
                'choice': "Acting",
                'rating': rating,
                'question': document.querySelector('#question').value
            });
            document.querySelector('#question').value = ''; 
        }
        
    }

    document.querySelector('#photography').onclick = () => {
        if (document.querySelector('#question').value == "") {
            console.log("You must input question!");
        } else {
            socket.emit('match', {
                'choice': "Photography",
                'rating': rating,
                'question': document.querySelector('#question').value
            });
            document.querySelector('#question').value = ''; 
        }
        
    }

    document.querySelector('#model').onclick = () => {
        if (document.querySelector('#question').value == "") {
            console.log("You must input question!");
        } else {
            socket.emit('match', {
                'choice': "Model",
                'rating': rating,
                'question': document.querySelector('#question').value
            });
            document.querySelector('#question').value = ''; 
        }
        
    }

    console.log(username);
    console.log(rating);
    console.log(room_id);

    function doConfirm(data) {
        var answer = window.confirm(data.question + "\nWould you like to answer that?");
        if (answer) {
            console.log(`You decided to answer this. ${data.room_id}`);
            socket.emit('redirect_asker', data);
            window.location.replace("http://127.0.0.1:5000/chat");
        } else {
            console.log('You dont want to.');
        }
    }
});