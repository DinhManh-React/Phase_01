import re
import time 
from datasets import load_dataset
from sklearn.model_selection import train_test_split

from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from Ex3_4 import OneHotEncoding
from Ex5 import BagOfWords
from Ex8 import TF_IDF
from sklearn.metrics import accuracy_score,f1_score
    
class TextClassification:
    def __init__(self,methods):
        self.methods = methods
        
    def proprocessing(self,sentence):
        sentence = sentence.lower()
        sentence = sentence.replace("\n","").replace("\r","")
        sentence = re.sub(r'[^\w\s]', '', sentence)
        emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  
                           u"\U0001F300-\U0001F5FF" 
                           u"\U0001F680-\U0001F6FF"  
                           u"\U0001F1E0-\U0001F1FF"  
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
        sentence = emoji_pattern.sub(r'',sentence)
        return sentence
    
    def dataset_split(self,features,labels):
        mapping_label = {}
        labels_list = []
        idx = 0
        for label in labels:
            if label not in mapping_label:
                mapping_label[label] = idx
                idx += 1
            labels_list.append(mapping_label[label])
        if self.methods == "TF_IDF":
            _,features_list = TF_IDF(features).TF_IDF()
        if self.methods == "BoW":
            features_list = BagOfWords(features).create_vectors()
        return train_test_split(features_list,labels_list,test_size=0.2, random_state=42)
        
    def train_multi_model(self,X_train,y_train,X_test,y_test):
        models = {
            "LogisticRegression" : LogisticRegression(max_iter=1000),
            "Navie Bayes:" : MultinomialNB()
        }
        for name , model in models.items():
            start_time = time.time()
            model.fit(X_train,y_train)
            end_time = time.time()
            predict = model.predict(X_test)
            acc = accuracy_score(y_pred=predict,y_true=y_test)
            f1 = f1_score(y_pred=predict,y_true=y_test,average="weighted")            
            print(f"\n{name}")
            print(f"Accuracy: {acc:.4f}")
            print(f"F1 Score: {f1:.4f}")
            print(f"Training Time: {end_time - start_time:.2f}s")   
           
datasets = load_dataset("clapAI/MultiLingualSentiment") # Counter({'negative': 442928, 'positive': 412535, 'neutral': 360246})
datasets = datasets.filter(lambda x: x["language"]=="en" )
datasets = datasets.shuffle(seed=42)
datasets = datasets.remove_columns(["source","domain","language"])
text = datasets["train"]["text"][:5000]
label = datasets["train"]["label"][:5000]
tf=TextClassification("TF_IDF")
X_train, X_test, y_train, y_test = tf.dataset_split(text, label)
print("Đang train mô hình phần TF-IDF")
tf.train_multi_model(X_train, y_train, X_test, y_test)
print("Đã train xong ở phần TF-IDF")
bow=TextClassification("BoW")
print("Đang train mô hình Bow")
X_train, X_test, y_train, y_test = bow.dataset_split(text,label)
bow.train_multi_model(X_train,y_train,X_test,y_test)
print("Done")
# Đang train mô hình phần TF-IDF

# LogisticRegression
# Accuracy: 0.6320
# F1 Score: 0.6183
# Training Time: 43.89s

# Navie Bayes:
# Accuracy: 0.6330
# F1 Score: 0.6174
# Training Time: 18.40s
# Đã train xong ở phần TF-IDF
# Đang train mô hình Bow

# LogisticRegression
# Accuracy: 0.6480
# F1 Score: 0.6481
# Training Time: 230.91s

# Navie Bayes:
# Accuracy: 0.6350
# F1 Score: 0.6274
# Training Time: 17.58s
