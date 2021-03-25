document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect('http://' + document.domain + ':' + location.port);  

    const username = document.querySelector('#get-username').innerHTML;
    console.log(document.querySelector('#get-username').innerHTML);
    // console.log(localStorage.room_id)
    // console.log(localStorage.chat_id)

    
    let room = localStorage.chat_id;
    joinRoom(room);
   

    printSysMsg("Note: If you leave without leaving a rating, the user will be rated with 5 stars.");

    socket.on('message', data => {
        const p = document.createElement('p');
        const span_username = document.createElement('span');
        const span_timestamp = document.createElement('span');
        const br = document.createElement('br');
        let img = document.createElement("img");
        
        if (data.username == username) {
            p.setAttribute("class", "my-msg");
            span_username.setAttribute("class", "my-username");
            img.setAttribute("class", "my-img");
        }  else if (typeof data.username !== 'undefined') {
            p.setAttribute("class", "others-msg");    
            span_username.setAttribute("class", "other-username");
            img.setAttribute("class", "others-img");
        }
        else {
            printSysMsg(data.msg);
        }
        span_username.innerText = data.username;
        span_timestamp.setAttribute("class", "timestamp");
        span_timestamp.innerText = data.time_stamp;

        p.innerHTML += span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML;
        document.querySelector('#display-message-section').append(p);
        scrollDownChatWindow();
    });

    socket.on('disconnect', function() {
        leaveRoom(room);
        joinRoom(localStorage.room_id);
    });

    // window.onbeforeunload = function(){
    //     console.log('closing shared worker port...');
    //     return 'Take care now, bye-bye then.';
    // };

    document.querySelector('#send_message').onclick = () => {
        socket.send({'msg': document.querySelector('#user_message').value, 
        'username': username, 'room': room});
        document.querySelector('#user_message').value = '';
    }

    document.querySelector('#fiveStar').onclick = () => {
        leaveRoom(room);
        socket.emit('rate', {'rating': 5, 'room': room});
        window.location.replace("http://127.0.0.1:5000/");
    }

    document.querySelector('#fourStar').onclick = () => {
        leaveRoom(room);
        socket.emit('rate', {'rating': 4, 'room': room });
        window.location.replace("http://127.0.0.1:5000/");
    }

    document.querySelector('#threeStar').onclick = () => {
        leaveRoom(room);
        socket.emit('rate', {'rating': 3, 'room': room });
        window.location.replace("http://127.0.0.1:5000/");
    }

    document.querySelector('#twoStar').onclick = () => {
        leaveRoom(room);
        joinRoom(localStorage.room_id);
        socket.emit('rate', {'rating': 2, 'room': room });
        window.location.replace("http://127.0.0.1:5000/");
    }

    document.querySelector('#oneStar').onclick = () => {
        leaveRoom(room);
        socket.emit('rate', {'rating': 1, 'room': room });
        window.location.replace("http://127.0.0.1:5000/");
    }
    
    function scrollDownChatWindow() {
        const chatWindow = document.querySelector("#display-message-section");
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    function printSysMsg(msg) {
        const p = document.createElement('p');
        p.setAttribute("class", "system-msg");
        p.innerHTML = msg;
        document.querySelector('#display-message-section').append(p);
        document.querySelector("#user_message").focus();
    }

    function joinChat(room) {
        socket.emit('join_chat', {'username': username});
    }


    function joinRoom(room) {
        socket.emit('join', {'username': username, 'room': room});
    }
    
    function leaveRoom(room) {
        socket.emit('leave', {'username': username, 'room': room});
    }

});
