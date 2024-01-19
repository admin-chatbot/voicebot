function appendUserInput(userInput) {
    const botResponseContainer = document.getElementById('botResponseContainer');
    const userInputElement = document.createElement('p');
    userInputElement.innerHTML = `<strong style="font-size: 20px;">You:</strong><br>${userInput}`;
    
    botResponseContainer.appendChild(userInputElement);
    botResponseContainer.scrollTop = botResponseContainer.scrollHeight;
}

function appendBotResponse(response) {
    const botResponseContainer = document.getElementById('botResponseContainer');
    const botResponseElement = document.createElement('p');
    botResponseElement.innerHTML = `<strong style="font-size: 20px;">Automate Sync:</strong><br>${response}`;
    
    botResponseContainer.appendChild(botResponseElement);
    botResponseContainer.scrollTop = botResponseContainer.scrollHeight;
}

function sendMessage() {
    const userInputElement = document.getElementById('user_input');
    const user_input = userInputElement.value;

    appendUserInput(user_input);

    const loadingElement = document.createElement('p');
    loadingElement.innerHTML = 'Bot is typing...';
    loadingElement.classList.add('loading-animation');
    botResponseContainer.appendChild(loadingElement);

    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `user_input=${encodeURIComponent(user_input)}`,
    })
    .then(response => response.text())
    .then(bot_response => {
        botResponseContainer.removeChild(loadingElement);
        appendBotResponse(bot_response);
    })
    .catch(error => {
        console.error('Error sending message:', error);
    });

    userInputElement.value = '';
}
// Function to generate a random user ID
function generateUserId() {
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    const userIdLength = 12; // Adjust the length as needed
    let userId = '';

    for (let i = 0; i < userIdLength; i++) {
        const randomIndex = Math.floor(Math.random() * characters.length);
        userId += characters.charAt(randomIndex);
    }

    return userId;
}

// Function to set a cookie
function setCookie(name, value, days) {
    const expires = new Date();
    expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
    document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/`;
}

// Example of generating a user ID and setting a cookie
const generatedUserId = generateUserId();
setCookie('userId', generatedUserId, 30); // Set the cookie to expire in 30 days

console.log('Generated User ID:', generatedUserId);

// Function to get the value of a cookie by name
function getCookie(name) {
    const cookies = document.cookie.split(';');
    for (const cookie of cookies) {
        const [cookieName, cookieValue] = cookie.trim().split('=');
        if (cookieName === name) {
            return cookieValue;
        }
    }
    return null;
}

// Example of reading the user ID from the cookie
const userIdFromCookie = getCookie('userId');

if (userIdFromCookie) {
    console.log('User ID from Cookie:', userIdFromCookie);
} else {
    console.log('User ID not found in Cookie');
}