from core.audio_operations import download_audio, transcribe_audio
from core.wordcloud import generate_from_file

def print_menu():
    print("Options: ")
    print("1. Download Audio")
    print("2. Transcribe Audio")
    print("3. Generate Wordcloud")

opt = None
while opt != "exit":

    print_menu()
    opt = input("Enter an option (or 'exit' to quit): ")
    opt = opt.strip().lower()
    if opt == "1":
        download_audio("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    elif opt == "2":
        transcribe_audio(audio_path="static/audio.mp3", output_path="static/transcript.txt")
    elif opt == "3":
        generate_from_file(path="./static/transcript.txt")
    elif opt == "exit":
        print("Exiting the program")
    else:
        print("Invalid option, please try again")