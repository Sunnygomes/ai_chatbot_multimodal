# Main chatbot logic and interface
from ai_integration.ai_model import AIModel
from ai_integration.data_preprocessing import preprocess

class Chatbot:
    def __init__(self):
        self.model = AIModel()
        self.context = ""
        self.max_context_length = 10000  # Limit context to avoid API limits

    def add_context(self, text):
        processed_text = preprocess(text)
        # Add new context
        new_context = self.context + " " + processed_text
        
        # Truncate if too long
        if len(new_context) > self.max_context_length:
            # Keep the most recent context
            new_context = new_context[-self.max_context_length:]
        
        self.context = new_context
        print(f"Context updated. Total length: {len(self.context)} characters")

    def ask(self, question):
        if not self.context.strip():
            return "I don't have any document content to reference. Please upload some files first!"
        
        try:
            answer = self.model.answer(self.context, question)
            return answer
        except Exception as e:
            return f"Sorry, I encountered an error while processing your question: {str(e)}"
    
    def get_context_summary(self):
        """Get a summary of the current context"""
        if not self.context:
            return "No documents loaded"
        
        word_count = len(self.context.split())
        char_count = len(self.context)
        return f"Loaded {word_count} words ({char_count} characters) from uploaded documents"
