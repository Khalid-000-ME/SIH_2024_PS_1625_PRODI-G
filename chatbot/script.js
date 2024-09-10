document.getElementById('send-button').addEventListener('click', function() {
    const name = document.getElementById('user-input').value;
    document.getElementById('chat-box').innerHTML += `<p><strong>You:</strong> ${name}</p>`;
    document.getElementById('user-input').value = '';

    // Send the message to the backend
    fetch(`http://127.0.0.1:5000/greet/${name}`)
    .then(response => response.text())
    .then(data => {
        document.getElementById('chat-box').innerHTML += `<p><strong>Bot:</strong> ${data}</p>`;
        document.getElementById('chat-box').scrollTop = document.getElementById('chat-box').scrollHeight;
    });
})
