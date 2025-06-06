from wordcloud import WordCloud
import matplotlib.pyplot as plt

def generate_from_file(path: str):

    with open(path) as text_file:
        content = text_file.read()

        wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_text(content)

        wordcloud.to_file("./static/wordcloud.png")

