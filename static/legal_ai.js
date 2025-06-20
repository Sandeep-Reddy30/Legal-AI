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
    document.getElementById('question').value = text;
    askQuestion();
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

document.getElementById('uploadForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    let formData = new FormData(this);
    let response = await fetch('/upload_images', {
        method: 'POST',
        body: formData
    });
    
    let data = await response.json();
    document.getElementById('context').value = data.context;
    document.getElementById('responseSection').style.display = 'block';
});

async function askQuestion() {
    let question = document.getElementById('question').value;
    let answerDiv = document.getElementById('answer');
    answerDiv.innerHTML = '<em>Typing...</em>';
    
    let response = await fetch('/ask_question', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: question })
    });
    
    let data = await response.json();
    answerDiv.innerText = data.response;
    speakText(data.response);
}
