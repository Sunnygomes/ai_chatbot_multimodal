# Entry point for running the app (CLI or web)
from ai_integration.chatbot import Chatbot
from audio.audio_handler import handle_audio
from images.image_handler import handle_image
from pdf_management.pdf_handler import handle_pdf

def main():
    bot = Chatbot()
    # Example: Load files (replace with your actual file paths)
    try:
        pdf_text = handle_pdf('pdf_management/sample.pdf')
        audio_text = handle_audio('audio/sample.wav')
        image_text = handle_image('images/sample.png')
        bot.add_context(pdf_text)
        bot.add_context(audio_text)
        bot.add_context(image_text)
    except Exception as e:
        print(f"Error loading files: {e}")

    print("Ask a question (type 'exit' to quit):")
    while True:
        question = input("> ")
        if question.lower() == 'exit':
            break
        print("Answer:", bot.ask(question))

if __name__ == "__main__":
    main()
