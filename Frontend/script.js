const chat = document.getElementById("chat");
const messageInput = document.getElementById("message");
const sendButton = document.getElementById("sendButton");


// ============================================================
// USER ID
// ============================================================

function getUserId() {

    let userId = localStorage.getItem("careerGuideUserId");

    if (!userId) {

        userId = crypto.randomUUID();

        localStorage.setItem(
            "careerGuideUserId",
            userId
        );
    }

    return userId;
}


const userId = getUserId();


// ============================================================
// ADD MESSAGE
// ============================================================

function addMessage(text, sender) {

    const message = document.createElement("div");

    message.className = `message ${sender}`;


    const content = document.createElement("div");

    content.className = "message-content";

    content.textContent = text;


    message.appendChild(content);

    chat.appendChild(message);


    chat.scrollTop = chat.scrollHeight;
}


// ============================================================
// SEND MESSAGE
// ============================================================

async function sendMessage() {

    const message = messageInput.value.trim();


    if (!message) {
        return;
    }


    addMessage(
        message,
        "user"
    );


    messageInput.value = "";

    sendButton.disabled = true;


    addMessage(
        "Thinking...",
        "ai"
    );


    const thinkingMessage =
        chat.lastElementChild;


    try {

        const response = await fetch(
            "/chat",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    message: message,

                    user_id: userId

                })
            }
        );


        const data = await response.json();


        thinkingMessage.remove();


        addMessage(
            data.response,
            "ai"
        );

    }


    catch (error) {

        thinkingMessage.remove();


        addMessage(
            "Sorry, I couldn't connect to CareerGuide AI.",
            "ai"
        );


        console.error(error);

    }


    sendButton.disabled = false;

    messageInput.focus();
}


// ============================================================
// SUGGESTION BUTTONS
// ============================================================

function sendSuggestion(text) {

    messageInput.value = text;

    sendMessage();

}


// ============================================================
// ENTER KEY
// ============================================================

messageInput.addEventListener(
    "keydown",
    function(event) {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            sendMessage();

        }

    }
);