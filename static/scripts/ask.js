    // const tagContainer = document.querySelector('.tag-container');
    //     const input = document.querySelector('.tag-container input');
    //     let tags = [];

    //     function createTag(label) {
    //         const div = document.createElement('div');
    //         div.setAttribute('class', 'tag');
    //         const span = document.createElement('span');
    //         span.innerHTML = label;
    //         const closeIcon = document.createElement('i');
    //         closeIcon.innerHTML = 'close';
    //         closeIcon.setAttribute('class', 'material-icons');
    //         closeIcon.setAttribute('data-item', label);
    //         div.appendChild(span);
    //         div.appendChild(closeIcon);
    //         return div;
    //     }

    //     function clearTags() {
    //         document.querySelectorAll('.tag').forEach(tag => {
    //             tag.parentElement.removeChild(tag);
    //         });
    //     }

    //     function addTags() {
    //         clearTags();
    //         tags.slice().reverse().forEach(tag => {
    //             tagContainer.prepend(createTag(tag));
    //         });
    //     }

    //     input.addEventListener('keyup', (e) => {
    //         if (e.key === 'Enter') {
    //             e.target.value.split(',').forEach(tag => {
    //                 tags.push(tag);  
    //             });
    //             addTags();
    //             input.value = '';
    //         }
    //     });

    //     document.addEventListener('click', (e) => {
    //         if (e.target.tagName === 'I') {
    //             const tagLabel = e.target.getAttribute('data-item');
    //             const index = tags.indexOf(tagLabel);
    //             tags = [...tags.slice(0, index), ...tags.slice(index+1)];
    //             addTags();    
    //         }
    //     })


    //     input.focus();

    //     localStorage.room_id = '{{ user.room_id }}';
    //     console.log(localStorage.room_id);
    //     $( document ).ready(function() {
    //     var socket = io.connect();

    //     var username = '{{ user.name }}';
    //     var room_id = '{{ user.room_id }}';
    //     var rating = '{{ user.rating }}';

    //     socket.on('connect', data => {
    //         socket.emit('join', {'username': username, 'room': room_id});
    //     });

    //     socket.on('question_match', data => {
    //         console.log("ivona e gei");
    //         var answer = window.confirm(data.question + "\nWould you like to answer that?");
    //         if (answer) {
    //             console.log(`You decided to answer this. ${data.room_id}`);
    //             socket.emit('redirect_asker', data);
    //             window.location.replace("http://127.0.0.1:5000/chat");
    //         } else {
    //             console.log('You dont want to.');
    //         }
    //     });

    //     socket.on('redirect', data => {
    //         localStorage.chat_id = '{{ user.chat_id }}';
    //         window.location.replace("http://127.0.0.1:5000/chat");
    //     });


    // document.querySelector('#acting').onclick = () => {
    //     if (document.querySelector('#question').value == "") {
    //         console.log("You must input question!");
    //     } else {
    //         socket.emit('match', {
    //             'choice': "Acting",
    //             'rating': rating,
    //             'question': document.querySelector('#question').value,
    //             'tags': tags
    //         });
    //         console.log(tags);
    //         localStorage.question = document.querySelector('#question').value;
    //         document.querySelector('#question').value = ''; 
    //     }
        
    // }

    // document.querySelector('#photography').onclick = () => {
    //     if (document.querySelector('#question').value == "") {
    //         console.log("You must input question!");
    //     } else {
    //         socket.emit('match', {
    //             'choice': "Photography",
    //             'rating': rating,
    //             'question': document.querySelector('#question').value
    //         });
    //         console.log(tags);
    //         localStorage.question = document.querySelector('#question').value;
    //         document.querySelector('#question').value = ''; 
    //     }
        
    // }

    // document.querySelector('#model').onclick = () => {
    //     if (document.querySelector('#question').value == "") {
    //         console.log("You must input question!");
    //     } else {
    //         socket.emit('match', {
    //             'choice': "Model",
    //             'rating': rating,
    //             'question': document.querySelector('#question').value
    //         });
    //         console.log(tags);
    //         localStorage.question = document.querySelector('#question').value;
    //         document.querySelector('#question').value = ''; 
    //     }
        
    // }

    // console.log(username);
    // console.log(rating);
    // console.log(room_id);
    //   });