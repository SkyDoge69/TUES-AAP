document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('connect', () => {
        socket.send("Someone logged in");
        // document.getElementById("#acting").addEventListener("click", function () {
        //     console.log("chose acting")
                  
        // });    
    });

    const room = document.querySelector('#get-room').innerHTML;
    const username = document.querySelector('#get-username').innerHTML;
    const rating = document.querySelector('#get-rating').innerHTML;
    joinRoom(room);

    socket.on('message', data => {
        console.log(`Message recieved: ${data}`);
    });

    socket.on('status', data => {
        var answer = window.confirm(data.question + "\nWould you like to answer that?");
        if (answer) {
            console.log('You decided to answer this.');
            removeElementsByClass('main-section');

            const p = document.createElement('p');
            p.innerHTML += data.question;
            document.querySelector('#display_stuff').append(p);

          } else {
            console.log('You dont want to.');
          }

        
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

    console.log(username);
    console.log(rating);
    console.log(room);
    
    function joinRoom(room) {
        socket.emit('join', {'room': room});
    }
    
    function leaveRoom(room) {
        socket.emit('leave', {'room': room});
    }

    function removeElementsByClass(className){
        var elements = document.getElementsByClassName(className);
            while(elements.length > 0){
                elements[0].parentNode.removeChild(elements[0]);
            }
        }

});
