// Voice recognition setup
const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.continuous = false;
recognition.lang = 'en-US';

// Speech synthesis setup
const synth = window.speechSynthesis;

let isListening = false;

function startVoiceInput() {
    const voiceBtn = document.getElementById('voiceBtn');
    if (!isListening) {
        recognition.start();
        isListening = true;
        voiceBtn.classList.add('listening');
        voiceBtn.innerHTML = '<i class="fas fa-stop"></i>';
    } else {
        recognition.stop();
        isListening = false;
        voiceBtn.classList.remove('listening');
        voiceBtn.innerHTML = '<i class="fas fa-microphone"></i>';
    }
}

recognition.onresult = function(event) {
    const text = event.results[0][0].transcript;
    document.getElementById('userInput').value = text;
    sendMessage();
};

recognition.onend = function() {
    isListening = false;
    const voiceBtn = document.getElementById('voiceBtn');
    voiceBtn.classList.remove('listening');
    voiceBtn.innerHTML = '<i class="fas fa-microphone"></i>';
};

function speakText(text) {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1.0;
    utterance.pitch = 1.0;
    synth.speak(utterance);
}

async function sendMessage() {
    let userInput = document.getElementById('userInput');
    let userMessage = userInput.value.trim();
    if (!userMessage) return;
    let chatWindow = document.getElementById('chatWindow');

    // Show user's message immediately
    chatWindow.innerHTML += `<p><strong>You:</strong> ${userMessage}</p>`;
    // Show typing indicator
    const typingId = `typing-${Date.now()}`;
    chatWindow.innerHTML += `<p id="${typingId}"><strong>Bot:</strong> <em>Typing...</em></p>`;
    chatWindow.scrollTop = chatWindow.scrollHeight;
    userInput.value = '';

    let response = await fetch('/chatbot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: userMessage })
    });
    let data = await response.json();

    // Replace typing indicator with actual response
    let typingElem = document.getElementById(typingId);
    if (typingElem) {
        typingElem.innerHTML = `<strong>Bot:</strong> ${data.response}`;
        // Speak the response
        speakText(data.response);
    }
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

document.getElementById('userInput').addEventListener('keydown', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

