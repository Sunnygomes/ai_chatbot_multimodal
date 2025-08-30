# 🤖 AI Document Assistant

A professional AI-powered document analysis platform that can handle and interact with various types of files, including PDFs, images, and audio files. Built with Flask, OpenAI GPT-5, and modern web technologies.

## 🚀 Features

- **Multi-format Document Support**: PDF, Images (PNG, JPG, JPEG), Audio (WAV, MP3)
- **AI-Powered Q&A**: Uses OpenAI's ChatGPT for intelligent responses
- **Professional Web UI**: Modern, responsive interface built with Tailwind CSS
- **File Organization**: Automatically organizes files into appropriate folders
- **Text Extraction**: 
  - PDFs: Extract text using pdfplumber and PyPDF2
  - Images: OCR text extraction using pytesseract
  - Audio: Speech-to-text transcription using SpeechRecognition
- **File Preview**: View uploaded files directly in the browser
- **Real-time Processing**: Instant file processing and context building

## 📁 Project Structure

```
ai_integration/
  ├── __init__.py
  ├── ai_model.py           # OpenAI ChatGPT integration
  ├── data_preprocessing.py # Text preprocessing utilities
  └── chatbot.py            # Main chatbot logic and interface

audio/
  ├── __init__.py
  ├── audio_handler.py      # Audio file processing and transcription
  └── audio_to_text.py      # Speech-to-text utilities

images/
  ├── __init__.py
  ├── image_handler.py      # Image processing and OCR
  └── ocr.py                # Optical Character Recognition

pdf_management/
  ├── __init__.py
  ├── pdf_handler.py        # PDF text extraction
  └── pdf_to_text.py        # PDF processing utilities

app/
  ├── __init__.py
  ├── main.py               # CLI entry point
  ├── webapp.py             # Flask web application
  └── config.py             # Configuration settings

templates/
  └── index.html            # Professional web UI (500+ lines)

tests/
  ├── __init__.py
  ├── test_ai_model.py
  ├── test_audio.py
  ├── test_images.py
  └── test_pdf.py

.env                        # Environment variables (API keys)
requirements.txt            # Python dependencies
README.md                   # This file
.gitignore                  # Git ignore patterns
```

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd ai_chatbot_test01
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
.venv\Scripts\activate  # On Windows
# or
source .venv/bin/activate  # On macOS/Linux
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the project root and add your OpenAI API key:
```env
OPENAI_API_KEY=your_openai_api_key_here
SECRET_KEY=your_secret_key_here
DEBUG=false
```

### 5. Run the Application
```bash
python -m app.webapp
```

The application will be available at `http://localhost:5000`

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `SECRET_KEY`: Flask secret key for sessions
- `DEBUG`: Enable/disable debug mode

### File Limits
- Maximum file size: 16MB
- Supported formats: PDF, PNG, JPG, JPEG, WAV, MP3
- Maximum context length: 10,000 characters

## 💡 Usage

### 1. Upload Documents
- Click "Upload & Process" to add PDF, image, or audio files
- Files are automatically processed and organized in their respective folders
- Extracted text is saved as `.txt` files for easy viewing in VS Code

### 2. Ask Questions
- Type questions about your uploaded documents
- The AI will analyze the content and provide relevant answers
- Context is built from all uploaded files

### 3. File Management
- View all uploaded files in the sidebar
- Click on any file to preview it
- Files are organized by type (PDF, Images, Audio)

### 4. File Organization
- **PDFs** → `pdf_management/` folder + `_extracted.txt`
- **Images** → `images/` folder + `_ocr.txt`
- **Audio** → `audio/` folder + `_transcript.txt`

## 🧪 Testing

Run the test suite:
```bash
python -m pytest tests/
```

## 🔍 Troubleshooting

### Common Issues

1. **"No context available" error**:
   - Upload files first before asking questions
   - Check if files were processed successfully

2. **API Key errors**:
   - Verify your OpenAI API key is correct in `.env`
   - Check your OpenAI account has sufficient credits

3. **File processing errors**:
   - Ensure files are not corrupted
   - Check file size limits (16MB max)
   - Verify file formats are supported

4. **Dependencies issues**:
   - Make sure all packages are installed: `pip install -r requirements.txt`
   - For OCR: Install Tesseract OCR on your system

## 🔐 Security

- API keys are stored in environment variables
- File uploads are validated and secured
- Maximum file size limits prevent abuse
- Input sanitization for all user inputs

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **OpenAI** for the ChatGPT API
- **Flask** for the web framework
- **Tailwind CSS** for the modern UI design
- **HuggingFace** for transformer models
- **Python libraries**: PyPDF2, pdfplumber, pytesseract, SpeechRecognition

## 📞 Support

For support, please open an issue on GitHub or contact the development team.

---

**Built with ❤️ using Python, Flask, OpenAI ChatGPT, and modern web technologies.**
