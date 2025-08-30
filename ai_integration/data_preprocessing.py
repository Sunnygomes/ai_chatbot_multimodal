# Preprocessing for all file types
import re

def preprocess(text):
    """Clean and preprocess text for better AI processing"""
    if not text or not isinstance(text, str):
        return ""
    
    # Remove extra whitespace and newlines
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters that might interfere
    text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)]', ' ', text)
    
    # Strip and ensure reasonable length
    text = text.strip()
    
    # Limit text length to avoid API limits
    if len(text) > 8000:
        text = text[:8000] + "..."
    
    return text
