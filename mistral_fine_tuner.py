"""
Mistral AI Fine-tuning Pipeline for Legal AI Out-of-Context Detection
This project belongs to SANDEEP REDDY K
"""

import os
import json
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import time
from typing import List, Dict
import pandas as pd

class MistralFineTuner:
    def __init__(self, api_key: str = None):
        """
        Initialize Mistral Fine-tuner
        
        Args:
            api_key: Mistral AI API key. If None, will use default key
        """
        self.api_key = api_key or "vL4Dri1lEwWhU0frSLsaY0FAWvdGyFDl"
        
        self.client = MistralClient(api_key=self.api_key)
        self.fine_tuned_model_id = None

    def upload_training_data(self, file_path: str) -> str:
        """
        Upload training data file to Mistral AI
        
        Args:
            file_path: Path to the JSONL training data file
            
        Returns:
            file_id: ID of the uploaded file
        """
        try:
            print(f"Uploading training data from {file_path}...")
            
            with open(file_path, 'rb') as f:
                file_object = self.client.files.create(
                    file=f,
                    purpose="fine-tune"
                )
            
            print(f"Training data uploaded successfully. File ID: {file_object.id}")
            return file_object.id
            
        except Exception as e:
            print(f"Error uploading training data: {e}")
            raise

    def create_fine_tuning_job(self, file_id: str, model: str = "mistral-small-latest") -> str:
        """
        Create a fine-tuning job
        
        Args:
            file_id: ID of the uploaded training data file
            model: Base model to fine-tune (default: mistral-small-latest)
            
        Returns:
            job_id: ID of the fine-tuning job
        """
        try:
            print(f"Creating fine-tuning job with model {model}...")
            
            job = self.client.fine_tuning.jobs.create(
                model=model,
                training_files=[file_id],
                hyperparameters={
                    "training_steps": 100,
                    "learning_rate": 0.0001,
                }
            )
            
            print(f"Fine-tuning job created successfully. Job ID: {job.id}")
            return job.id
            
        except Exception as e:
            print(f"Error creating fine-tuning job: {e}")
            raise

    def monitor_fine_tuning_job(self, job_id: str, check_interval: int = 60) -> str:
        """
        Monitor fine-tuning job progress
        
        Args:
            job_id: ID of the fine-tuning job
            check_interval: Time in seconds between status checks
            
        Returns:
            model_id: ID of the fine-tuned model when completed
        """
        print(f"Monitoring fine-tuning job {job_id}...")
        
        while True:
            try:
                job = self.client.fine_tuning.jobs.retrieve(job_id)
                status = job.status
                
                print(f"Job status: {status}")
                
                if status == "succeeded":
                    self.fine_tuned_model_id = job.fine_tuned_model
                    print(f"Fine-tuning completed successfully! Model ID: {self.fine_tuned_model_id}")
                    return self.fine_tuned_model_id
                elif status == "failed":
                    print(f"Fine-tuning failed. Error: {job.error}")
                    raise Exception(f"Fine-tuning job failed: {job.error}")
                elif status in ["running", "queued"]:
                    print(f"Job is {status}. Checking again in {check_interval} seconds...")
                    time.sleep(check_interval)
                else:
                    print(f"Unknown status: {status}")
                    time.sleep(check_interval)
                    
            except Exception as e:
                print(f"Error checking job status: {e}")
                time.sleep(check_interval)

    def test_fine_tuned_model(self, model_id: str, test_questions: List[str]) -> List[Dict]:
        """
        Test the fine-tuned model with sample questions
        
        Args:
            model_id: ID of the fine-tuned model
            test_questions: List of test questions
            
        Returns:
            List of test results with questions and responses
        """
        results = []
        
        for question in test_questions:
            try:
                messages = [
                    ChatMessage(
                        role="system",
                        content="You are a legal AI assistant. Respond to legal questions with helpful information. If a question is not related to legal matters, respond with 'Out of context - I can only assist with legal-related questions.'"
                    ),
                    ChatMessage(role="user", content=question)
                ]
                
                response = self.client.chat(
                    model=model_id,
                    messages=messages,
                    max_tokens=150
                )
                
                result = {
                    "question": question,
                    "response": response.choices[0].message.content,
                    "is_out_of_context": "out of context" in response.choices[0].message.content.lower()
                }
                results.append(result)
                
                print(f"Q: {question}")
                print(f"A: {response.choices[0].message.content}")
                print("-" * 50)
                
            except Exception as e:
                print(f"Error testing question '{question}': {e}")
                results.append({
                    "question": question,
                    "response": f"Error: {e}",
                    "is_out_of_context": False
                })
        
        return results

    def run_complete_fine_tuning_pipeline(self, training_file_path: str) -> str:
        """
        Run the complete fine-tuning pipeline
        
        Args:
            training_file_path: Path to the training data file
            
        Returns:
            model_id: ID of the fine-tuned model
        """
        print("Starting complete fine-tuning pipeline...")
        
        # Step 1: Upload training data
        file_id = self.upload_training_data(training_file_path)
        
        # Step 2: Create fine-tuning job
        job_id = self.create_fine_tuning_job(file_id)
        
        # Step 3: Monitor job progress
        model_id = self.monitor_fine_tuning_job(job_id)
        
        # Step 4: Test the model
        test_questions = [
            "What is the statute of limitations for personal injury?",  # Legal
            "How do I cook pasta?",  # Out of context
            "Can I sue for breach of contract?",  # Legal
            "What's the weather like today?",  # Out of context
            "What are my Miranda rights?",  # Legal
            "How to lose weight fast?"  # Out of context
        ]
        
        print("\nTesting fine-tuned model...")
        results = self.test_fine_tuned_model(model_id, test_questions)
        
        # Save test results
        results_df = pd.DataFrame(results)
        results_df.to_csv('fine_tuning_test_results.csv', index=False)
        print("Test results saved to fine_tuning_test_results.csv")
        
        return model_id

def main():
    """Main function to demonstrate fine-tuning process"""
    print("Mistral AI Fine-tuning for Legal AI")
    print("=" * 50)
    
    # Check if API key is available
    api_key = os.getenv('MISTRAL_API_KEY')
    if not api_key:
        print("Please set your MISTRAL_API_KEY environment variable")
        print("You can get an API key from: https://console.mistral.ai/")
        return
    
    try:
        # Initialize fine-tuner
        fine_tuner = MistralFineTuner(api_key)
        
        # Check if training data exists
        training_file = "legal_ai_training_data.jsonl"
        if not os.path.exists(training_file):
            print(f"Training data file {training_file} not found.")
            print("Please run training_data_generator.py first to generate training data.")
            return
        
        # Run fine-tuning pipeline
        model_id = fine_tuner.run_complete_fine_tuning_pipeline(training_file)
        
        print(f"\nFine-tuning completed successfully!")
        print(f"Fine-tuned model ID: {model_id}")
        print("You can now use this model in your application.")
        
    except Exception as e:
        print(f"Error in fine-tuning process: {e}")

if __name__ == "__main__":
    main()
