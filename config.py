"""
Configuration file for Legal AI Application
This project belongs to SANDEEP REDDY K
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Mistral AI Configuration
MISTRAL_API_KEY = "vL4Dri1lEwWhU0frSLsaY0FAWvdGyFDl"
MISTRAL_FINE_TUNED_MODEL_ID = os.getenv('MISTRAL_FINE_TUNED_MODEL_ID', None)

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'legal_ai_db'
}

# Tesseract Configuration
TESSERACT_CMD = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Flask Configuration
SECRET_KEY = 'your_secret_key'
DEBUG = True
