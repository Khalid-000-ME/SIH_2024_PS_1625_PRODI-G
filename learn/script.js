document.getElementById('notes').addEventListener('click', function(){
    alert('Notes section clicked!');
});

document.getElementById('quiz').addEventListener('click', function() {
    fetch('http://127.0.0.1:5000/run-python-script')
    .then(response => response.json())
    .then(data => {
        document.getElementById('output').textContent = 'Python script output: ' + data.output;
    })
    .catch(error => {
        console.error('Error: ', error);
    });
});

document.getElementById('chatbot').addEventListener('click', function() {
    alert('Chatbot Section clicked!');
});
