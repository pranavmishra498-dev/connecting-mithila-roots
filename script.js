
const API_URL = "http://127.0.0.1:8000/chat";

const chatMessages = document.getElementById("chatMessages");
const userInput = document.getElementById("userInput");
const sendButton = document.getElementById("sendButton");
const chatStatus = document.getElementById("chatStatus");


function addMessage(message, sender) {

    const messageDiv = document.createElement("div");

    messageDiv.classList.add(
        sender === "user" ? "user-message" : "bot-message"
    );

    messageDiv.textContent = message;

    chatMessages.appendChild(messageDiv);

    chatMessages.scrollTop = chatMessages.scrollHeight;
}
function addProductCard(product) {

    if (!product) return;

    const card = document.createElement("div");
    card.classList.add("product-card");

    const title = document.createElement("h3");
    title.textContent = product.name;

    const description = document.createElement("p");
    description.textContent = product.description;

    card.appendChild(title);
    card.appendChild(description);

    if (product.url) {
        const link = document.createElement("a");

        link.href = product.url;
        link.target = "_blank";
        link.rel = "noopener noreferrer";
        link.textContent = "Explore Product";
        link.classList.add("product-button");

        card.appendChild(link);
    } else {
        const message = document.createElement("p");
        message.textContent = "Link Coming Soon";

        card.appendChild(message);
    }

    chatMessages.appendChild(card);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function sendMessage() {

    const question = userInput.value.trim();

    if (!question) return;

    addMessage(question, "user");

    userInput.value = "";
    sendButton.disabled = true;
    chatStatus.textContent = "Mithila AI is thinking...";

    try {

        const response = await fetch(API_URL, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question
            })

        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Request failed");
        }

        addMessage(data.answer, "bot");
        addProductCard(data.recommendation); 
        chatStatus.textContent = "";

    } catch (error) {

        console.error(error);

        addMessage(
            "Sorry, something went wrong. Please try again.",
            "bot"
        );

        chatStatus.textContent =
            "Connection error. Check your backend.";

    } finally {

        sendButton.disabled = false;
        userInput.focus();

    }
}


sendButton.addEventListener("click", sendMessage);


userInput.addEventListener("keydown", function(event) {

    if (event.key === "Enter") {
        sendMessage();
    }

});
