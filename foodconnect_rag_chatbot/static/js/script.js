async function sendMessage() {
  const input = document.getElementById("user-input");
  const chatBox = document.getElementById("chat-box");

  const userText = input.value.trim();
  if (!userText) return;

  // Display user message
  chatBox.innerHTML += `<div class='user-msg'>You: ${userText}</div>`;
  input.value = "";

  // Send to backend
  const response = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question: userText })
  });

  const data = await response.json();
  const botText = data.answer || "Sorry, something went wrong.";

  // Display bot reply
  chatBox.innerHTML += `<div class='bot-msg'>Bot: ${botText}</div>`;
  chatBox.scrollTop = chatBox.scrollHeight;
}


