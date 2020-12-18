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
        // console.log(msg);
        var btn1 = document.querySelector('#acting');
        var btn2 = document.querySelector('#photography');
        var btn3 = document.querySelector('#model');
        btn1.parentNode.removeChild(btn1);
        btn2.parentNode.removeChild(btn2);
        btn3.parentNode.removeChild(btn3);
        const p = document.createElement('p');
        p.innerHTML += "lol";
        document.querySelector('#display_stuff').append(p);
        
    });

    document.querySelector('#acting').onclick = () => {
        console.log('chose acting');
        socket.emit('match', {
            'choice': "Acting",
            'rating': rating
        });
        // window.location.href = "http://127.0.0.1:5000/chat";  
        
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

});
