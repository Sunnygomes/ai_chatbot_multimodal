def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from ai_integration.chatbot import Chatbot
from audio.audio_handler import handle_audio
from images.image_handler import handle_image
from pdf_management.pdf_handler import handle_pdf
from app.config import Config

# Load environment variables
load_dotenv()

# Validate configuration
try:
    Config.validate_config()
    print("✅ Configuration validated successfully")
except ValueError as e:
    print(f"❌ Configuration error: {e}")
    exit(1)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
AUDIO_FOLDER = os.path.join(BASE_DIR, 'audio')
IMAGES_FOLDER = os.path.join(BASE_DIR, 'images')
PDF_FOLDER = os.path.join(BASE_DIR, 'pdf_management')
ALLOWED_EXTENSIONS = {'pdf', 'wav', 'mp3', 'png', 'jpg', 'jpeg'}

app = Flask(__name__, template_folder=TEMPLATE_DIR)
app.secret_key = Config.SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['AUDIO_FOLDER'] = AUDIO_FOLDER
app.config['IMAGES_FOLDER'] = IMAGES_FOLDER
app.config['PDF_FOLDER'] = PDF_FOLDER
app.config['MAX_CONTENT_LENGTH'] = Config.MAX_CONTENT_LENGTH

# Create folders if they don't exist
for folder in [UPLOAD_FOLDER, AUDIO_FOLDER, IMAGES_FOLDER, PDF_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

chatbot = Chatbot()

@app.route('/', methods=['GET', 'POST'])
def index():
    answer = None
    if request.method == 'POST':
        # Handle file upload
        if 'file' in request.files:
            file = request.files['file']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                ext = filename.rsplit('.', 1)[1].lower()
                
                # Determine the appropriate folder based on file type
                if ext == 'pdf':
                    folder = app.config['PDF_FOLDER']
                elif ext in ['wav', 'mp3']:
                    folder = app.config['AUDIO_FOLDER']
                elif ext in ['png', 'jpg', 'jpeg']:
                    folder = app.config['IMAGES_FOLDER']
                else:
                    folder = app.config['UPLOAD_FOLDER']
                
                filepath = os.path.join(folder, filename)
                print(f"Saving file to: {filepath}")  # Debug print
                
                try:
                    file.save(filepath)
                    print(f"File saved successfully: {filepath}")  # Debug print
                    
                    text = ''
                    
                    if ext == 'pdf':
                        try:
                            text = handle_pdf(filepath)
                            if text and text.strip():
                                txt_path = os.path.splitext(filepath)[0] + '_extracted.txt'
                                with open(txt_path, 'w', encoding='utf-8') as f:
                                    f.write(text)
                                print(f"PDF text extracted: {len(text)} characters")
                            else:
                                text = "No readable text found in PDF"
                        except Exception as e:
                            text = f"Error processing PDF: {e}"
                            print(f"PDF processing error: {e}")
                    elif ext in ['wav', 'mp3']:
                        try:
                            text = handle_audio(filepath)
                            if text and text.strip():
                                txt_path = os.path.splitext(filepath)[0] + '_transcript.txt'
                                with open(txt_path, 'w', encoding='utf-8') as f:
                                    f.write(text)
                                print(f"Audio transcript: {len(text)} characters")
                            else:
                                text = "No speech detected in audio"
                        except Exception as e:
                            text = f"Error processing audio: {e}"
                            print(f"Audio processing error: {e}")
                    elif ext in ['png', 'jpg', 'jpeg']:
                        try:
                            text = handle_image(filepath)
                            if text and text.strip():
                                txt_path = os.path.splitext(filepath)[0] + '_ocr.txt'
                                with open(txt_path, 'w', encoding='utf-8') as f:
                                    f.write(text)
                                print(f"Image OCR: {len(text)} characters")
                            else:
                                text = "No text detected in image"
                        except Exception as e:
                            text = f"Error processing image: {e}"
                            print(f"Image processing error: {e}")
                    
                    if text and text.strip() and not text.startswith("Error"):
                        chatbot.add_context(text)
                        flash(f'File "{filename}" uploaded and processed successfully! Found {len(text)} characters of content.')
                    else:
                        flash(f'File "{filename}" uploaded but {text.lower() if text else "no content extracted"}.')
                    
                except Exception as e:
                    print(f"Error saving file: {e}")
                    flash(f'Error uploading file: {e}')
            else:
                flash('Invalid file type or no file selected!')
        # Handle question
        if 'question' in request.form and request.form['question'].strip():
            question = request.form['question'].strip()
            print(f"Question asked: {question}")
            try:
                answer = chatbot.ask(question)
                print(f"Answer generated: {answer[:100]}...")
            except Exception as e:
                print(f"Error generating answer: {e}")
                answer = f"Sorry, I encountered an error: {str(e)}"

    # List uploaded files for sidebar from organized folders
    files = []
    try:
        # Check audio folder
        for fname in os.listdir(app.config['AUDIO_FOLDER']):
            fpath = os.path.join(app.config['AUDIO_FOLDER'], fname)
            if os.path.isfile(fpath) and fname.endswith(('.wav', '.mp3')):
                files.append({'name': fname, 'type': 'audio', 'path': f'audio/{fname}', 'folder': 'audio'})
        
        # Check images folder
        for fname in os.listdir(app.config['IMAGES_FOLDER']):
            fpath = os.path.join(app.config['IMAGES_FOLDER'], fname)
            if os.path.isfile(fpath) and fname.endswith(('.png', '.jpg', '.jpeg')):
                files.append({'name': fname, 'type': 'image', 'path': f'images/{fname}', 'folder': 'images'})
        
        # Check PDF folder
        for fname in os.listdir(app.config['PDF_FOLDER']):
            fpath = os.path.join(app.config['PDF_FOLDER'], fname)
            if os.path.isfile(fpath) and fname.endswith('.pdf'):
                files.append({'name': fname, 'type': 'pdf', 'path': f'pdf_management/{fname}', 'folder': 'pdf_management'})
                
    except Exception as e:
        print(f"Error listing files: {e}")
        files = []

    return render_template('index.html', answer=answer, files=files)

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    """Serve uploaded files from organized folders"""
    # Handle different folder structures
    if 'audio/' in filename:
        folder_path = app.config['AUDIO_FOLDER']
        file_name = filename.replace('audio/', '')
    elif 'images/' in filename:
        folder_path = app.config['IMAGES_FOLDER']
        file_name = filename.replace('images/', '')
    elif 'pdf_management/' in filename:
        folder_path = app.config['PDF_FOLDER']
        file_name = filename.replace('pdf_management/', '')
    else:
        folder_path = app.config['UPLOAD_FOLDER']
        file_name = filename
    
    return send_from_directory(folder_path, file_name)

if __name__ == '__main__':
    app.run(debug=True)
