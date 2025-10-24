# model/fake_news_model.py
from transformers import pipeline

def load_model():
    model_name = "ghanashyamvtatti/roberta-fake-news"  # your new model
    model_pipeline = pipeline("text-classification", model=model_name)
    return model_pipeline
