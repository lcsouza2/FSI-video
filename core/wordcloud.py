from wordcloud import WordCloud

def generate_from_file(path: str, output_file: str = "wordcloud"):

    output_file = output_file.split(".")[0]

    with open(path) as text_file:
        content = text_file.read()

        wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_text(content)

        wordcloud.to_file(f"{output_file}.png")

def generate_from_str(text: str, output_file: str = "wordcloud"):

    output_file = output_file.split(".")[0]

    wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_text(text)

    wordcloud.to_file(f"{output_file}.png")