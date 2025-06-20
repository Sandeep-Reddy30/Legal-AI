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

def store_legal_ai_interaction(question, response, is_legal_question, user_id='anonymous'):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
        INSERT INTO legal_ai_interactions (question, response, is_legal_question, user_id)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (question, response, is_legal_question, user_id))
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

# LangChain and model setup
model = OllamaLLM(model="llama3")

# Legal domain keywords and patterns
LEGAL_KEYWORDS = [
    'law', 'legal', 'court', 'judge', 'lawyer', 'attorney', 'case', 'trial', 'evidence',
    'witness', 'plaintiff', 'defendant', 'prosecution', 'defense', 'verdict', 'sentence',
    'jurisdiction', 'statute', 'regulation', 'constitution', 'contract', 'agreement',
    'litigation', 'appeal', 'petition', 'motion', 'hearing', 'testimony', 'deposition',
    'subpoena', 'warrant', 'bail', 'parole', 'probation', 'criminal', 'civil', 'family',
    'property', 'intellectual', 'copyright', 'patent', 'trademark', 'tax', 'immigration',
    'employment', 'labor', 'corporate', 'business', 'bankruptcy', 'estate', 'trust',
    'will', 'inheritance', 'divorce', 'custody', 'adoption', 'marriage', 'domestic',
    'violence', 'abuse', 'harassment', 'discrimination', 'rights', 'freedom', 'justice',
    'equity', 'fairness', 'due process', 'habeas corpus', 'precedent', 'jurisprudence',
    'legislation', 'bill', 'act', 'code', 'ordinance', 'regulation', 'policy', 'procedure',
    'rule', 'standard', 'guideline', 'directive', 'order', 'decree', 'judgment', 'ruling',
    'opinion', 'brief', 'argument', 'pleading', 'complaint', 'indictment', 'charge',
    'offense', 'crime', 'felony', 'misdemeanor', 'infraction', 'violation', 'penalty',
    'punishment', 'fine', 'imprisonment', 'probation', 'parole', 'restitution',
    'compensation', 'damages', 'injunction', 'remedy', 'relief', 'settlement',
    'mediation', 'arbitration', 'negotiation', 'resolution', 'dispute', 'conflict',
    'controversy', 'matter', 'issue', 'question', 'concern', 'problem', 'situation',
    'circumstance', 'condition', 'state', 'status', 'position', 'standing', 'capacity',
    'authority', 'power', 'right', 'privilege', 'immunity', 'exemption', 'exception',
    'exclusion', 'limitation', 'restriction', 'condition', 'requirement', 'obligation',
    'duty', 'responsibility', 'liability', 'accountability', 'culpability', 'guilt',
    'innocence', 'conviction', 'acquittal', 'dismissal', 'withdrawal', 'abandonment',
    'termination', 'conclusion', 'finality', 'res judicata', 'stare decisis'
]

def is_legal_question(question):
    # Convert question to lowercase for case-insensitive matching
    question_lower = question.lower()
    
    # Check if any legal keyword is present in the question
    for keyword in LEGAL_KEYWORDS:
        if keyword in question_lower:
            return True
    
    # Check for common legal question patterns
    legal_patterns = [
        r'what is the law',
        r'legal advice',
        r'court case',
        r'legal rights',
        r'legal obligation',
        r'legal requirement',
        r'legal procedure',
        r'legal process',
        r'legal action',
        r'legal matter',
        r'legal issue',
        r'legal problem',
        r'legal situation',
        r'legal status',
        r'legal position',
        r'legal standing',
        r'legal capacity',
        r'legal authority',
        r'legal power',
        r'legal right',
        r'legal privilege',
        r'legal immunity',
        r'legal exemption',
        r'legal exception',
        r'legal limitation',
        r'legal restriction',
        r'legal condition',
        r'legal requirement',
        r'legal obligation',
        r'legal duty',
        r'legal responsibility',
        r'legal liability',
        r'legal accountability',
        r'legal culpability',
        r'legal guilt',
        r'legal innocence',
        r'legal conviction',
        r'legal acquittal',
        r'legal dismissal',
        r'legal withdrawal',
        r'legal abandonment',
        r'legal termination',
        r'legal conclusion',
        r'legal finality'
    ]
    
    for pattern in legal_patterns:
        if re.search(pattern, question_lower):
            return True
    
    return False

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

    is_legal = is_legal_question(question)
    
    if not is_legal:
        response = "I apologize, but I can only assist with legal-related questions. Please ask about laws, legal procedures, court cases, or other legal matters. For example, you can ask about specific laws, legal rights, court procedures, or legal implications of certain situations."
    else:
        # Get the AI model's response using context and question
        response = model.invoke(f"Context: {context}\nQuestion: {question}")
    
    # Store the legal AI interaction
    store_legal_ai_interaction(question, response, is_legal_question=is_legal)
    
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
