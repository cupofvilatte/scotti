import os
from flask import Flask, request, jsonify, render_template
import speech_recognition as sr
from pydub import AudioSegment
import moviepy.editor as mp

import summarizeText
import createQuestion

app = Flask(__name__)
# Folders to store uploaded files and transcripts
UPLOAD_FOLDER = 'uploads'
TRANSCRIPT_FOLDER = 'transcripts'
SUMMARIZE_FOLDER = 'summarize'

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TRANSCRIPT_FOLDER, exist_ok=True)

def extract_audio(file_path):
    """Extract audio from video file"""
    video = mp.VideoFileClip(file_path)
    audio = video.audio
    audio_path = os.path.join(UPLOAD_FOLDER, "temp_audio.wav")
    audio.write_audiofile(audio_path)
    return audio_path

def transcribe_audio(file_path):
    """Transcribe audio file to text"""
    recognizer = sr.Recognizer()
    transcription = ""

    # Load the audio file
    with sr.AudioFile(file_path) as source:
        while True:
            try:
                audio = recognizer.record(source, duration=10)  # Record in 10-second chunks
                text = recognizer.recognize_google(audio)
                transcription += text + " "
            except sr.UnknownValueError:
                break  # Could not understand the audio
            except sr.RequestError as e:
                return f"Could not request results from Google's Speech Recognition service; {e}"
            except EOFError:
                break  # End of file

    return transcription.strip()

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if a file was uploaded
    if 'file' not in request.files:
        return jsonify(error="No file uploaded"), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify(error="No selected file"), 400

    # Save the uploaded file
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Process the file
    if file_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
        audio_path = extract_audio(file_path)
    else:
        audio_path = file_path

    transcription = transcribe_audio(audio_path)

    # transcript_file_path = os.path.join(TRANSCRIPT_FOLDER, f"{os.path.splitext(file.filename)[0]}_transcription.txt")
    transcript_file_path = os.path.join(TRANSCRIPT_FOLDER, "transcription.txt")
    with open(transcript_file_path, 'w') as f:
        f.write(transcription)
    # Clean up temporary files
    if audio_path != file_path:
        os.remove(audio_path)

    return jsonify(transcription=transcription)

@app.route('/summarize', methods=['POST'])
def summarize():
    # Check if transcription text was provided
    print("Form data:", request.form)  # Add this line
    transcription = request.form.get('transcription')
    print("Transcription:", transcription)
    if not transcription:
        return jsonify(error="No transcription provided"), 400

    try:
        # Summarize the transcription
        summary = summarizeText.summarize(transcription)
        if summary is None:  # Handle if summarize returns None
            return jsonify(error="Summary generation failed"), 500

        return jsonify(summary=summary)
    except Exception as e:
        return jsonify(error=str(e)), 500  # Return the error as JSON

@app.route('/questionize', methods=['POST'])
def questionize():
    summary = request.form.get('summary')
    if not summary:
        return jsonify(error="No summary provided"), 400
    
    questions = createQuestion.process_response(summary)
    if not questions:
        return jsonify(error="Question generation failed"), 500
        
    return render_template('question.html', questions=questions)
    

if __name__ == '__main__':
    app.run(debug=True)
