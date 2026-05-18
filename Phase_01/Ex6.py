class TermFrequency:
    def __init__(self, sentence):
        self.sentence = sentence

    def preprocess(self):
        return self.sentence.lower().split()

    def create_TF(self):
        TF = {}

        words = self.preprocess()
        total_words = len(words)
        for word in words:
            TF[word] = TF.get(word, 0) + 1
        for word in TF:
            TF[word] = TF[word] / total_words
        return TF

tf = TermFrequency("NLP is fun NLP NLP")
print(tf.create_TF())