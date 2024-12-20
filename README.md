## Overview
AiVoicer is a powerful desktop application that provides seamless voice transcription and AI-powered text processing. With customizable hotkeys, you can quickly transcribe audio or process text using OpenAI's advanced language models. Even the UI is German it works in any Language. English UI will come in next release.

<img width="499" alt="image" src="https://github.com/user-attachments/assets/5ee0e1f1-ef47-4532-9bc1-73519d9fbe52">
<img width="255" alt="image" src="https://github.com/user-attachments/assets/a32f8d23-5fd1-47e1-8de7-332572091e0b">

![PFEsq4sMpX](https://github.com/user-attachments/assets/cefb181f-8b86-41d8-8c37-95c5ea7db376)


## Features
- Voice recording with global hotkey (can be changed in Settings)
- AI-powered transcription using Whisper (local Modell with CPU or GPU) in every Language
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
1. Double-click start_aivoicer.bat
   - This script will:
     - Create a virtual environment
     - Install dependencies
     - Launch the application

### Manual Setup

1. Clone the repository:
```
git clone https://github.com/NeverBeLazyG/AiVoicer.git
cd AiVoicer
```
3. Create a virtual environment:
```
python -m venv .venv
.venv\Scripts\activate  # On Windows
```


5. Install dependencies:
bash
```
pip install -r requirements.txt
```

7. Run the application:
bash
```
python aivoicer.py
```

### Configuration
- First-time setup requires an OpenAI API key
- Go to application settings to configure (right click in Tray Icon):
  - OpenAI API key
  - Hotkeys

### Hotkeys
- Transcription Mode: Default Ctrl+Shift+F9
- Text Processing Mode: Default Ctrl+Shift+F10

## Dependencies
- CustomTkinter for UI
- OpenAI (GPT-4o-mini, can be changed) for text processing
- Whisper for transcription
- SoundDevice for audio recording

## Troubleshooting
- Ensure you have a valid OpenAI API key
- Check that your system meets the audio recording requirements
- For GPU acceleration, ensure CUDA is properly installed

## License
This project is licensed under the Apache License 2.0. You may use, distribute, and modify the code under the terms of this license. See the LICENSE file for full details.

## Contributing
Contributions are welcome! Please submit pull requests or open issues.

## Disclaimer
This tool requires an active internet connection and an OpenAI API key for full functionality.
