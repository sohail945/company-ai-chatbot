document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("user-input").focus();
    sendWelcomeMessage();  // Display the welcome message when chatbot opens
});

function sendWelcomeMessage() {
    let chatbox = document.getElementById("chat-box");  
    let botMessage = `<div class="bot-message">🤖 Hi, I'm Solutyics Bot, here to help you with any queries related to our company. How may I assist you today?</div>`;
    chatbox.innerHTML += botMessage;
}

function sendMessage() {
    let userInput = document.getElementById("user-input").value.trim();
    if (!userInput) return;

    let chatBox = document.getElementById("chat-box");

    // Add User Message
    chatBox.innerHTML += `<div class="chat-message user-message">${userInput}</div>`;
    document.getElementById("user-input").value = "";
    chatBox.scrollTop = chatBox.scrollHeight;

    // Show Typing Indicator
    let typingIndicator = document.createElement("div");
    typingIndicator.className = "chat-message bot-message typing";
    typingIndicator.innerHTML = `<i>Typing...</i>`;
    chatBox.appendChild(typingIndicator);
    chatBox.scrollTop = chatBox.scrollHeight;

    fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {
        // Remove Typing Indicator
        typingIndicator.remove();

        // Add Bot Response
        let botMessage = `<div class="chat-message bot-message">${data.bot_response.replace(/\n/g, "<br>")}</div>`;
        chatBox.innerHTML += botMessage;
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Something went wrong. Try again!");
    });
}

// Send message on Enter key
function handleKeyPress(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}
