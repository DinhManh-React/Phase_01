class BagOfWords:
    def __init__(self, documents):
        self.documents = documents

    def preprocessing(self, text):
        return text.lower().split()

    def build_vocabulary(self):
        vocab = []
        for doc in self.documents:
            words = self.preprocessing(doc)
            for word in words:
                if word not in vocab:
                    vocab.append(word)
        return vocab

    def create_vectors(self):
        vocabulary = self.build_vocabulary()
        vectors = []    
        for doc in self.documents:
            words = self.preprocessing(doc)
            vector = [0] * len(vocabulary)
            for word in words:
                idx = vocabulary.index(word)
                vector[idx] += 1
            vectors.append(vector)
        return vectors
    
documents = [
    "NLP is fun",
    "I love NLP",
    "NLP NLP NLP"
]
bow = BagOfWords(documents)
print(bow.create_vectors())