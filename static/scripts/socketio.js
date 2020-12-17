document.addEventListener('DOMContentLoaded', () => {

    const username = document.querySelector('#get-username').innerHTML;
    const rating = document.querySelector('#get-rating').innerHTML;
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('connect', () => {
        socket.send("Someone logged in");
        // document.getElementById("#acting").addEventListener("click", function () {
        //     console.log("chose acting")
                  
        // });
    
    });

    socket.on('message', data => {
        console.log(`Message recieved: ${data}`);
    });

    socket.on('test', data => {
        console.log(`Message recieved: ${data}`);
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
  
  
});
