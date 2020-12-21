document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('connect', () => {
        socket.send("Someone logged in");
    });

    const room = document.querySelector('#get-room').innerHTML;
    const username = document.querySelector('#get-username').innerHTML;
    const rating = document.querySelector('#get-rating').innerHTML;
    joinRoom(room);

    socket.on('message', data => {
        console.log(`Message recieved: ${data}`);
    });

    socket.on('question_match', data => {
        var answer = window.confirm(data.question + "\nWould you like to answer that?");
        if (answer) {
            console.log('You decided to answer this.');
            removeElementsByClass('main-section');
            const p = document.createElement('p');
            p.innerHTML += data.question;
            document.querySelector('#display_stuff').append(p);
            socket.emit('redirect_asker', {
                'question': data.question,
                'user_id': data.user_id,
                'room_substring': data.room_substring
            })
            console.log(data.room_substring);
            //iskame da se generira substring ot id-to i na dvamata, i tova da e ob6t room?
            //code to redirect here soon
            // joinRoom(data.room_substring)
          } else {
            console.log('You dont want to.');
          }
    });

    socket.on('redirect', data => {
        removeElementsByClass('main-section');
        const p = document.createElement('p');
        p.innerHTML += data.question;
        document.querySelector('#display_stuff').append(p);
        console.log(data.room_substring);
        // code to redirect here
        // joinRoom(data.room_substring);
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
    
    function joinRoom(room) {
        socket.emit('join', {'username': username, 'room': room});
    }
    
    function leaveRoom(room) {
        socket.emit('leave', {'username': username, 'room': room});
    }

    function removeElementsByClass(className){
        var elements = document.getElementsByClassName(className);
            while(elements.length > 0){
                elements[0].parentNode.removeChild(elements[0]);
            }
    }

});
