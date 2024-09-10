document.getElementById('send-button').addEventListener('click', function() {
    const prompt = document.getElementById('user-input').value;
    document.getElementById('chat-box').innerHTML += `<p><strong>You:</strong> ${prompt}</p>`;
    document.getElementById('user-input').value = '';

    // Send the message to the backend
    fetch(`http://127.0.0.1:5000/chatbot/${prompt}`)
    .then(response => response.text())
    .then(data => {
        document.getElementById('chat-box').innerHTML += `<p><strong>Bot:</strong> ${data}</p>`;
        document.getElementById('chat-box').scrollTop = document.getElementById('chat-box').scrollHeight;
    });
})