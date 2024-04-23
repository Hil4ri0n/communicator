const friend_id = JSON.parse(document.getElementById('json-friend-id').textContent);
const user_id = JSON.parse(document.getElementById('json-user-id').textContent);

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + friend_id
    + '/'
);

const onlineSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/online_status/'
);

onlineSocket.onmessage = function (e){
    const data = JSON.parse(e.data);
    if(data.profile_id === friend_id){
       let onlineStatus = document.getElementById('online');
       onlineStatus.classList.toggle('hidden', !data.isOnline);
       console.log(friend_id, ' is online');
    }
}

chatSocket.onmessage = function(e){
    const data = JSON.parse(e.data);
    if(data.action === 'message'){
        if(data.sender_id === user_id){
        document.querySelector('.chat-box').innerHTML += ' <div class="message-wrapper">\n' +
                                            '                        <div class="user-message-content">\n' +
                                            '                            <p>'+data.message+'</p>\n' +
                                            '                        </div>\n' +
                                            '                    </div>';
        }else{
            document.querySelector('.chat-box').innerHTML += '<div class="message-wrapper">\n' +
                                                '                        <div class="message-content">\n' +
                                                '                            <p>'+data.message+'</p>\n' +
                                                '                        </div>\n' +
                                                '                    </div>';
            chatSocket.send(JSON.stringify({
                'action':'viewed',
                'sender_id':data.sender_id,
            }));
        }
        scrollToBottom()
    }else if(data.action === 'typing'){
        if(data.sender_id !== user_id) {
            let typing_div = document.querySelector('.typing-message');
            if (data.state === true) {
                typing_div.classList.remove('hidden');
            }else{
                typing_div.classList.add('hidden');
            }
        }
    }else if(data.action === 'viewed'){
        if(data.sender_id === user_id){
           let lastSeenMessage = document.getElementById('last-seen');
           if(lastSeenMessage){
               lastSeenMessage.removeAttribute('id');
               let eyeIcon = lastSeenMessage.querySelector('i');
               lastSeenMessage.removeChild(eyeIcon);
           }
           let messages = document.querySelectorAll(".user-message-content");
           let lastMessage = messages[messages.length - 1].querySelector('p');
           lastMessage.id = 'last-seen';
           lastMessage.innerHTML += '<i class="fa-solid fa-eye"></i>';
            console.log('wiadomosc od ', data.sender_id, ' wyswietlona');
        }
    }
}

document.querySelector('#message-submit').onclick = function(e){
    const message_input = document.querySelector('#message-input');
    const message = message_input.value;

    chatSocket.send(JSON.stringify({
        'action':'message',
        'message':message,
        'sender_id':user_id,
    }));

    message_input.value = '';
    toggleTyping({target: message_input});
}

function toggleTyping(event) {

    const value = event.target.value;
    const state = value !== ''; // true if typing, false if not

    chatSocket.send(JSON.stringify({
        'action': 'typing',
        'state': state,
        'sender_id': user_id,
    }));
}

document.getElementById('message-input').addEventListener('input', toggleTyping);

function scrollToBottom() {
    let chatBox = document.querySelector('.chat-box');
    chatBox.scrollTop = chatBox.scrollHeight;
}