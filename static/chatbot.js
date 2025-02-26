async function sendMessage() {
    let userMessage = document.getElementById('userInput').value;
    
    let response = await fetch('/chatbot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: userMessage })
    });
    
    let data = await response.json();
    let chatWindow = document.getElementById('chatWindow');
    
    chatWindow.innerHTML += `<p><strong>You:</strong> ${userMessage}</p>`;
    chatWindow.innerHTML += `<p><strong>Bot:</strong> ${data.response}</p>`;
    
    // Scroll to the bottom after new messages
    chatWindow.scrollTop = chatWindow.scrollHeight;
}
