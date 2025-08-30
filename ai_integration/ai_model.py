# Core AI model logic (training, inference) with GPT-5 multimodal capabilities
import openai
import os
import base64
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class AIModel:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def answer(self, context, question):
        """Answer questions using GPT-5 with text context"""
        try:
            prompt = f"""Based on the following document content, please answer the user's question:

Context: {context}

Question: {question}

Please provide a detailed and accurate answer based only on the information provided in the context."""

            response = self.client.chat.completions.create(
                model="gpt-5",  # Use GPT-5 for better performance
                messages=[{
                    "role": "user", 
                    "content": prompt
                }],
                verbosity="high",
                reasoning_effort="low"
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}. Please check your OpenAI API key."

    def process_image_with_gpt5(self, image_path, question=None):
        """Process images using GPT-5 multimodal capabilities"""
        try:
            # Read and encode image
            with open(image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            
            prompt = question or "Please extract all text content from this image and describe what you see."
            
            response = self.client.chat.completions.create(
                model="gpt-5",
                messages=[{
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }],
                verbosity="high",
                reasoning_effort="low"
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error processing image with GPT-5: {str(e)}"

    def transcribe_audio_with_whisper(self, audio_path):
        """Transcribe audio using OpenAI's Whisper model"""
        try:
            with open(audio_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
            return transcript.text
        except Exception as e:
            return f"Error transcribing audio with Whisper: {str(e)}"

    def process_pdf_with_gpt5(self, pdf_path, extracted_text):
        """Process PDF content including images using GPT-5"""
        try:
            prompt = f"""Please analyze this PDF content and extract all relevant information including text and any image descriptions:

Text Content: {extracted_text}

Please provide a comprehensive summary of all the information in this document."""

            response = self.client.chat.completions.create(
                model="gpt-5",
                messages=[{
                    "role": "user", 
                    "content": prompt
                }],
                verbosity="high",
                reasoning_effort="low"
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error processing PDF with GPT-5: {str(e)}"
