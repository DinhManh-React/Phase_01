import math
class InverseDocumentFrequency:
    def __init__(self,document):
        self.document = document
    
    def propressing(self):
        return self.document.lower().split()
    
    def create_IDF(self):
        self.document = self.propressing()
        total_word = len(self.document)
        count = {}
        for word in self.document:
            count[word] = count.get(word, 0) + 1
            count[word] = math.log(total_word/count[word])
        return count
documents = "NLP is fun I love NLP NLP NLP NLP"
idf = InverseDocumentFrequency(documents)
print(idf.create_IDF())