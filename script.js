
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
// Suggested Questions Functionality

const suggestionButtons = document.querySelectorAll(".suggestion-btn");

suggestionButtons.forEach((button) => {

    button.addEventListener("click", function () {

        const question = this.dataset.question;

        userInput.value = question;

        sendMessage();

    });

});


userInput.addEventListener("keydown", function(event) {

    if (event.key === "Enter") {
        sendMessage();
    }

});
 // SHARE YOUR MITHILA STORY - SUPABASE INTEGRATION

const STORY_API_URL = "http://127.0.0.1:8000/submit-story";

const storyForm = document.getElementById("storyForm");

if (storyForm) {

    storyForm.addEventListener("submit", async function (event) {

        event.preventDefault();

        const name = document.getElementById("storyName").value.trim();
        const location = document.getElementById("storyLocation").value.trim();
        const category = document.getElementById("storyCategory").value;
        const message = document.getElementById("storyMessage").value.trim();

        const storyStatus = document.getElementById("storyStatus");
        const submitButton = storyForm.querySelector(".story-submit-btn");

        const storyData = {
            name: name,
            location: location,
            category: category,
            message: message
        };

        try {

            submitButton.disabled = true;
            submitButton.textContent = "Submitting...";
            storyStatus.textContent = "Sending your story...";

            const response = await fetch(STORY_API_URL, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(storyData)
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || "Submission failed");
            }

            storyStatus.textContent =
                "Thank you! Your Mithila story has been submitted successfully.";

            storyStatus.style.color = "#38845b";

            storyForm.reset();

        } catch (error) {

            console.error("Story submission error:", error);

            storyStatus.textContent =
                "Unable to submit your story. Please try again.";

            storyStatus.style.color = "#d14343";

        } finally {

            submitButton.disabled = false;
            submitButton.textContent = "Share My Story →";

        }

    });

}
// =====================================
// GIVE FEEDBACK FORM
// =====================================

const feedbackForm = document.getElementById("feedbackForm");
const feedbackStatus = document.getElementById("feedbackStatus");
const feedbackSubmitBtn = feedbackForm
    ? feedbackForm.querySelector(".feedback-submit-btn")
    : null;

if (feedbackForm) {

    feedbackForm.addEventListener("submit", async function (event) {

        // Prevent page refresh
        event.preventDefault();

        // Get selected rating
        const selectedRating = document.querySelector(
            'input[name="feedbackRating"]:checked'
        );

        if (!selectedRating) {
            feedbackStatus.textContent = "Please select a rating.";
            feedbackStatus.style.color = "red";
            return;
        }

        // Prepare feedback data
        const feedbackData = {
            name: document.getElementById("feedbackName").value.trim() || "Anonymous",
            rating: Number(selectedRating.value),
            message: document.getElementById("feedbackMessage").value.trim()
        };

        // Check message
        if (!feedbackData.message) {
            feedbackStatus.textContent = "Please write your feedback.";
            feedbackStatus.style.color = "red";
            return;
        }

        // Disable button while submitting
        feedbackSubmitBtn.disabled = true;
        feedbackSubmitBtn.textContent = "Submitting...";

        feedbackStatus.textContent = "Submitting your feedback...";
        feedbackStatus.style.color = "#555";

        try {

            // Send feedback to FastAPI backend
            const response = await fetch(
                "http://127.0.0.1:8000/submit-feedback",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(feedbackData)
                }
            );

            const result = await response.json();

            if (!response.ok) {
                throw new Error(
                    result.detail || "Unable to submit feedback."
                );
            }

            // Success message
            feedbackStatus.textContent =
                "Thank you for your feedback! ❤️";

            feedbackStatus.style.color = "green";

            // Reset form
            feedbackForm.reset();

        } catch (error) {

            console.error("Feedback Error:", error);

            feedbackStatus.textContent =
                error.message || "Something went wrong. Please try again.";

            feedbackStatus.style.color = "red";

        } finally {

            // Enable button again
            feedbackSubmitBtn.disabled = false;
            feedbackSubmitBtn.textContent = "Submit Feedback →";

        }

    });

}