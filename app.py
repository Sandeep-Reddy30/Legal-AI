from flask import Flask, render_template, request, jsonify, session
import pytesseract
from PIL import Image
import os
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session handling

# Tesseract OCR configuration (update this path if necessary)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# LangChain and model setup
model = OllamaLLM(model="llama3")

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/legal_ai')
def legal_ai():
    return render_template('legal_ai.html')

@app.route('/chatbot', methods=['GET', 'POST'])  # Supports GET and POST
def chatbot():
    if request.method == 'POST':
        data = request.json
        question = data.get('question')
        
        if not question:
            return jsonify({'response': 'Please provide a question.'})

        # Get the AI model's response directly for the question
        result = model.invoke(question)
        return jsonify({'response': result})
    
    return render_template('chatbot.html')#render converts web file to webpage

# Handle image upload and OCR
@app.route('/upload_images', methods=['POST'])
def upload_images():
    if 'images' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    files = request.files.getlist('images')
    extracted_text = ""
    
    for file in files:
        if file and file.filename:
            image = Image.open(file)
            extracted_text += pytesseract.image_to_string(image) + "\n\n"
    
    # Save extracted text in the session for future questions
    session['context'] = extracted_text.strip()
    
    return jsonify({'context': session['context']})#jsonify converts Python data (like dictionaries or lists) into JSON format and sends it as a proper HTTP response.

# Handle question-answering based on context
@app.route('/ask_question', methods=['POST'])
def ask_question():
    data = request.json
    question = data.get('question')
    context = session.get('context', '')

    if not context:
        return jsonify({'response': 'Please upload an image first to extract content.'})

    # Get the AI model's response using context and question
    result = model.invoke(f"Context: {context}\nQuestion: {question}")
    return jsonify({'response': result})

if __name__ == '__main__':
    app.run(debug=True)
