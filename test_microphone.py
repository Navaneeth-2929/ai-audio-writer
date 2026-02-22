# test_microphone.py
import speech_recognition as sr

def list_microphones():
    """List all available microphones"""
    print("Available Microphones:")
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"Microphone {index}: {name}")

def test_microphone():
    """Simple microphone test"""
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            print("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=2)
            print("Microphone is ready! Speak now...")
            
            audio = recognizer.listen(source, timeout=5)
            print("Got audio! Testing recognition...")
            
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_microphones()
    print("\n" + "="*50)
    test_microphone()