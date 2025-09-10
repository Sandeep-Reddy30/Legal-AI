# This project belongs to SANDEEP REDDY K
from flask import Flask, render_template, request, jsonify, session
import pytesseract
from PIL import Image
import os
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import re
import mysql.connector
from datetime import datetime
import io
from mistral_integration import MistralLegalAI, FallbackLegalDetector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session handling

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Default XAMPP password is empty
    'database': 'legal_ai_db'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

def store_chat_interaction(question, response, user_id='anonymous'):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
        INSERT INTO chat_interactions (question, response, user_id)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (question, response, user_id))
        conn.commit()
    except Exception as e:
        print(f"Error storing chat interaction: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def store_legal_ai_interaction(question, response, is_legal_question, user_id='anonymous', model_used='mistral'):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
        INSERT INTO legal_ai_interactions (question, response, is_legal_question, user_id, model_used, created_at)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (question, response, is_legal_question, user_id, model_used, datetime.now()))
        conn.commit()
    except Exception as e:
        print(f"Error storing legal AI interaction: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

# Tesseract OCR configuration (update this path if necessary)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Initialize AI models
try:
    # Try to initialize Mistral AI (fine-tuned model)
    mistral_ai = MistralLegalAI()
    print("Mistral AI initialized successfully")
    use_mistral = True
except Exception as e:
    print(f"Failed to initialize Mistral AI: {e}")
    print("Falling back to keyword-based detection")
    fallback_detector = FallbackLegalDetector()
    use_mistral = False

# LangChain and model setup for general responses
model = OllamaLLM(model="llama3")

def extract_text_from_file(file):
    """Extract text from image files"""
    filename = file.filename.lower()
    
    if filename.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
        try:
            image = Image.open(file)
            return pytesseract.image_to_string(image)
        except Exception as e:
            print(f"Error reading image: {e}")
            return ""
    else:
        print(f"Unsupported file type: {filename}")
        return ""

def analyze_question_with_ai(question, context=""):
    """
    Analyze question using Mistral AI or fallback method
    
    Returns:
        dict: Contains response, is_legal_question, model_used, etc.
    """
    try:
        if use_mistral:
            return mistral_ai.is_question_legal_related(question, context)
        else:
            return fallback_detector.is_question_legal_related(question, context)
    except Exception as e:
        print(f"Error in AI analysis: {e}")
        # Ultimate fallback
        return {
            "response": "I apologize, but I'm experiencing technical difficulties. Please try again later.",
            "is_legal_question": False,
            "is_out_of_context": True,
            "model_used": "error_fallback",
            "error": str(e)
        }

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/legal_ai')
def legal_ai():
    return render_template('legal_ai.html')

@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    if request.method == 'POST':
        data = request.json
        question = data.get('question')
        
        if not question:
            return jsonify({'response': 'Please provide a question.'})

        result = model.invoke(question)
        
        # Store the chat interaction
        store_chat_interaction(question, result)
        
        return jsonify({'response': result})
    
    return render_template('chatbot.html')

@app.route('/upload_images', methods=['POST'])
def upload_images():
    if 'images' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    files = request.files.getlist('images')
    extracted_text = ""
    
    for file in files:
        if file and file.filename:
            extracted_text += extract_text_from_file(file) + "\n\n"
    
    if not extracted_text.strip():
        return jsonify({'error': 'No text could be extracted from the uploaded files. Please ensure you are uploading image files (PNG, JPG, JPEG, GIF, BMP).'}), 400
    
    session['context'] = extracted_text.strip()
    
    return jsonify({'context': session['context']})

@app.route('/ask_question', methods=['POST'])
def ask_question():
    data = request.json
    question = data.get('question')
    context = session.get('context', '')

    if not context:
        return jsonify({'response': 'Please upload an image first to extract content.'})

    # Use AI to analyze the question and generate response
    ai_result = analyze_question_with_ai(question, context)
    
    response = ai_result["response"]
    is_legal = ai_result["is_legal_question"]
    model_used = ai_result.get("model_used", "unknown")
    
    # If it's a legal question and we have context, enhance the response
    if is_legal and not ai_result["is_out_of_context"]:
        try:
            # Use Ollama for detailed legal analysis with context
            enhanced_prompt = f"""
            Based on the following legal document context, please provide a detailed and accurate response to the legal question.
            
            Context from document: {context}
            
            Question: {question}
            
            Please provide a comprehensive legal analysis based on the document context. If the document doesn't contain relevant information for the question, please state that clearly.
            """
            enhanced_response = model.invoke(enhanced_prompt)
            response = enhanced_response
        except Exception as e:
            print(f"Error getting enhanced response: {e}")
            # Keep the original Mistral response
    
    # Store the legal AI interaction with model information
    store_legal_ai_interaction(question, response, is_legal, model_used=model_used)
    
    return jsonify({
        'response': response,
        'is_legal_question': is_legal,
        'model_used': model_used
    })

@app.route('/test_mistral', methods=['GET'])
def test_mistral():
    """Test endpoint to verify Mistral AI functionality"""
    if not use_mistral:
        return jsonify({
            'status': 'error',
            'message': 'Mistral AI not available',
            'using_fallback': True
        })
    
    try:
        test_results = mistral_ai.test_model_performance()
        return jsonify({
            'status': 'success',
            'test_results': test_results,
            'model_id': mistral_ai.model_id
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

@app.route('/model_status', methods=['GET'])
def model_status():
    """Get current model status and configuration"""
    return jsonify({
        'mistral_available': use_mistral,
        'model_id': mistral_ai.model_id if use_mistral else None,
        'fallback_active': not use_mistral,
        'ollama_model': 'llama3'
    })

if __name__ == '__main__':
    app.run(debug=True)
# This project belongs to SANDEEP REDDY K
