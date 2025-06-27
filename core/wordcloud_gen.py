from wordcloud import WordCloud
import uuid

def generate_from_str(text: str):

    wordcloud = WordCloud(
        width=800, height=400, background_color="white"
    ).generate_from_text(text)

    path = f"./images/{str(uuid.uuid4())}.png"

    wordcloud.to_file(path)
    return path

