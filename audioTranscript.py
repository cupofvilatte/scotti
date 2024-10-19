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
    transcription = ""

    # Load the audio file
    with sr.AudioFile(file_path) as source:
        while True:
            try:
                audio = recognizer.record(source, duration=10)  # Record in 10-second chunks
                text = recognizer.recognize_google(audio)
                transcription += text + " "
            except sr.UnknownValueError:
                print("Could not understand the audio")
                break
            except sr.RequestError as e:
                print(f"Could not request results from Google's Speech Recognition service; {e}")
                break
            except EOFError:
                break  # End of file

    return transcription.strip()
def main():
    file_path = input("Enter the path to your video or audio file: ")
    
    if file_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):  # Video file
        print("Extracting audio from video...")
        audio_path = extract_audio(file_path)
    else:  # Audio file
        audio_path = file_path
    
    print("Transcribing audio...")
    transcription = transcribe_audio(audio_path)
    
    # print("\nTranscription:")
    # print(transcription)
    out_file = open("output.txt", "w")
    out_file.write(transcription)
    out_file.close()
    
    # Clean up temporary files
    if audio_path != file_path:
        os.remove(audio_path)
    
    return transcription

if __name__ == "__main__":
    main()