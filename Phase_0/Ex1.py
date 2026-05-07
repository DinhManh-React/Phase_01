class Frequency_Word:
    def __init__(self, document):
        self.document = document 

    def frequency_count(self):
        words = self.document.split()  
        frequency = {}
        for word in words:
            if word in frequency:
                frequency[word] += 1
            else:
                frequency[word] = 1    
        return frequency

doc = input("Input Document: ")
frequency_word = Frequency_Word(doc)

frequency = frequency_word.frequency_count()
print(f"{frequency}\n")
