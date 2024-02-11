// chat-script.js

(function () {
    // Create a chat container
    const chatContainer = document.createElement('div');
    chatContainer.id = 'chatContainer';
    chatContainer.style.display = 'none';
    // Append the chat container to the body
    document.body.appendChild(chatContainer);

    // Create a chat icon
    const chatIcon = document.createElement('div');
    chatIcon.id = 'chatIcon';
    chatIcon.innerHTML = '<img src="static/assets/chat-icon.svg" alt="Chat Icon" style="width: 100%; height: 100%;">';

    chatIcon.onclick = toggleChat;

    // Append the chat icon to the body
    document.body.appendChild(chatIcon);

    // Create the chat form and append it to the chat container
    const chatForm = document.createElement('iframe');
    chatForm.src = 'chat-form'; // Replace with your actual chat form URL
    chatForm.width = '100%';
    chatForm.height = '100%';
    chatForm.frameBorder = '0';

    chatContainer.appendChild(chatForm);

    // Function to toggle the chat visibility
    function toggleChat() {
        chatContainer.style.display = chatContainer.style.display === 'none' ? 'block' : 'none';
    }
})();
