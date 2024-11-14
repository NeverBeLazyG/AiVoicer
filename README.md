# AiVoicer - AI-Powered local Voice Transcription and Text Processing Tool

## Overview
AiVoicer is a powerful desktop application that provides seamless voice transcription and AI-powered text processing. With customizable hotkeys, you can quickly transcribe audio or process text using OpenAI's advanced language models. Even though the UI is in German, it works in any language. An English UI will be available in the next release.

<img width="499" alt="image" src="https://github.com/user-attachments/assets/5ee0e1f1-ef47-4532-9bc1-73519d9fbe52">
<img width="255" alt="image" src="https://github.com/user-attachments/assets/a32f8d23-5fd1-47e1-8de7-332572091e0b">

![PFEsq4sMpX](https://github.com/user-attachments/assets/cefb181f-8b86-41d8-8c37-95c5ea7db376)

## Features
- Voice recording with global hotkey (can be changed in Settings)
- AI-powered transcription using Whisper (local model with CPU or GPU) in every language
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
