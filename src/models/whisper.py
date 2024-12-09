import os
import wave
import torch
import whisper

from pydub import AudioSegment
import speech_recognition as sr
from pydub.effects import normalize

def enhanced_preprocess_audio(audio_file, export_path=None):

    print("Loading the speech.")
    audio = AudioSegment.from_file(audio_file)

    print(f"Starting enhanced audio preprocessing for {audio_file}")
    
    # Convert to mono
    # audio = audio.set_channels(1)
    
    # # Normalize audio (adjust volume to a standard level)
    # audio = normalize(audio)
    
    # # Increase volume by 10 dB (adjust as needed)
    # audio = audio + 10
    
    # # Remove low frequencies (below 80Hz) which are often noise
    # audio = audio.high_pass_filter(80)
    
    # # Set sample rate to 16kHz
    # audio = audio.set_frame_rate(16000)
    
    # If export_path is not provided, create one based on the input filename
    if export_path is None:
        base_name = os.path.splitext(os.path.basename(audio_file))[0]
        export_path = f"preprocessed_{base_name}.wav"

    # Ensure the directory exists
    directory = os.path.dirname(export_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)


    # Export to file
    audio.export(export_path, format="wav")
    print(f"Preprocessed audio exported to {export_path}")
    
    print("Enhanced audio preprocessing completed.")
    return export_path

def transcribe_with_whisper(audio_file_path, initial_prompt, model_size="base"):
    """
    Transcribe audio using OpenAI's Whisper model.
    
    :param audio_file_path: Path to the audio file
    :param model_size: Size of the Whisper model to use ("tiny", "base", "small", "medium", "large")
    :return: Transcribed text
    """
    # Check for CUDA availability
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    # Load the Whisper model
    print("Loading Whisper Model.")
    model = whisper.load_model(model_size).to(device)

    # Perform the transcription
    print("Performing the transciption")
    result = model.transcribe(audio=audio_file_path, language="en", initial_prompt=initial_prompt)

    return result["text"]

def transcribe_audio(audio, initial_prompt):
    print("Starting audio transcription...")
    try:
        transcript = transcribe_with_whisper(audio,initial_prompt)
        print("Audio transcription completed.")
    
    except sr.UnknownValueError as e:
        print("Speech recognition could not understand audio")
        print(f"Speech recognition could not understand audio: {e}")
        print(f"Audio file: {audio}")
        print(f"Audio duration: {len(AudioSegment.from_file(audio))/1000} seconds")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from speech recognition service; {e}")
        return ""
    return transcript

def start_transcription(audio_file,initial_prompt):

    audio_file = enhanced_preprocess_audio(audio_file,"../data/processed/temp2.wav")
    transcript = transcribe_audio(audio_file, initial_prompt)
    if not transcript:
        print("Transcription failed.")
        return ''
    
    return transcript

def record_and_transcribe(initial_prompt):
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=2)
        
        print("Please speak something...")
        try:
            print("Listening Started...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=15)
            print("Listening Completed...")
            
            # First save as WAV
            print("saving as wav file")
            wav_filename = "whisper_temp.wav"
            with wave.open(wav_filename, 'wb') as wf:
                wf.setnchannels(1)  # Mono
                wf.setsampwidth(audio.sample_width)
                wf.setframerate(audio.sample_rate)
                wf.writeframes(audio.get_raw_data())

            transcript = start_transcription(wav_filename, initial_prompt)
            
            # Remove temporary WAV file
            # os.remove(wav_filename)

            return transcript
                
        except sr.WaitTimeoutError:
            print("No speech detected within timeout period")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

def run(audio_file_path : str = "", initial_prompt: str = None):
    if not audio_file_path:
        return record_and_transcribe(initial_prompt)
    return start_transcription(audio_file_path, initial_prompt)