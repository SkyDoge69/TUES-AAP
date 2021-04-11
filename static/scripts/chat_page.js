document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect('http://' + document.domain + ':' + location.port);  

    const username = document.querySelector('#get-username').innerHTML;
    console.log(document.querySelector('#get-username').innerHTML);
    

    printSysMsg("Note: If you leave without leaving a rating, the user will be rated with 5 stars.");

    //display question to both users
    if (localStorage.type == "Answering") {
        socket.emit("display_question", {'username': username})
    } else {
        printQuestionMsg(localStorage.question);
    }

    socket.on('display', data => {
        printSysMsg("Your first response will be saved as the answer. Make it understandable. ")
        printQuestionMsg(data.question);
    });

    let room = localStorage.chat_id;
    let msg_count = 0;
    let type = localStorage.type;
    joinRoom(room);
   

    
    

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
        msg_count++;
        console.log(localStorage.type);
    
        if (msg_count == 1 && localStorage.type == "Answering") {
            socket.emit('save_answer', {'answer': data.msg, 'username': username, 'type': localStorage.type});
            msg_count = 2;
        }
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

    function printQuestionMsg(msg) {
        const p = document.createElement('p');
        p.setAttribute("class", "question-msg");
        p.innerHTML = msg;
        document.querySelector('#display-message-section').append(p);
        document.querySelector("#user_message").focus();
    }

    // function saveAnswer(msg_count, type, msg, question) {
    //     if (msg_count == 1 && type == "Answering") {
    //         socket.emit('save_answer', {'answer': msg, 'question': question});
    //         msg_count = 2;
    //     }
    // }

    function joinRoom(room) {
        socket.emit('join', {'username': username, 'room': room});
    }
    
    function leaveRoom(room) {
        socket.emit('leave', {'username': username, 'room': room});
    }


});
