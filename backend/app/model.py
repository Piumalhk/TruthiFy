from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

class FakeNewsModel:
    def __init__(self):
        # Use a pre-trained model from Hugging Face Hub for fake news detection
        model_name = "hamzab/roberta-fake-news-classification"
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            self.model.to(self.device)
            print(f"Model loaded successfully on {self.device}")
        except Exception as e:
            print(f"Error loading model: {e}")
            # Fallback to a more basic model
            model_name = "distilbert-base-uncased-finetuned-sst-2-english"
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            self.model.to(self.device)
            print(f"Fallback model loaded successfully on {self.device}")
    
    def predict(self, text):
        try:
            # Tokenize the input text
            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                truncation=True,
                padding=True,
                max_length=512
            )
            
            # Move inputs to the same device as model
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Make prediction
            with torch.no_grad():
                outputs = self.model(**inputs)
                predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
                
            # Get the predicted class and confidence
            predicted_class = torch.argmax(predictions, dim=-1).item()
            confidence = predictions[0][predicted_class].item()
            
            # Map the prediction to human-readable labels
            if predicted_class == 0:
                label = "REAL"
            else:
                label = "FAKE"
                
            return {
                "prediction": label,
                "confidence": float(confidence),
                "probabilities": {
                    "REAL": float(predictions[0][0]),
                    "FAKE": float(predictions[0][1]) if predictions.shape[1] > 1 else 1 - float(predictions[0][0])
                }
            }
            
        except Exception as e:
            print(f"Error during prediction: {e}")
            return {
                "prediction": "ERROR",
                "confidence": 0.0,
                "error": str(e)
            }