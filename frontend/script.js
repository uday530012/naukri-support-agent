const API_URL = "/chat";

const chatContainer = document.getElementById("chat-container");
const messageInput = document.getElementById("message-input");
const sendButton = document.getElementById("send-button");


function addUserMessage(message) {
    const messageWrapper = document.createElement("div");
    messageWrapper.className = "user-message";

    messageWrapper.textContent = message;

    chatContainer.appendChild(messageWrapper);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}


function addAssistantMessage(result) {
    const messageWrapper = document.createElement("div");
    messageWrapper.className = "assistant-message";

    let responseText = "";

    if (result.response) {
        responseText += result.response;
    }

    if (result.source) {
        responseText += "\n\nSource: " + result.source;
    }

    if (result.next_action) {
        responseText += "\n\nNext Action: " + result.next_action;
    }

    messageWrapper.textContent = responseText;

    chatContainer.appendChild(messageWrapper);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}


function addLoadingMessage() {
    const loadingMessage = document.createElement("div");

    loadingMessage.id = "loading-message";
    loadingMessage.className = "assistant-message";
    loadingMessage.textContent = "Thinking...";

    chatContainer.appendChild(loadingMessage);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}


function removeLoadingMessage() {
    const loadingMessage = document.getElementById("loading-message");

    if (loadingMessage) {
        loadingMessage.remove();
    }
}


async function sendMessage() {

    const message = messageInput.value.trim();

    if (!message) {
        return;
    }

    // Show user's message
    addUserMessage(message);

    // Clear input
    messageInput.value = "";

    // Disable controls
    sendButton.disabled = true;
    messageInput.disabled = true;

    // Show loading
    addLoadingMessage();

    try {

        const response = await fetch(API_URL, {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })
        });


        removeLoadingMessage();


        if (!response.ok) {
            throw new Error("Server returned status " + response.status);
        }


        const result = await response.json();

        addAssistantMessage(result);


    } catch (error) {

        removeLoadingMessage();

        console.error("Chat error:", error);

        addAssistantMessage({
            response: "Sorry, I could not connect to the support agent. Please try again.",
            source: "System",
            next_action: "Check that the FastAPI server is running."
        });

    } finally {

        sendButton.disabled = false;
        messageInput.disabled = false;

        messageInput.focus();
    }
}


// Send button
sendButton.addEventListener("click", sendMessage);


// Press Enter to send
messageInput.addEventListener("keydown", function(event) {

    if (event.key === "Enter") {

        event.preventDefault();

        sendMessage();
    }
});