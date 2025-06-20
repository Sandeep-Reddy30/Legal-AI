# Legal AI Web Application

This project is a web-based Legal AI assistant designed especially for lawyers and legal professionals. It leverages OCR and advanced LLMs to **summarize and answer legal questions based on uploaded images of legal documents**. The system uses Flask for the backend, Tesseract for OCR, and integrates with **Ollama Llama-3** and **Retrieval-Augmented Generation (RAG)** for highly relevant, context-aware legal responses.

## Features
- **Summarize legal documents**: Upload images (PNG, JPG, JPEG, GIF, BMP) and extract text using OCR, then receive concise summaries and answers.
- **Lawyer-focused Q&A**: Ask legal questions based on the extracted text context—ideal for lawyers needing quick insights or case preparation.
- **RAG-powered responses**: Uses Retrieval-Augmented Generation (RAG) to ground answers in the uploaded document content, increasing accuracy and relevance.
- **Ollama Llama-3 integration**: Utilizes the powerful Llama-3 model via Ollama for natural language understanding and generation.
- AI-powered chatbot for general and legal queries
- Stores chat and legal interactions in a MySQL database
- Simple web interface (Flask + HTML/JS/CSS)

## Directory Structure
- `app.py` - Main Flask application
- `templates/` - HTML templates (home, chatbot, legal AI)
- `static/` - Static assets (CSS, JS)
- `uploads/` - Directory for uploaded images

## Setup Instructions

### 1. Clone the repository
```bash
git clone <repo-url>
cd legal-ai
```

### 2. Create and activate a virtual environment (optional but recommended)
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Unix/Mac:
source venv/bin/activate
```

### 3. Install dependencies
Install the following Python packages:
- Flask
- pytesseract
- pillow
- langchain_ollama
- langchain_core
- mysql-connector-python

Example:
```bash
pip install Flask pytesseract pillow langchain_ollama langchain_core mysql-connector-python
```

### 4. Install Tesseract OCR
- Download and install Tesseract from [here](https://github.com/tesseract-ocr/tesseract).
- Update the path in `app.py` if your installation is in a different location:
  ```python
  pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
  ```

### 5. Set up MySQL Database
- Create a database named `legal_ai_db` and the following tables:

```sql
CREATE TABLE chat_interactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question TEXT,
    response TEXT,
    user_id VARCHAR(255),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE legal_ai_interactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question TEXT,
    response TEXT,
    is_legal_question BOOLEAN,
    user_id VARCHAR(255),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
- Update the database credentials in `app.py` if needed.

### 6. Run the Application
```bash
python app.py
```
Visit [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser.

## Usage
- Go to the home page and navigate to the Legal AI section.
- Upload images of legal documents.
- Receive summaries and ask questions about the content of the uploaded images.
- Use the chatbot for general or legal queries.

## Technical Details
- **Ollama Llama-3**: The application uses the Llama-3 model via Ollama for advanced legal language understanding and generation.
- **Retrieval-Augmented Generation (RAG)**: Answers are generated using RAG, which grounds responses in the actual content of uploaded documents, making them more accurate and context-aware.
- **For Lawyers**: This tool is especially useful for lawyers to quickly summarize, review, and query legal documents, saving time and improving productivity.

## Notes
- This project is for educational/demo purposes and should not be used for real legal advice.
- Make sure Tesseract OCR and MySQL are running.
- The AI model is set to use `llama3` via Ollama; you may need to adjust this for your environment.

## License
MIT License (add your license here) 