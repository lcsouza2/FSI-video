from wordcloud import WordCloud
from core.config import Config
from google import genai
from google.genai import types


def process_text_with_ai(filepath: str | None, plaintext: str | None):
    genai_client = genai.Client(api_key=Config.GENAI_API_KEY)

    if filepath:
        with open(filepath, "r") as file:
            texto = file.read()
    elif not filepath and plaintext:
        texto = plaintext
    elif filepath and plaintext:
        print("Envie somente o caminho para o arquivo ou texto puro")
        return
    else:
        print("Não enviou nenhum texto ou arquivo")
        return

    output = genai_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Vou gerar uma nuvem de palavras com esse texto, pode remover artigos preposições e etc? responda somente com o texto processado: {texto}",
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0)
        ),
    )

    return output.text


def generate_from_file(path: str, output_file: str = "wordcloud"):
    output_file = output_file.split(".")[0]

    with open(path) as text_file:
        content = text_file.read()

        wordcloud = WordCloud(
            width=800, height=400, background_color="white"
        ).generate_from_text(content)

        wordcloud.to_file(f"{output_file}.png")


def generate_from_str(text: str, output_file: str = "wordcloud"):
    output_file = output_file.split(".")[0]

    wordcloud = WordCloud(
        width=800, height=400, background_color="white"
    ).generate_from_text(text)

    wordcloud.to_file(f"{output_file}.png")
