"""
Training Data Generator for Legal AI Out-of-Context Detection
This project belongs to SANDEEP REDDY K
"""

import json
import random
from typing import List, Dict

class LegalAIDataGenerator:
    def __init__(self):
        # Legal questions that should be answered
        self.legal_questions = [
            "What is the statute of limitations for personal injury cases?",
            "How do I file for divorce in my state?",
            "What are my rights as a tenant?",
            "Can I sue for breach of contract?",
            "What is the difference between civil and criminal law?",
            "How do I create a will?",
            "What constitutes workplace harassment?",
            "What are the requirements for filing bankruptcy?",
            "How do I obtain a restraining order?",
            "What is intellectual property law?",
            "Can I represent myself in court?",
            "What are the penalties for DUI?",
            "How do I copyright my work?",
            "What is the process for adoption?",
            "What are my Miranda rights?",
            "How do I start a small business legally?",
            "What is the difference between a felony and misdemeanor?",
            "Can I break my lease early?",
            "What is workers' compensation?",
            "How do I file a complaint against my lawyer?",
            "What is the legal age of consent?",
            "How do I get a patent for my invention?",
            "What are the laws regarding child custody?",
            "Can I record conversations legally?",
            "What is the process for expunging criminal records?",
            "How do I handle a car accident legally?",
            "What are the laws about employment discrimination?",
            "Can I sue for medical malpractice?",
            "What is the legal drinking age?",
            "How do I create a power of attorney?",
            "What are the requirements for marriage?",
            "Can I be fired without cause?",
            "What is the difference between murder and manslaughter?",
            "How do I protect my business name legally?",
            "What are the laws regarding online privacy?",
            "Can I refuse a breathalyzer test?",
            "What is the legal process for eviction?",
            "How do I handle identity theft legally?",
            "What are the laws about gun ownership?",
            "Can I sue for emotional distress?"
        ]
        
        # Out-of-context questions that should get "out of context" response
        self.out_of_context_questions = [
            "What's the weather like today?",
            "How do I cook pasta?",
            "What's the capital of France?",
            "How to lose weight fast?",
            "What's the best smartphone to buy?",
            "How do I fix my car engine?",
            "What's the meaning of life?",
            "How to learn Python programming?",
            "What's the best restaurant in town?",
            "How do I grow tomatoes?",
            "What's the latest movie release?",
            "How to play guitar?",
            "What's the score of the game?",
            "How do I bake a cake?",
            "What's the best vacation destination?",
            "How to exercise at home?",
            "What's the stock market doing?",
            "How do I learn a new language?",
            "What's the best coffee shop?",
            "How to meditate properly?",
            "What's the latest fashion trend?",
            "How do I train my dog?",
            "What's the best video game?",
            "How to improve my memory?",
            "What's the weather forecast?",
            "How do I clean my house?",
            "What's the best book to read?",
            "How to start a garden?",
            "What's the latest technology news?",
            "How do I learn to dance?",
            "What's the best way to travel?",
            "How to improve my photography?",
            "What's the healthiest diet?",
            "How do I learn math?",
            "What's the best music streaming service?",
            "How to improve my sleep?",
            "What's the latest sports news?",
            "How do I learn to swim?",
            "What's the best social media platform?",
            "How to improve my communication skills?"
        ]

    def generate_training_data(self, num_samples: int = 1000) -> List[Dict]:
        """Generate training data for fine-tuning"""
        training_data = []
        
        # Generate legal question samples
        for _ in range(num_samples // 2):
            question = random.choice(self.legal_questions)
            training_data.append({
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a legal AI assistant. Respond to legal questions with helpful information. If a question is not related to legal matters, respond with 'Out of context - I can only assist with legal-related questions.'"
                    },
                    {
                        "role": "user",
                        "content": question
                    },
                    {
                        "role": "assistant",
                        "content": f"This is a legal question about {self._categorize_legal_question(question)}. I can help you with this legal matter."
                    }
                ]
            })
        
        # Generate out-of-context question samples
        for _ in range(num_samples // 2):
            question = random.choice(self.out_of_context_questions)
            training_data.append({
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a legal AI assistant. Respond to legal questions with helpful information. If a question is not related to legal matters, respond with 'Out of context - I can only assist with legal-related questions.'"
                    },
                    {
                        "role": "user",
                        "content": question
                    },
                    {
                        "role": "assistant",
                        "content": "Out of context - I can only assist with legal-related questions."
                    }
                ]
            })
        
        # Shuffle the data
        random.shuffle(training_data)
        return training_data

    def _categorize_legal_question(self, question: str) -> str:
        """Categorize legal questions for better responses"""
        question_lower = question.lower()
        
        if any(word in question_lower for word in ['divorce', 'marriage', 'custody', 'adoption']):
            return "family law"
        elif any(word in question_lower for word in ['contract', 'breach', 'business', 'employment']):
            return "contract and business law"
        elif any(word in question_lower for word in ['criminal', 'dui', 'arrest', 'miranda', 'felony', 'misdemeanor']):
            return "criminal law"
        elif any(word in question_lower for word in ['property', 'tenant', 'lease', 'eviction']):
            return "property law"
        elif any(word in question_lower for word in ['copyright', 'patent', 'trademark', 'intellectual']):
            return "intellectual property law"
        elif any(word in question_lower for word in ['will', 'estate', 'inheritance', 'power of attorney']):
            return "estate planning"
        else:
            return "general legal matters"

    def save_training_data(self, filename: str = "legal_ai_training_data.jsonl"):
        """Save training data to JSONL format for Mistral AI fine-tuning"""
        training_data = self.generate_training_data(1000)
        
        with open(filename, 'w', encoding='utf-8') as f:
            for item in training_data:
                f.write(json.dumps(item) + '\n')
        
        print(f"Training data saved to {filename}")
        print(f"Total samples: {len(training_data)}")
        return filename

if __name__ == "__main__":
    generator = LegalAIDataGenerator()
    generator.save_training_data()
