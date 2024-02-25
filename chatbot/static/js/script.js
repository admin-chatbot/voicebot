function appendUserInput(userInput) {
    const botResponseContainer = document.getElementById('botResponseContainer');
    const chatResponseContainer = document.getElementById('chatContainer');
    const userInputElement = document.createElement('p');
    userInputElement.innerHTML = `<strong style="font-size: 20px;">You:</strong><br>${userInput}`;
    
    botResponseContainer.appendChild(userInputElement);
    chatResponseContainer.scrollTop = chatResponseContainer.scrollHeight;
}


function appendBotResponse(response, type) {
    const botResponseContainer = document.getElementById('botResponseContainer');
    const chatResponseContainer = document.getElementById('chatContainer');
    const botResponseElement = document.createElement('p');

    let index = 0; // Index to track the character being appended

    function typeWriter() {
        if (index < response.length) {
            botResponseElement.innerHTML += response.charAt(index);
            index++;
            // Scroll to the bottom after each character is appended
            chatResponseContainer.scrollTop = chatResponseContainer.scrollHeight;
            setTimeout(typeWriter, 20); // Adjust the delay (in milliseconds) as needed
        } else {
            // Scroll to the bottom after typing is complete
            chatResponseContainer.scrollTop = chatResponseContainer.scrollHeight;
          
        }
    }
    if (response === "requestClientID") {
        botResponseElement.innerHTML = `<strong style="font-size: 20px;" id="requestClientID">Automate Sync:</strong><br>Please provide your client id`;
        if (window && window.automatesync) {
            window.automatesync.requestClientID = true;
        }
    } else {
        botResponseElement.innerHTML = `<strong style="font-size: 20px;">Automate Sync:</strong><br>`;
        if (window && window.automatesync) {
            window.automatesync.hasClientID = true;
            window.automatesync.requestClientID = false;

        }
         // Start the typing animation
        typeWriter();
    }

    // Append the element to the container
    botResponseContainer.appendChild(botResponseElement);
}


function sendMessage() {
    const userInputElement = document.getElementById('user_input');
    let user_input = userInputElement.value;
    let responded_to_user = false;
    appendUserInput(user_input);

    const loadingElement = document.createElement('p');
    loadingElement.innerHTML = 'Bot is typing...';
    loadingElement.classList.add('loading-animation');
    const botResponseContainer = document.getElementById('botResponseContainer');
    botResponseContainer.appendChild(loadingElement);
    const chatResponseContainer = document.getElementById('chatContainer');
    chatResponseContainer.scrollTop = chatResponseContainer.scrollHeight;
    
    if (!window.automatesync) {
        window.automatesync = {}
    }
    if (window && window.automatesync && window.automatesync.requestClientID) {
        setCookie("client_id", user_input);
        botResponseContainer.removeChild(loadingElement);
        appendBotResponse("Thank you! What can i help you with ?");
    }
    else {
        if (window && window.automatesync && window.automatesync.setRequestParameter) {
            setCookie(window.automatesync.requestParameter, user_input);
            window.automatesync.setRequestParameter = false;
        }
        if (window && window.automatesync && window.automatesync.intent) {
            //user_input = window.automatesync.intent;
            window.automatesync.intent = null; // Set intent to null after assigning it to user_input
        }
        
        
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `user_input=${encodeURIComponent(user_input)}&user_id=${encodeURIComponent(window.automatesync.userId)}`,
        })        
        .then(response => response.text())
        .then(bot_response => {
            try {
                let responseData = JSON.parse(bot_response);
            
                // Check if responseData is an object and not null
                if (typeof responseData === 'object' && responseData !== null) {
                    // Check if requestParameter field exists
                    if ('requestParameter' in responseData) {
                        // requestParameter field exists, you can access its value
                        if (window && window.automatesync) {
                            window.automatesync.setRequestParameter = true;
                            window.automatesync.requestParameter = responseData.requestParameter;
                            window.automatesync.intent = responseData.intent;
                            bot_response = responseData.description;
                            console.log("requestParameter exists:", responseData.requestParameter);
                        }
                    
                    } else {
                        console.log("requestParameter does not exist");

                    }
                } else {
                    // responseData is not JSON
                    console.log("Response is not JSON");
                }
                if(responseData.type=="pdf") {
                    // requestParameter field does not exist
                    botResponseContainer.removeChild(loadingElement);
                    appendPDF("dowload.pdf",responseData.fileName)
                    responded_to_user=true
                }else{
                    botResponseContainer.removeChild(loadingElement);
                    appendBotResponse(bot_response);
                }
            
        }catch (error) {
            console.log("Error parsing JSON:", error);
        }
        if(!responded_to_user){
            
        botResponseContainer.removeChild(loadingElement);
        appendBotResponse(bot_response);
        }
    })
        .catch(error => {
            console.error('Error sending message:', error);
        });
    }
    

    userInputElement.value = '';
}
function appendPDF(pdfFileName, pdfLocation) {
    const pdfContainer = document.getElementById('botResponseContainer');
    pdfContainer.innerHTML = `<strong style="font-size: 20px;">Automate Sync:</strong><br>`;

    // Create a download link
    const downloadLink = document.createElement('a');
    downloadLink.href = pdfLocation;
    downloadLink.setAttribute('download', pdfFileName);
    downloadLink.innerText = 'Download PDF';

    // Create an iframe for embedded view
    const embedView = document.createElement('iframe');
    embedView.src = pdfLocation;
    embedView.style.width = '100%';
    embedView.style.height = '600px'; // Set the height as needed

    // Append the download link and embedded view to the container
    pdfContainer.appendChild(downloadLink);
    pdfContainer.appendChild(document.createElement('br')); // Add a line break
    pdfContainer.appendChild(embedView);
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
if (!window.automatesync) {
    window.automatesync = {}
}
window.automatesync.userId=generatedUserId;
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

// Add event listeners to call sendMessage on Enter key press
document.getElementById('user_input').addEventListener('keypress', handleKeyPress);

// Add event listener for voice button click
document.getElementById('voiceButton').addEventListener('click', handleVoiceButtonClick);
function handleVoiceButtonClick(event){
    const recognition = new webkitSpeechRecognition() || new SpeechRecognition();

    recognition.lang = 'en-US';
    recognition.interimResults = false;

    recognition.onresult = function(event) {
        const result = event.results[0][0].transcript;
        document.getElementById('user_input').value = result;
    };

    recognition.onerror = function(event) {
        alert('Speech recognition error: ' + event.error);
    };

    recognition.onend = function() {
       console.log("you said",result);
       sendMessage()
    };

    recognition.start();

}
