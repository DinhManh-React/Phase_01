import re
from nltk.corpus import stopwords

class VietnameseTextProcessor:

    def __init__(self, text):
        self.text = text

    def sentence_tokenize(self):
        text = re.sub(r"\n+", " ", self.text)
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return sentences

    def word_tokenize(self, text):
        return text.split()

    def remove_urls(self, text):
        return re.sub(r'https?://\S+', '', text)

    def remove_html(self, text):
        return re.sub(r'<[^>]*>', ' ', text)

    def remove_emojis(self, text):
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"
            "\U0001F300-\U0001F5FF"
            "\U0001F680-\U0001F6FF"
            "\U00002600-\U000027BF"
            "]+",
            flags=re.UNICODE
        )
        return emoji_pattern.sub('', text)

    def remove_punctuation(self, text):
        return re.sub(r'[^\w\s]', '', text)

    def normalize_whitespace(self, text):
        return re.sub(r'\s+', ' ', text).strip()

    def remove_stopwords(self, tokens):
        stop_words = set(stopwords.words('english'))
        return [word for word in tokens if word.lower() not in stop_words]

    def preprocess(self):

        text = self.text

        text = self.remove_urls(text)
        text = self.remove_html(text)
        text = self.remove_emojis(text)
        text = self.remove_punctuation(text)
        text = self.normalize_whitespace(text)

        tokens = self.word_tokenize(text)

        tokens = self.remove_stopwords(tokens)

        return tokens
    
with open("text.txt",encoding='utf-8') as f:
    text=f.read()
Text_preprocess = VietnameseTextProcessor(text)
preprocess = Text_preprocess.preprocess()
print(preprocess)

