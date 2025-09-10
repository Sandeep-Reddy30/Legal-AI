"""
Mistral AI Integration for Legal AI Application
This project belongs to SANDEEP REDDY K
"""

import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from typing import Optional, Dict

class MistralLegalAI:
    def __init__(self, api_key: str = None, model_id: str = None):
        """
        Initialize Mistral Legal AI client
        
        Args:
            api_key: Mistral AI API key
            model_id: Fine-tuned model ID (if None, uses base model)
        """
        self.api_key = api_key or "vL4Dri1lEwWhU0frSLsaY0FAWvdGyFDl"
        
        self.client = MistralClient(api_key=self.api_key)
        self.model_id = model_id or os.getenv('MISTRAL_FINE_TUNED_MODEL_ID') or "mistral-small-latest"
        
        # System prompt for legal AI
        self.system_prompt = """You are a legal AI assistant specialized in providing accurate legal information. 

IMPORTANT INSTRUCTIONS:
1. If a question is related to legal matters (laws, legal procedures, court cases, legal rights, etc.), provide helpful and accurate legal information.
2. If a question is NOT related to legal matters, respond EXACTLY with: "Out of context - I can only assist with legal-related questions."
3. Do not provide legal advice, only legal information.
4. Always recommend consulting with a qualified attorney for specific legal advice.

Legal topics include but are not limited to:
- Laws and regulations
- Court procedures
- Legal rights and obligations  
- Contract law
- Criminal law
- Civil law
- Family law
- Property law
- Employment law
- Intellectual property
- Estate planning
- Business law
- Constitutional law"""

    def is_question_legal_related(self, question: str, context: str = "") -> Dict:
        """
        Use Mistral AI to determine if a question is legal-related and generate response
        
        Args:
            question: User's question
            context: Additional context (e.g., from OCR)
            
        Returns:
            Dictionary with response and metadata
        """
        try:
            # Prepare the full prompt
            if context:
                full_question = f"Context: {context}\n\nQuestion: {question}"
            else:
                full_question = question
            
            messages = [
                ChatMessage(role="system", content=self.system_prompt),
                ChatMessage(role="user", content=full_question)
            ]
            
            # Get response from Mistral
            response = self.client.chat(
                model=self.model_id,
                messages=messages,
                max_tokens=500,
                temperature=0.1  # Low temperature for consistent responses
            )
            
            response_text = response.choices[0].message.content
            
            # Check if response indicates out of context
            is_out_of_context = "out of context" in response_text.lower()
            
            return {
                "response": response_text,
                "is_legal_question": not is_out_of_context,
                "is_out_of_context": is_out_of_context,
                "model_used": self.model_id,
                "tokens_used": response.usage.total_tokens if hasattr(response, 'usage') else None
            }
            
        except Exception as e:
            print(f"Error with Mistral AI: {e}")
            # Fallback response
            return {
                "response": "I apologize, but I'm experiencing technical difficulties. Please try again later.",
                "is_legal_question": False,
                "is_out_of_context": True,
                "model_used": "fallback",
                "error": str(e)
            }

    def test_model_performance(self) -> Dict:
        """Test the model with sample questions"""
        test_questions = [
            # Legal questions
            "What is the statute of limitations for personal injury?",
            "How do I file for divorce?",
            "What are my Miranda rights?",
            
            # Non-legal questions  
            "What's the weather today?",
            "How do I cook pasta?",
            "What's the capital of France?"
        ]
        
        results = []
        for question in test_questions:
            result = self.is_question_legal_related(question)
            results.append({
                "question": question,
                "response": result["response"],
                "is_out_of_context": result["is_out_of_context"]
            })
        
        return {
            "test_results": results,
            "model_id": self.model_id
        }

# Fallback legal detection (keyword-based) for when Mistral is unavailable
class FallbackLegalDetector:
    def __init__(self):
        self.legal_keywords = [
            'law', 'legal', 'court', 'judge', 'lawyer', 'attorney', 'case', 'trial', 'evidence',
            'witness', 'plaintiff', 'defendant', 'prosecution', 'defense', 'verdict', 'sentence',
            'jurisdiction', 'statute', 'regulation', 'constitution', 'contract', 'agreement',
            'litigation', 'appeal', 'petition', 'motion', 'hearing', 'testimony', 'deposition',
            'subpoena', 'warrant', 'bail', 'parole', 'probation', 'criminal', 'civil', 'family',
            'property', 'intellectual', 'copyright', 'patent', 'trademark', 'tax', 'immigration',
            'employment', 'labor', 'corporate', 'business', 'bankruptcy', 'estate', 'trust',
            'will', 'inheritance', 'divorce', 'custody', 'adoption', 'marriage', 'domestic',
            'violence', 'abuse', 'harassment', 'discrimination', 'rights', 'freedom', 'justice'
        ]

    def is_question_legal_related(self, question: str, context: str = "") -> Dict:
        """Fallback method using keyword matching"""
        full_text = f"{question} {context}".lower()
        
        is_legal = any(keyword in full_text for keyword in self.legal_keywords)
        
        if is_legal:
            response = "This appears to be a legal question. I can help you with legal matters, but please consult with a qualified attorney for specific legal advice."
        else:
            response = "Out of context - I can only assist with legal-related questions."
        
        return {
            "response": response,
            "is_legal_question": is_legal,
            "is_out_of_context": not is_legal,
            "model_used": "fallback_keyword_matching"
        }
