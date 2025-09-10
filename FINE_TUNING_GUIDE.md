# Mistral AI Fine-Tuning Guide for Legal AI

This project belongs to SANDEEP REDDY K

## Overview
This guide walks you through fine-tuning a Mistral AI model to improve out-of-context detection in your legal AI application.

## Prerequisites

1. **Mistral AI API Key**
   - Sign up at [Mistral AI Console](https://console.mistral.ai/)
   - Generate an API key
   - Set environment variable: `MISTRAL_API_KEY=your_api_key_here`

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Step-by-Step Fine-Tuning Process

### Step 1: Generate Training Data
```bash
python training_data_generator.py
```
This creates `legal_ai_training_data.jsonl` with 1000 training samples (500 legal questions + 500 out-of-context questions).

### Step 2: Set Environment Variables
```bash
# Windows PowerShell
$env:MISTRAL_API_KEY = "your_mistral_api_key"

# Windows Command Prompt
set MISTRAL_API_KEY=your_mistral_api_key

# Linux/Mac
export MISTRAL_API_KEY=your_mistral_api_key
```

### Step 3: Run Fine-Tuning Pipeline
```bash
python mistral_fine_tuner.py
```

This will:
1. Upload training data to Mistral AI
2. Create a fine-tuning job
3. Monitor progress (can take 30-60 minutes)
4. Test the fine-tuned model
5. Save the model ID for later use

### Step 4: Update Model Configuration
After fine-tuning completes, set the fine-tuned model ID:
```bash
# Set the fine-tuned model ID
$env:MISTRAL_FINE_TUNED_MODEL_ID = "ft:your_model_id_here"
```

### Step 5: Run the Updated Application
```bash
python app_with_mistral.py
```

## Testing and Evaluation

### Test the Fine-Tuned Model
```bash
python model_evaluator.py
```

### Check Model Status via API
Visit: `http://localhost:5000/test_mistral`

### Monitor Model Performance
Visit: `http://localhost:5000/model_status`

## Expected Improvements

After fine-tuning, your model should:
- Better detect out-of-context questions
- Respond with "Out of context - I can only assist with legal-related questions" for non-legal queries
- Maintain high accuracy for legal questions
- Reduce false positives/negatives

## Troubleshooting

### Common Issues:

1. **API Key Error**
   - Ensure `MISTRAL_API_KEY` is set correctly
   - Check API key validity at Mistral console

2. **Fine-Tuning Job Fails**
   - Check training data format
   - Ensure sufficient credits in Mistral account
   - Review error messages in console output

3. **Model Not Loading**
   - Verify `MISTRAL_FINE_TUNED_MODEL_ID` is set
   - Check model ID format
   - Ensure model fine-tuning completed successfully

4. **Fallback Mode**
   - If Mistral fails, app automatically uses keyword-based detection
   - Check `/model_status` endpoint for current status

## Cost Considerations

- Fine-tuning costs depend on training data size and model complexity
- Monitor usage at Mistral AI console
- Consider starting with smaller datasets for testing

## Performance Monitoring

The application logs:
- Model responses and accuracy
- Fallback usage statistics  
- User interaction patterns
- Model performance metrics

## Next Steps

1. **Collect Real User Data**: Use actual user interactions to improve training data
2. **Iterative Improvement**: Regularly retrain with new examples
3. **A/B Testing**: Compare fine-tuned vs base model performance
4. **Domain Expansion**: Add more legal specializations to training data

## Files Created

- `training_data_generator.py` - Generates training dataset
- `mistral_fine_tuner.py` - Handles fine-tuning pipeline
- `mistral_integration.py` - Mistral AI integration layer
- `model_evaluator.py` - Model performance evaluation
- `app_with_mistral.py` - Updated Flask application
- `requirements.txt` - Python dependencies

## Support

For issues with:
- Mistral AI: Check [Mistral Documentation](https://docs.mistral.ai/)
- Fine-tuning: Review console logs and error messages
- Integration: Check application logs and `/model_status` endpoint
