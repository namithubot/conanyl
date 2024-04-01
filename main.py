from flask import Flask, request, render_template
import os
import requests
from werkzeug.utils import secure_filename
import json
from openai import OpenAI

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp3', 'wav'}

# Load configuration from JSON file
config = json.load(open('config.json'))

# Configure upload folder and API keys
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
DEEPGRAM_API_KEY = config['DEEPGRAM_API_KEY']
openai_client = OpenAI(api_key=config['OPENAI_API_KEY'])

def allowed_file(filename):
    """Check if the file has an allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def transcribe_audio(file_path):
    """Transcribe audio file using Deepgram API"""
    url = "https://api.deepgram.com/v1/listen"
    headers = {
        'Authorization': 'Token {}'.format(DEEPGRAM_API_KEY),
    }
    files = {'content': open(file_path, 'rb')}
    params = {
        'diarize': 'true',
        'punctuate': 'true',
        'utterances': 'true',
    }
    response = requests.post(url, headers=headers, params=params, files=files)
    if response.status_code == 200:
        transcriptions = response.json().get('results', {}).get('utterances', [{}])
        # Parse transcriptions into separate dialogues
        current_sentence = ''
        current_speaker = ''
        transcript = []
        for t in transcriptions:
            if t['speaker'] == current_speaker:
                current_sentence += ' ' + t['transcript']
            else:
                if current_speaker != '':
                    transcript.append({ 'speaker': current_speaker, 'says': current_sentence })
                current_sentence = t['transcript']
                current_speaker = t['speaker']
        if current_speaker != '':
            transcript.append({ 'speaker': current_speaker, 'says': current_sentence })
        return transcript
    else:
        return 'Transcription failed'

def analyze_sentiment(transcriptions):
    """Analyze sentiment of transcribed text using OpenAI API"""
    # Concatenate transcriptions into a single text
    text = ''
    i = 0
    for transcription in transcriptions:
        text = text + '[{}] Speaker {}:{}\n'.format(i + 1, transcription['speaker'] + 1, transcription['says'])
        i = i + 1
    # Generate sentiment analysis using OpenAI
    response = openai_client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a psychologist specializing in observing speech patterns.",
            },
            {
                "role": "user",
                "content": '''Consider this dialogue transcript.
                Analyze the sentiment of the following transcript and prorvide details like mood, confidence, characteristics and estimate working style of the speakers in this conversation.
                The dialogue numbers are indicated in square brackets at the beginning of every dialogue. Provided context by dialogue number\n''' + text,
            }
        ],
        model="gpt-3.5-turbo",
    )
    # Extract sentiment analysis from OpenAI response
    reply = ''
    for res in response.choices:
        reply = reply + res.message.content.strip() + '\n'
    return reply

@app.route('/')
def upload_form():
    """Render upload form"""
    return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_file():
    """Handle file upload and perform transcription and sentiment analysis"""
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        transcriptions = transcribe_audio(file_path)
        sentiment = analyze_sentiment(transcriptions)
        return render_template('upload.html', transcription=transcriptions, sentiment=sentiment)
    else:
        return 'Invalid file format'

if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get("PORT", 8080)))
