document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect('http://' + document.domain + ':' + location.port);

    const room = document.querySelector('#get-room').innerHTML;
    const username = document.querySelector('#get-username').innerHTML;
    const rating = document.querySelector('#get-rating').innerHTML;

    socket.on('message', data => {
        console.log(`Message recieved: ${data}`);
    });

    socket.on('question_match', data => {
        console.log("pi6 mi q6kata");
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
    console.log(room);

    function removeElementsByClass(className){
        var elements = document.getElementsByClassName(className);
            while(elements.length > 0){
                elements[0].parentNode.removeChild(elements[0]);
            }
    }

});
