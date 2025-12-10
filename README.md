# studyscribe

StudyScribe is a web-based transcription application that uses OpenAI's Whisper AI to convert audio files into text. It provides a simple interface for uploading audio files and getting accurate transcriptions.

## Features

- **Multiple Model Support**: Choose from all available Whisper models for transcription
- **Drag & Drop Interface**: Easy file upload with drag and drop functionality
- **Multi-format Support**: Accepts MP3, WAV, M4A, OGG, and FLAC audio files
- **Language Detection**: Automatically detects the spoken language
- **Responsive Design**: Works on both desktop and mobile devices

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd studyscribe
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the Flask application:
   ```bash
   python app.py
   ```

2. Open your browser and navigate to `http://localhost:5000`

3. Select your preferred Whisper model from the dropdown
4. Upload an audio file using drag & drop or the file browser
5. View the transcription result with detected language

## Available Models

The application automatically detects all available Whisper models through `whisper.available_models()`. These include:
- `tiny`
- `base`
- `small`
- `medium`
- `large`
- `large-v2`
- `large-v3`
- `turbo`

## Requirements

- Python 3.11
- Flask
- Whisper

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) for the transcription technology
- [Flask](https://flask.palletsprojects.com/) for the web framework