# app.py
from flask import Flask, render_template, request, jsonify
import whisper
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'm4a', 'ogg', 'flac'}
MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Get available models
available_models = whisper.available_models()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def transcribe_audio(file_path, model_name):
    # Load the specified model
    model = whisper.load_model(model_name)
    
    # Load and preprocess audio
    audio = whisper.load_audio(file_path)
    audio = whisper.pad_or_trim(audio)
    
    # Create log-Mel spectrogram
    mel = whisper.log_mel_spectrogram(audio, n_mels=model.dims.n_mels).to(model.device)
    
    # Detect language
    _, probs = model.detect_language(mel)
    detected_language = max(probs, key=probs.get)
    
    # Decode audio
    options = whisper.DecodingOptions()
    result = whisper.decode(model, mel, options)
    
    return result.text, detected_language

@app.route('/')
def index():
    return render_template('index.html', models=available_models)

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    file = request.files['audio']
    
    if file.filename == '':
        return jsonify({'error': 'No audio file selected'}), 400
    
    if file and allowed_file(file.filename):
        # Get selected model from form data
        model_name = request.form.get('model', 'turbo')
        
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        try:
            # Transcribe the audio
            text, language = transcribe_audio(file_path, model_name)
            
            # Clean up the uploaded file
            os.remove(file_path)
            
            return jsonify({
                'text': text,
                'language': language
            })
        except Exception as e:
            # Clean up the uploaded file if processing fails
            if os.path.exists(file_path):
                os.remove(file_path)
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    app.run(debug=True)
