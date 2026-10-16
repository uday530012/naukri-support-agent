const input = document.getElementById("message-input");
const sendButton = document.getElementById("send-button");
const chatContainer = document.getElementById("chat-container");


// ============================================================
// SEND MESSAGE
// ============================================================

async function sendMessage() {

    const message = input.value.trim();

    if (!message) {
        return;
    }


    // Show user message

    addMessage(
        message,
        "user"
    );


    // Clear input

    input.value = "";


    // Disable button

    sendButton.disabled = true;
    sendButton.textContent = "Sending...";


    // Show temporary loading message

    const loadingMessage = addMessage(
        "Thinking...",
        "assistant"
    );


    try {

        const response = await fetch(
            "http://127.0.0.1:8000/chat",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    message: message
                })
            }
        );


        if (!response.ok) {

            throw new Error(
                "Server returned an error."
            );

        }


        const data = await response.json();


        // Remove loading message

        loadingMessage.remove();


        // Display response

        addAgentResponse(data);


    } catch (error) {

        loadingMessage.remove();

        addMessage(
            "Sorry, I could not connect to the support agent.",
            "assistant"
        );

        console.error(error);

    }


    // Enable button

    sendButton.disabled = false;
    sendButton.textContent = "Send";

}


// ============================================================
// ADD NORMAL MESSAGE
// ============================================================

function addMessage(message, sender) {

    const messageDiv =
        document.createElement("div");

    messageDiv.className =
        `message ${sender}`;


    if (sender === "assistant") {

        messageDiv.innerHTML = `

            <div class="avatar">
                🤖
            </div>

            <div class="message-content">

                <div class="message-name">
                    Naukri Assistant
                </div>

                <div class="message-bubble">
                    ${escapeHtml(message)}
                </div>

            </div>

        `;

    } else {

        messageDiv.innerHTML = `

            <div class="message-content">

                <div class="message-name">
                    You
                </div>

                <div class="message-bubble">
                    ${escapeHtml(message)}
                </div>

            </div>

        `;

    }


    chatContainer.appendChild(messageDiv);

    scrollToBottom();

    return messageDiv;
}


// ============================================================
// ADD AGENT RESPONSE
// ============================================================

function addAgentResponse(data) {

    const messageDiv =
        document.createElement("div");

    messageDiv.className =
        "message assistant";


    const response =
        data.response || "No response received.";


    const source =
        data.source || "";


    const nextAction =
        data.next_action || "";


    messageDiv.innerHTML = `

        <div class="avatar">
            🤖
        </div>

        <div class="message-content">

            <div class="message-name">
                Naukri Assistant
            </div>

            <div class="message-bubble">

                ${escapeHtml(response)}

                ${
                    source
                    ? `<br><br>
                       <small>
                       Source: ${escapeHtml(source)}
                       </small>`
                    : ""
                }

                ${
                    nextAction
                    ? `<br><br>
                       <strong>
                       Next Action:
                       </strong>
                       ${escapeHtml(nextAction)}`
                    : ""
                }

            </div>

        </div>

    `;


    chatContainer.appendChild(messageDiv);

    scrollToBottom();
}


// ============================================================
// ENTER KEY
// ============================================================

input.addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Enter") {

            sendMessage();

        }

    }
);


// ============================================================
// SCROLL
// ============================================================

function scrollToBottom() {

    chatContainer.scrollTop =
        chatContainer.scrollHeight;

}


// ============================================================
// BASIC HTML ESCAPE
// ============================================================

function escapeHtml(text) {

    const div =
        document.createElement("div");

    div.textContent = text;

    return div.innerHTML;

}