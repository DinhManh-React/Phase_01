import re

class WhitespaceTokenizer:
    def __init__(self,text):
        self.text = text

    def lowercase(self, text):
        text = self.text
        return text.lower()

    def normalize_whitespace(self, text):
        text = self.text
        text = self.lowercase(text)
        text = re.sub("\s+"," ",text)
        return text

    def tokenize(self, text):
        text = self.text
        text = self.normalize_whitespace(text)
        text = text.split()
        for token in text - 1:
            print(token)

text = input("Input Text: ")
Token = WhitespaceTokenizer(text)
print(Token.tokenize(text))