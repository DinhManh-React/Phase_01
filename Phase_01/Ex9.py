import re
import time 
from datasets import load_dataset
from sklearn.model_selection import train_test_split

from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
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
        labels_list = []
        for label in labels:
            labels_list.append(label)
        labels_string = " ".join(labels_list)
        labels_list = OneHotEncoding(labels_string).one_hot()
        if self.methods == "TF_IDF":
            _,_,features_list = TF_IDF(features).TF_IDF()
        if self.methods == "BoW":
            features_list = BagOfWords(features).create_vectors()
        return train_test_split(features_list,labels_list,test_size=0.2,state_random=42)
        
    def train_multi_model(self,X_train,y_train,X_test,y_test):
        models = {
            "LogisticRegression" : LogisticRegression(),
            "Navie Bayes:" : GaussianNB()
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
datasets = datasets.remove_columns(["source","domain","language"])
text = datasets["train"]["text"]
label = datasets["train"]["label"]
tf=TextClassification("TF_IDF")
X_train,y_train,X_test,y_test = tf.dataset_split(text,label)
tf.train_multi_model(X_train,y_train,X_test,y_test)
bow=TextClassification("BoW")
X_train,y_train,X_test,y_test = tf.dataset_split(text,label)
tf.train_multi_model(X_train,y_train,X_test,y_test)
 