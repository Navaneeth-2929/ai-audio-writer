# transcriber.py
import speech_recognition as sr
import os
from datetime import datetime
from colorama import init, Fore, Style

# Initialize colorama for colored output
init(autoreset=True)

class SpeechTranscriber:
    """Main class for speech-to-text transcription"""
    
    def __init__(self):
        """Initialize the recognizer and settings"""
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        print(f"{Fore.YELLOW}🎤 Initializing microphone...{Style.RESET_ALL}")
        
        # Adjust for ambient noise (helps with background noise)
        try:
            with self.microphone as source:
                print(f"{Fore.YELLOW}Calibrating for ambient noise... Please wait.{Style.RESET_ALL}")
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
            print(f"{Fore.GREEN}✅ Microphone ready!{Style.RESET_ALL}\n")
        except Exception as e:
            print(f"{Fore.RED}❌ Microphone error: {e}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Make sure your microphone is connected and working.{Style.RESET_ALL}")
        
        # Create transcriptions folder if it doesn't exist
        self.transcriptions_folder = "transcriptions"
        if not os.path.exists(self.transcriptions_folder):
            os.makedirs(self.transcriptions_folder)
            print(f"{Fore.GREEN}✅ Created transcriptions folder{Style.RESET_ALL}")
    
    def transcribe_from_microphone(self, language="en-US", timeout=5):
        """
        Transcribe speech from microphone
        
        Args:
            language: Language code (en-US, es-ES, fr-FR, etc.)
            timeout: Maximum seconds to listen
        
        Returns:
            Transcribed text or None if failed
        """
        try:
            print(f"{Fore.CYAN}🎤 Listening... (speak clearly){Style.RESET_ALL}")
            
            with self.microphone as source:
                # Listen for audio
                audio = self.recognizer.listen(source, timeout=timeout)
            
            print(f"{Fore.YELLOW}⚙️ Processing...{Style.RESET_ALL}")
            
            # Use Google's speech recognition (requires internet)
            text = self.recognizer.recognize_google(audio, language=language)
            
            return text
            
        except sr.WaitTimeoutError:
            print(f"{Fore.RED}⏰ No speech detected. Try again.{Style.RESET_ALL}")
            return None
        except sr.UnknownValueError:
            print(f"{Fore.RED}😕 Could not understand audio. Please speak clearly.{Style.RESET_ALL}")
            return None
        except sr.RequestError as e:
            print(f"{Fore.RED}🌐 Could not request results from Google API: {e}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Check your internet connection.{Style.RESET_ALL}")
            return None
        except Exception as e:
            print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")
            return None
    
    def transcribe_from_file(self, file_path, language="en-US"):
        """
        Transcribe speech from an audio file
        
        Args:
            file_path: Path to audio file (WAV, MP3, etc.)
            language: Language code
        
        Returns:
            Transcribed text or None if failed
        """
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                print(f"{Fore.RED}❌ File not found: {file_path}{Style.RESET_ALL}")
                return None
            
            print(f"{Fore.CYAN}📁 Processing file: {file_path}{Style.RESET_ALL}")
            
            # Handle different audio formats
            if file_path.lower().endswith('.wav'):
                # Directly process WAV files
                with sr.AudioFile(file_path) as source:
                    audio = self.recognizer.record(source)
            else:
                # For MP3 and other formats, use pydub to convert
                try:
                    from pydub import AudioSegment
                    print(f"{Fore.YELLOW}⚙️ Converting audio format...{Style.RESET_ALL}")
                    
                    # Convert to WAV temporarily
                    audio_segment = AudioSegment.from_file(file_path)
                    temp_wav = "temp_audio.wav"
                    audio_segment.export(temp_wav, format="wav")
                    
                    # Process the converted file
                    with sr.AudioFile(temp_wav) as source:
                        audio = self.recognizer.record(source)
                    
                    # Clean up temp file
                    os.remove(temp_wav)
                    
                except ImportError:
                    print(f"{Fore.RED}❌ pydub not installed. Install it for MP3 support:{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}pip install pydub{Style.RESET_ALL}")
                    return None
                except Exception as e:
                    print(f"{Fore.RED}❌ Error converting file: {e}{Style.RESET_ALL}")
                    return None
            
            # Recognize speech
            print(f"{Fore.YELLOW}⚙️ Transcribing...{Style.RESET_ALL}")
            text = self.recognizer.recognize_google(audio, language=language)
            return text
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error processing file: {e}{Style.RESET_ALL}")
            return None
    
    def save_transcription(self, text, source_type="microphone"):
        """
        Save transcribed text to a file
        
        Args:
            text: Transcribed text
            source_type: Where the audio came from
        
        Returns:
            Path to saved file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"transcription_{timestamp}.txt"
        filepath = os.path.join(self.transcriptions_folder, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"{'='*50}\n")
            f.write(f"SPEECH-TO-TEXT TRANSCRIPTION\n")
            f.write(f"{'='*50}\n")
            f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Source: {source_type}\n")
            f.write(f"{'='*50}\n\n")
            f.write(f"Transcribed Text:\n{text}\n")
        
        print(f"{Fore.GREEN}✅ Transcription saved to: {filepath}{Style.RESET_ALL}")
        return filepath
    
    def list_transcriptions(self):
        """List all saved transcriptions"""
        files = os.listdir(self.transcriptions_folder)
        if not files:
            print(f"{Fore.YELLOW}📂 No transcriptions found.{Style.RESET_ALL}")
            return []
        
        print(f"\n{Fore.CYAN}📋 Saved Transcriptions:{Style.RESET_ALL}")
        files.sort(reverse=True)  # Show newest first
        
        for i, file in enumerate(files[:10], 1):  # Show last 10
            filepath = os.path.join(self.transcriptions_folder, file)
            size = os.path.getsize(filepath)
            modified = datetime.fromtimestamp(os.path.getmtime(filepath))
            mod_time = modified.strftime("%Y-%m-%d %H:%M")
            print(f"{Fore.GREEN}{i}.{Style.RESET_ALL} {file} ({size} bytes) - {mod_time}")
        
        return files[:10]
    
    def view_transcription(self, filename):
        """View content of a transcription file"""
        filepath = os.path.join(self.transcriptions_folder, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
            print(content)
            print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}❌ Error reading file: {e}{Style.RESET_ALL}")