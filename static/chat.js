const chatForm = document.getElementById("chatForm");
const chatInput = document.getElementById("chatInput");
const chatMessages = document.getElementById("chatMessages");

function addMessage(text, className) {
    const message = document.createElement("div");
    message.className = className;
    message.textContent = text;
    chatMessages.appendChild(message);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

if (chatForm) {
    chatForm.addEventListener("submit", async function (event) {
        event.preventDefault();
        const text = chatInput.value.trim();

        if (!text) {
            return;
        }

        addMessage(text, "user-message");
        chatInput.value = "";
        addMessage("Thinking...", "bot-message loading");

        const response = await fetch("/chat", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({message: text})
        });

        const data = await response.json();
        const loading = document.querySelector(".loading");

        if (loading) {
            loading.remove();
        }

        addMessage(data.reply, "bot-message");
    });
}
