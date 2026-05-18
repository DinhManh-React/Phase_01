import math

class TF_IDF:
    def __init__(self, documents):
        self.documents = documents

    def preprocessing(self, text):
        return text.lower().split()
    
    def create_TF(self, doc):
        TF = {}
        words = self.preprocessing(doc)
        total_words = len(words)
        for word in words:
            TF[word] = TF.get(word, 0) + 1
        for word in TF:
            TF[word] = TF[word] / total_words
        return TF

    def create_IDF(self):
        N = len(self.documents)
        IDF = {}
        for doc in self.documents:
            words = self.preprocessing(doc)
            for word in words:
                IDF[word] = IDF.get(word, 0) + 1
        for word in IDF:
            IDF[word] = math.log(N / IDF[word])
        return IDF
    
    def TF_IDF(self):
        IDF = self.create_IDF()
        results = []
        matrix_vocab = []
        matrix_tfidf = []
        row = []
        for doc in range(len(self.documents)):
            TF = self.create_TF(self.documents[doc])
            tfidf = {}
            for word in TF:
                tfidf[word] = TF[word] * IDF[word]
                row.append(tfidf[word])
                if word not in matrix_vocab:
                    matrix_vocab.append(word)       
            results.append(tfidf)
            matrix_tfidf.append(row)
            row = []
        return results,matrix_vocab,matrix_tfidf


documents = [
    "I love NLP",
    "NLP is fun",
    "I love machine learning"
]
model = TF_IDF(documents)
result,matrix_vocab,matrix_tfidf = model.TF_IDF()
print(result)
print(matrix_vocab)
print(matrix_tfidf)
