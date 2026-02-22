# main.py
import sys
import os
from colorama import init, Fore, Style
from transcriber import SpeechTranscriber

# Initialize colorama
init(autoreset=True)

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Print application banner"""
    banner = f"""
{Fore.CYAN}{'⭐'*30}
{Fore.YELLOW}🎤 SPEECH-TO-TEXT TRANSCRIPTION TOOL
{Fore.CYAN}{'⭐'*30}
{Fore.GREEN}Convert your voice into text instantly!
{Fore.CYAN}{'⭐'*30}{Style.RESET_ALL}
"""
    print(banner)

def get_language_name(code):
    """Convert language code to readable name"""
    languages = {
        "en-US": "🇺🇸 English (US)",
        "en-GB": "🇬🇧 English (UK)",
        "es-ES": "🇪🇸 Spanish",
        "fr-FR": "🇫🇷 French",
        "de-DE": "🇩🇪 German",
        "it-IT": "🇮🇹 Italian",
        "pt-BR": "🇧🇷 Portuguese (Brazil)",
        "ja-JP": "🇯🇵 Japanese",
        "ko-KR": "🇰🇷 Korean",
        "zh-CN": "🇨🇳 Chinese (Mandarin)",
        "hi-IN": "🇮🇳 Hindi",
    }
    return languages.get(code, code)

def language_menu():
    """Display language selection menu"""
    languages = [
        ("en-US", "🇺🇸 English (US)"),
        ("en-GB", "🇬🇧 English (UK)"),
        ("es-ES", "🇪🇸 Spanish"),
        ("fr-FR", "🇫🇷 French"),
        ("de-DE", "🇩🇪 German"),
        ("it-IT", "🇮🇹 Italian"),
        ("pt-BR", "🇧🇷 Portuguese (Brazil)"),
        ("ja-JP", "🇯🇵 Japanese"),
        ("ko-KR", "🇰🇷 Korean"),
        ("zh-CN", "🇨🇳 Chinese (Mandarin)"),
        ("hi-IN", "🇮🇳 Hindi"),
    ]
    
    print(f"\n{Fore.CYAN}🌐 SELECT LANGUAGE:{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'-'*40}{Style.RESET_ALL}")
    for i, (code, name) in enumerate(languages, 1):
        print(f"{Fore.GREEN}{i:2}.{Style.RESET_ALL} {name}")
    print(f"{Fore.YELLOW}{'-'*40}{Style.RESET_ALL}")
    print(f"{Fore.GREEN} 0.{Style.RESET_ALL} Back to Main Menu")
    
    return languages

def test_microphone(transcriber):
    """Test if microphone is working"""
    print(f"\n{Fore.CYAN}🎤 TESTING MICROPHONE{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Speak something now...{Style.RESET_ALL}")
    
    try:
        with transcriber.microphone as source:
            transcriber.recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = transcriber.recognizer.listen(source, timeout=3)
        print(f"{Fore.GREEN}✅ Microphone is working!{Style.RESET_ALL}")
        return True
    except Exception as e:
        print(f"{Fore.RED}❌ Microphone test failed: {e}{Style.RESET_ALL}")
        return False

def main():
    """Main application loop"""
    # Initialize transcriber
    print(f"{Fore.YELLOW}Initializing Speech-to-Text Tool...{Style.RESET_ALL}")
    transcriber = SpeechTranscriber()
    
    current_language = "en-US"
    current_language_name = get_language_name(current_language)
    
    while True:
        clear_screen()
        print_banner()
        
        # Show current language
        print(f"{Fore.YELLOW}Current Language: {current_language_name}{Style.RESET_ALL}\n")
        
        # Main menu
        print(f"{Fore.CYAN}📋 MAIN MENU:{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{'─'*40}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}1.{Style.RESET_ALL} 🎙️  Live Microphone Transcription")
        print(f"{Fore.GREEN}2.{Style.RESET_ALL} 📁  Transcribe Audio File")
        print(f"{Fore.GREEN}3.{Style.RESET_ALL} 📋  View Saved Transcriptions")
        print(f"{Fore.GREEN}4.{Style.RESET_ALL} 🌐  Change Language")
        print(f"{Fore.GREEN}5.{Style.RESET_ALL} 🎤  Test Microphone")
        print(f"{Fore.GREEN}6.{Style.RESET_ALL} ❌  Exit")
        print(f"{Fore.YELLOW}{'─'*40}{Style.RESET_ALL}")
        
        choice = input(f"{Fore.CYAN}👉 Enter your choice (1-6): {Style.RESET_ALL}")
        
        if choice == "1":
            # Live transcription
            print(f"\n{Fore.CYAN}{'🎙️ LIVE TRANSCRIPTION MODE':^60}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Speak clearly. Press Ctrl+C to stop.{Style.RESET_ALL}\n")
            
            while True:
                try:
                    text = transcriber.transcribe_from_microphone(
                        language=current_language,
                        timeout=5
                    )
                    
                    if text:
                        print(f"\n{Fore.GREEN}📝 You said:{Style.RESET_ALL}")
                        print(f"{Fore.WHITE}{text}{Style.RESET_ALL}\n")
                        
                        # Ask if user wants to save
                        save = input(f"{Fore.YELLOW}💾 Save this transcription? (y/n): {Style.RESET_ALL}")
                        if save.lower() == 'y':
                            transcriber.save_transcription(text, "microphone")
                    
                    cont = input(f"{Fore.YELLOW}🔄 Continue listening? (y/n): {Style.RESET_ALL}")
                    if cont.lower() != 'y':
                        break
                        
                except KeyboardInterrupt:
                    print(f"\n{Fore.YELLOW}⏹️ Transcription stopped.{Style.RESET_ALL}")
                    break
        
        elif choice == "2":
            # File transcription
            print(f"\n{Fore.CYAN}{'📁 TRANSCRIBE AUDIO FILE':^60}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Supported formats: WAV, MP3, M4A, FLAC{Style.RESET_ALL}\n")
            
            file_path = input(f"{Fore.CYAN}📂 Enter audio file path: {Style.RESET_ALL}")
            
            if file_path:
                # Remove quotes if user added them
                file_path = file_path.strip('"\'')
                
                text = transcriber.transcribe_from_file(file_path, language=current_language)
                if text:
                    print(f"\n{Fore.GREEN}{'✅ TRANSCRIPTION RESULT':^60}{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}{'─'*60}{Style.RESET_ALL}")
                    print(f"{Fore.WHITE}{text}{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}{'─'*60}{Style.RESET_ALL}")
                    
                    # Ask if user wants to save
                    save = input(f"\n{Fore.YELLOW}💾 Save this transcription? (y/n): {Style.RESET_ALL}")
                    if save.lower() == 'y':
                        filename = os.path.basename(file_path)
                        transcriber.save_transcription(text, f"file_{filename}")
            
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        
        elif choice == "3":
            # View saved transcriptions
            print(f"\n{Fore.CYAN}{'📋 SAVED TRANSCRIPTIONS':^60}{Style.RESET_ALL}")
            files = transcriber.list_transcriptions()
            
            if files:
                view_choice = input(f"\n{Fore.CYAN}Enter number to view file (or Enter to skip): {Style.RESET_ALL}")
                if view_choice and view_choice.isdigit():
                    idx = int(view_choice) - 1
                    if 0 <= idx < len(files):
                        transcriber.view_transcription(files[idx])
            
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        
        elif choice == "4":
            # Change language
            languages = language_menu()
            lang_choice = input(f"\n{Fore.CYAN}👉 Select language (0-{len(languages)}): {Style.RESET_ALL}")
            
            if lang_choice.isdigit():
                lang_num = int(lang_choice)
                if 1 <= lang_num <= len(languages):
                    code, name = languages[lang_num-1]
                    current_language = code
                    current_language_name = name
                    print(f"{Fore.GREEN}✅ Language changed to {name}{Style.RESET_ALL}")
                elif lang_num == 0:
                    pass
                else:
                    print(f"{Fore.RED}❌ Invalid choice{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ Please enter a number{Style.RESET_ALL}")
            
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        
        elif choice == "5":
            # Test microphone
            test_microphone(transcriber)
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        
        elif choice == "6":
            print(f"\n{Fore.GREEN}👋 Thank you for using the Speech-to-Text Tool!{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Goodbye!{Style.RESET_ALL}\n")
            break
        
        else:
            print(f"{Fore.RED}❌ Invalid choice. Please enter a number between 1-6.{Style.RESET_ALL}")
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.GREEN}👋 Goodbye!{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}❌ An error occurred: {e}{Style.RESET_ALL}")
        input(f"\n{Fore.YELLOW}Press Enter to exit...{Style.RESET_ALL}")