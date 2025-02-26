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
    
    let response = await fetch('/ask_question', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: question })
    });
    
    let data = await response.json();
    document.getElementById('answer').innerText = data.response;
}
