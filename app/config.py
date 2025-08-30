# Configuration settings
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # File Upload Configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_EXTENSIONS = {'pdf', 'wav', 'mp3', 'png', 'jpg', 'jpeg'}
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # AI Model Configuration
    AI_MODEL = "gpt-5"  # Use GPT-5 for multimodal capabilities
    MAX_TOKENS = 1000   # Increased for detailed responses
    TEMPERATURE = 0.7
    VERBOSITY = "high"
    REASONING_EFFORT = "low"
    
    # Chat Configuration
    MAX_CONTEXT_LENGTH = 10000  # Maximum characters in context
    
    @staticmethod
    def validate_config():
        """Validate that required configuration is present"""
        if not Config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required in .env file")
        return True
