from core.audio_operations import download_audio, transcribe_audio
from core.wordcloud import generate_from_file, generate_from_str

def print_menu():
    print("Options: ")
    print("1. Download Audio")
    print("2. Transcribe Audio")
    print("3. Generate Wordcloud from file")
    print("4. Generate Wordcloud from text")

opt = None
while opt != "exit":

    print_menu()
    opt = input("Enter an option (or 'exit' to quit): ")
    opt = opt.strip().lower()
    if opt == "1":
        download_audio(input("Url do vídeo: "))
    elif opt == "2":
        transcribe_audio(audio_path=input("Arquivo de áudio: "), output_path=input("Arquivo de destino: "))
    elif opt == "3":
        generate_from_file(path=input("Arquivo referência: "), output_file=input("Arquivo de saída: "))
    elif opt == "4":
        generate_from_str(text=input("Texto referência: "), output_file=input("Arquivo de saída: "))
    elif opt == "exit":
        print("Exiting the program")
    else:
        print("Invalid option, please try again")