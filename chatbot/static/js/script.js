function appendUserInput(userInput) {
    const botResponseContainer = document.getElementById('botResponseContainer');
    const userInputElement = document.createElement('p');
    userInputElement.innerHTML = `<strong style="font-size: 20px;">You:</strong><br>${userInput}`;
    
    botResponseContainer.appendChild(userInputElement);
    botResponseContainer.scrollTop = botResponseContainer.scrollHeight;
}

function appendBotResponse(response, type) {
    const botResponseContainer = document.getElementById('botResponseContainer');
    const botResponseElement = document.createElement('p');

    // Check if the response is equal to the clientId
    if (response === "requestClientID") {
        botResponseElement.innerHTML = `<strong style="font-size: 20px;" id="requestClientID">Automate Sync:</strong><br>Please provide your client id`;
        window.automatesync={"requestClientID":true};
    } else {
        botResponseElement.innerHTML = `<strong style="font-size: 20px;">Automate Sync:</strong><br>${response}`;
        window.automatesync={"hasClientID":true,"requestClientID":false};
    }

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
    if(window?.automatesync?.requestClientID){
        setCookie("client_id",user_input)
        botResponseContainer.removeChild(loadingElement);
        appendBotResponse("Thank you! What can i help you with ?");
    }
    else{
        
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
    }
    

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

function handleKeyPress(event) {
    // Check if the pressed key is Enter (key code 13)
    if (event.keyCode === 13) {
        sendMessage();
    }
}

// Function to handle voice button click
function handleVoiceButtonClick() {
    // Add logic for handling voice input if needed
    console.log("Voice button clicked");
}

// Add event listeners to call sendMessage on Enter key press
document.getElementById('user_input').addEventListener('keypress', handleKeyPress);

// Add event listener for voice button click
document.getElementById('voiceButton').addEventListener('click', handleVoiceButtonClick);
