"""
Model Evaluation System for Legal AI Out-of-Context Detection
This project belongs to SANDEEP REDDY K
"""

import json
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from typing import List, Dict, Tuple
import matplotlib.pyplot as plt
import seaborn as sns

class LegalAIEvaluator:
    def __init__(self):
        self.test_cases = self._create_test_cases()

    def _create_test_cases(self) -> List[Dict]:
        """Create comprehensive test cases for evaluation"""
        return [
            # Legal questions (should NOT be out of context)
            {"question": "What is the statute of limitations for personal injury cases?", "expected_out_of_context": False},
            {"question": "How do I file for divorce in California?", "expected_out_of_context": False},
            {"question": "What are my rights as a tenant?", "expected_out_of_context": False},
            {"question": "Can I sue for breach of contract?", "expected_out_of_context": False},
            {"question": "What constitutes workplace harassment?", "expected_out_of_context": False},
            {"question": "How do I create a will?", "expected_out_of_context": False},
            {"question": "What are the penalties for DUI?", "expected_out_of_context": False},
            {"question": "How do I copyright my work?", "expected_out_of_context": False},
            {"question": "What is intellectual property law?", "expected_out_of_context": False},
            {"question": "Can I represent myself in court?", "expected_out_of_context": False},
            {"question": "What are my Miranda rights?", "expected_out_of_context": False},
            {"question": "How do I file for bankruptcy?", "expected_out_of_context": False},
            {"question": "What is the difference between civil and criminal law?", "expected_out_of_context": False},
            {"question": "How do I obtain a restraining order?", "expected_out_of_context": False},
            {"question": "What are the laws regarding child custody?", "expected_out_of_context": False},
            
            # Out-of-context questions (should be out of context)
            {"question": "What's the weather like today?", "expected_out_of_context": True},
            {"question": "How do I cook pasta?", "expected_out_of_context": True},
            {"question": "What's the capital of France?", "expected_out_of_context": True},
            {"question": "How to lose weight fast?", "expected_out_of_context": True},
            {"question": "What's the best smartphone to buy?", "expected_out_of_context": True},
            {"question": "How do I fix my car engine?", "expected_out_of_context": True},
            {"question": "What's the meaning of life?", "expected_out_of_context": True},
            {"question": "How to learn Python programming?", "expected_out_of_context": True},
            {"question": "What's the best restaurant in town?", "expected_out_of_context": True},
            {"question": "How do I grow tomatoes?", "expected_out_of_context": True},
            {"question": "What's the latest movie release?", "expected_out_of_context": True},
            {"question": "How to play guitar?", "expected_out_of_context": True},
            {"question": "What's the score of the game?", "expected_out_of_context": True},
            {"question": "How do I bake a cake?", "expected_out_of_context": True},
            {"question": "What's the best vacation destination?", "expected_out_of_context": True},
            
            # Edge cases - legal-sounding but not really legal
            {"question": "What's the law of gravity?", "expected_out_of_context": True},
            {"question": "What are the laws of thermodynamics?", "expected_out_of_context": True},
            {"question": "What's Murphy's law?", "expected_out_of_context": True},
            
            # Borderline cases - could be interpreted either way
            {"question": "What are the legal requirements for starting a food truck?", "expected_out_of_context": False},
            {"question": "Are there legal issues with recording phone calls?", "expected_out_of_context": False},
        ]

    def evaluate_model_responses(self, responses: List[Dict]) -> Dict:
        """
        Evaluate model responses against expected outcomes
        
        Args:
            responses: List of dictionaries with 'question', 'response', and 'is_out_of_context'
            
        Returns:
            Dictionary with evaluation metrics
        """
        if len(responses) != len(self.test_cases):
            raise ValueError("Number of responses must match number of test cases")
        
        y_true = [case["expected_out_of_context"] for case in self.test_cases]
        y_pred = [response["is_out_of_context"] for response in responses]
        
        # Calculate metrics
        accuracy = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred)
        recall = recall_score(y_true, y_pred)
        f1 = f1_score(y_true, y_pred)
        
        # Confusion matrix
        cm = confusion_matrix(y_true, y_pred)
        
        # Detailed analysis
        correct_predictions = sum(1 for true, pred in zip(y_true, y_pred) if true == pred)
        incorrect_predictions = len(y_true) - correct_predictions
        
        # False positives and negatives
        false_positives = sum(1 for true, pred in zip(y_true, y_pred) if not true and pred)
        false_negatives = sum(1 for true, pred in zip(y_true, y_pred) if true and not pred)
        
        results = {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1_score": f1,
            "confusion_matrix": cm.tolist(),
            "correct_predictions": correct_predictions,
            "incorrect_predictions": incorrect_predictions,
            "false_positives": false_positives,
            "false_negatives": false_negatives,
            "total_cases": len(y_true)
        }
        
        return results

    def generate_detailed_report(self, responses: List[Dict], save_to_file: bool = True) -> str:
        """Generate a detailed evaluation report"""
        metrics = self.evaluate_model_responses(responses)
        
        report = f"""
Legal AI Model Evaluation Report
===============================

Overall Performance:
- Accuracy: {metrics['accuracy']:.3f}
- Precision: {metrics['precision']:.3f}
- Recall: {metrics['recall']:.3f}
- F1 Score: {metrics['f1_score']:.3f}

Detailed Results:
- Total test cases: {metrics['total_cases']}
- Correct predictions: {metrics['correct_predictions']}
- Incorrect predictions: {metrics['incorrect_predictions']}
- False positives: {metrics['false_positives']} (legal questions marked as out-of-context)
- False negatives: {metrics['false_negatives']} (out-of-context questions marked as legal)

Confusion Matrix:
                 Predicted
                 Legal  Out-of-Context
Actual Legal     {metrics['confusion_matrix'][0][0]}      {metrics['confusion_matrix'][0][1]}
Actual OOC       {metrics['confusion_matrix'][1][0]}      {metrics['confusion_matrix'][1][1]}

Individual Test Case Analysis:
"""
        
        for i, (test_case, response) in enumerate(zip(self.test_cases, responses)):
            expected = test_case["expected_out_of_context"]
            actual = response["is_out_of_context"]
            status = "✓ CORRECT" if expected == actual else "✗ INCORRECT"
            
            report += f"""
{i+1}. {status}
   Question: {test_case['question']}
   Expected: {'Out-of-context' if expected else 'Legal'}
   Actual: {'Out-of-context' if actual else 'Legal'}
   Response: {response['response'][:100]}...
"""
        
        if save_to_file:
            with open('evaluation_report.txt', 'w', encoding='utf-8') as f:
                f.write(report)
            print("Evaluation report saved to evaluation_report.txt")
        
        return report

    def plot_confusion_matrix(self, responses: List[Dict], save_plot: bool = True):
        """Create and save confusion matrix plot"""
        metrics = self.evaluate_model_responses(responses)
        cm = metrics['confusion_matrix']
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=['Legal', 'Out-of-Context'],
                   yticklabels=['Legal', 'Out-of-Context'])
        plt.title('Legal AI Model - Confusion Matrix')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        
        if save_plot:
            plt.savefig('confusion_matrix.png', dpi=300, bbox_inches='tight')
            print("Confusion matrix plot saved to confusion_matrix.png")
        
        plt.show()

    def get_test_questions(self) -> List[str]:
        """Get list of test questions for evaluation"""
        return [case["question"] for case in self.test_cases]

def main():
    """Example usage of the evaluator"""
    evaluator = LegalAIEvaluator()
    
    # Example responses (you would get these from your model)
    example_responses = [
        {"question": q, "response": "Example response", "is_out_of_context": False}
        for q in evaluator.get_test_questions()
    ]
    
    # Generate report
    report = evaluator.generate_detailed_report(example_responses)
    print(report)

if __name__ == "__main__":
    main()
