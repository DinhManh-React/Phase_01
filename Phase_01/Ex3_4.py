import numpy as np
class OneHotEncoding:
    def __init__(self, text):
        self.text = text

    def one_hot(self):
        words = self.text.split()
        vocab = list(set(words))
        word_to_index = {word: i for i, word in enumerate(vocab)}
        onehot = np.zeros((len(words), len(vocab)), dtype=int)
        for i, word in enumerate(words):
            onehot[i, word_to_index[word]] = 1

        return onehot


text = "I love Nlp Nlp is happy"
onehotencoding = OneHotEncoding(text)
result = onehotencoding.one_hot()
print(result)
