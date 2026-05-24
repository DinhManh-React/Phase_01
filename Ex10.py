import json
import math
import os
import re
import sys
from difflib import get_close_matches

from Ex8 import TF_IDF
from crawl import OUTPUT_FILE, crawl_chiaki, save_documents

sys.stdout.reconfigure(encoding="utf-8")


def preprocessing(text):
    text = text.lower()
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"[^\w\sÀ-ỹ]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def load_data():
    if not os.path.exists(OUTPUT_FILE):
        data = crawl_chiaki(max_pages=20)
        save_documents(data)

    file = open(OUTPUT_FILE, "r", encoding="utf-8")
    data = json.load(file)
    file.close()
    return data


def tao_vector_query(query, vocabulary, idf, model):
    query = preprocessing(query)
    words = query.split()
    new_words = []

    for word in words:
        if word in vocabulary:
            new_words.append(word)
        else:
            gan_giong = get_close_matches(word, vocabulary, n=1, cutoff=0.8)
            if len(gan_giong) > 0:
                new_words.append(gan_giong[0])
            else:
                new_words.append(word)

    query = " ".join(new_words)
    tf_query = model.create_TF(query)
    vector = []

    for word in vocabulary:
        if word in tf_query:
            vector.append(tf_query[word] * idf[word])
        else:
            vector.append(0)

    return vector


def cosine_similarity(A, B):
    tu_so = 0
    mau_A = 0
    mau_B = 0

    for i in range(len(A)):
        tu_so += A[i] * B[i]
        mau_A += A[i] ** 2
        mau_B += B[i] ** 2

    mau = math.sqrt(mau_A) * math.sqrt(mau_B)
    if mau == 0:
        return 0
    return tu_so / mau


def search(query, data):
    documents = []

    for item in data:
        text = item["title"] + " " + item["description"] + " " + item["content"]
        documents.append(preprocessing(text))

    model = TF_IDF(documents)
    vocabulary, matrix_tfidf = model.TF_IDF()
    idf = model.create_IDF()
    query_vector = tao_vector_query(query, vocabulary, idf, model)

    result = []
    for i in range(len(matrix_tfidf)):
        score = cosine_similarity(query_vector, matrix_tfidf[i])
        result.append([score, data[i]["title"], data[i]["url"]])

    result = sorted(result, reverse=True)
    return result


data = load_data()
print("So document crawl duoc:", len(data))

query = input("Nhap cau truy van: ")
result = search(query, data)

print("\nKet qua tim kiem:")
for i in range(min(5, len(result))):
    score_percent = result[i][0] * 100
    print(i + 1, "Score:", str(round(score_percent, 2)) + "%")
    print("Title:", result[i][1])
    print("URL:", result[i][2])
    print()
