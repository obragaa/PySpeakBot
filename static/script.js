// script.js
function sendMessage() {
    var input = document.getElementById("user-input");
    var message = input.value.trim();
    if (message !== "") {
        addToChat("Você: " + message);
        fetch('/ask', {
            method: 'POST',
            body: new URLSearchParams('message=' + message)
        })
        .then(response => response.json())
        .then(data => {
            addToChat("Bot: " + data.response);
        });
    }
    input.value = "";
}

function addToChat(message) {
    var chatBox = document.getElementById("chat-box");
    var newMessage = document.createElement("div");
    newMessage.textContent = message;
    chatBox.appendChild(newMessage);
    chatBox.scrollTop = chatBox.scrollHeight;
}
