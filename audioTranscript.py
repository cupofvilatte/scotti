import speech_recognition as sr
from pydub import AudioSegment
import moviepy.editor as mp
import os

def extract_audio(file_path):
    """Extract audio from video file"""
    video = mp.VideoFileClip(file_path)
    audio = video.audio
    audio.write_audiofile("temp_audio.wav")
    return "temp_audio.wav"

def transcribe_audio(file_path):
    """Transcribe audio file to text"""
    recognizer = sr.Recognizer()
    
    # Load audio file
    audio_file = sr.AudioFile(file_path)
    
    with audio_file as source:
        audio = recognizer.record(source)
    
    try:
        # Transcribe audio to text
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Speech Recognition could not understand the audio"
    except sr.RequestError as e:
        return f"Could not request results from Speech Recognition service; {e}"

def main():
    file_path = input("Enter the path to your video or audio file: ")
    
    if file_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):  # Video file
        print("Extracting audio from video...")
        audio_path = extract_audio(file_path)
    else:  # Audio file
        audio_path = file_path
    
    print("Transcribing audio...")
    transcription = transcribe_audio(audio_path)
    
    print("\nTranscription:")
    print(transcription)
    
    # Clean up temporary files
    if audio_path != file_path:
        os.remove(audio_path)

if __name__ == "__main__":
    main()