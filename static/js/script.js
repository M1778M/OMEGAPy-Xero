document.getElementById('user-input-form').addEventListener('submit', function (e) {
    e.preventDefault(); // Prevent form submission

    const userInput = document.getElementById('user-input');
    const userMessage = userInput.value;
    
    // Display user's message
    displayMessage(userMessage, 'user');

    // Clear the input field
    userInput.value = '';

    // Simulate bot response
    setTimeout(() => {
        const botResponse = getBotResponse(userMessage);
        displayMessage(botResponse, 'bot');
    }, 1000);
});

function displayMessage(message, sender) {
    const chatBox = document.getElementById('chat-box');
    const messageElement = document.createElement('div');
    messageElement.classList.add('chat-message');
    messageElement.classList.add(sender === 'user' ? 'user-message' : 'bot-message');
    messageElement.textContent = message;
    // <div class="chat-message user-message/bot-message">{content}</div>
    chatBox.appendChild(messageElement);
    
    // Scroll to the bottom of the chat
    chatBox.scrollTop = chatBox.scrollHeight;
}

function getBotResponse(userInput) {
    // Simple static responses for demo purposes
    if (userInput.toLowerCase().includes('hello')) {
        return "Hello! How can I assist you today?";
    } else if (userInput.toLowerCase().includes('how are you')) {
        return "I'm just a bunch of code, but thanks for asking!";
    } else {
        return "Sorry, I didn't understand that.";
    }
}