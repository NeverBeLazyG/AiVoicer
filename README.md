# AiVoicer - AI-Powered Voice Transcription and Text Processing Tool

## Overview
AiVoicer is a powerful desktop application that provides seamless voice transcription and AI-powered text processing. With customizable hotkeys, you can quickly transcribe audio or process text using OpenAI's advanced language models.

![PFEsq4sMpX](https://github.com/user-attachments/assets/cefb181f-8b86-41d8-8c37-95c5ea7db376)
![image](https://github.com/user-attachments/assets/43564901-eaad-41c7-9f52-629d02308364)
<img width="255" alt="image" src="https://github.com/user-attachments/assets/a32f8d23-5fd1-47e1-8de7-332572091e0b">







## Features
- Voice recording with global hotkey
- AI-powered transcription using Whisper
- Text processing capabilities:
  - Error correction
  - Rephrasing
  - Translation (to English)
  - Summarization
- Systray integration
- Customizable hotkeys

## Prerequisites
- Python 3.8+
- pip (Python package manager)
- CUDA-compatible GPU recommended (for faster processing)

## Installation and Running

### Automatic Setup (Windows)
1. Double-click `start_aivoicer.bat`
   - This script will:
     - Create a virtual environment
     - Install dependencies
     - Launch the application

### Manual Setup

1. Clone the repository:
```bash
git clone https://github.com/NeverBeLazyG/AiVoicer.git
cd AiVoicer
```

2. Create a virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python aivoicer.py
```

### Configuration
- First-time setup requires an OpenAI API key
- Go to application settings to configure:
  - OpenAI API key
  - Hotkeys

### Hotkeys
- Transcription Mode: Default `Ctrl+Shift+F9`
- Text Processing Mode: Default `Ctrl+Shift+F10`

## Dependencies
- CustomTkinter for UI
- OpenAI for text processing
- Whisper for transcription
- SoundDevice for audio recording

## Troubleshooting
- Ensure you have a valid OpenAI API key
- Check that your system meets the audio recording requirements
- For GPU acceleration, ensure CUDA is properly installed

## License
[Specify your license here]

## Contributing
Contributions are welcome! Please submit pull requests or open issues.

## Disclaimer
This tool requires an active internet connection and an OpenAI API key for full functionality.
