const online_profile_id = JSON.parse(document.getElementById('json-user-id').textContent);

const onlineSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/online_status/'
);

onlineSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        if(data.profile_id !== online_profile_id){
            let friendBoxes = document.getElementsByClassName('friend-box');
            friendBoxes = Array.from(friendBoxes);
            console.log('id od consumera', data.profile_id);
            friendBoxes.forEach((friendBox) => {
                let friend_id = parseInt(friendBox.getAttribute('data-profile_id'))
                if(friend_id === data.profile_id){
                    friendBox.querySelector('.online-circle').classList.toggle('hidden', !data.isOnline);
                    console.log(friend_id, ' is online');
                }
            });
        }
};

